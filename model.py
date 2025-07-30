"""
Contains all functions pertaining to the model used in the recommendation system
"""
import openai
import sqlite3

# Define error messages
ERROR_MESSAGE_1 = "It sounds like you already know where you want to go! I simply recommended destinations. For more detailed travel advise, consult another travel app. Safe travels!"
ERROR_MESSAGE_2 = "In order for me to provide you with the best recommendations given your constraints, you must specify where you are traveling from. Please try again, and explicitly mention your origin location."
ERROR_MESSAGE_3 = "Sorry, I did not understand your prompt. I can only be used for travel recommendations. Please try again."
ERROR_MESSAGE_4 = "Please provide some more details about where you might want to go."
ERROR_MESSAGE_5 = "Unfortunately, I could not find any destinations that met your criteria. Consider trying different parameters and try again."

apikey = "YOUR API KEY HERE"
client = openai.OpenAI(api_key=apikey)

def load_schema_from_file():
    """
    Reads the schema of trip_recommender.sql and returns the results as a string
    """
    with open("trip_recommender.sql", 'r') as f:
        return f.read()

def get_country_names():
    """
    Helper function for generate_query. Returns the names of countries in the Country table as a list.
    """
    country_names = []
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Country')
    for row in cursor.fetchall():
        country_names.append(row[0])
    conn.close()
    return country_names

def get_destination_names():
    """
    Helper function for generate_query. Returns the names of destinations in the Destination table as a list.
    """
    destination_names = []
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM Destination')
    for row in cursor.fetchall():
        destination_names.append(row[0])
    conn.close()
    return destination_names

def generate_query(prompt, schema):
    """
    Function to generate a valid SQL query based on user input.
    """
    country_names = get_country_names()
    destination_names = get_destination_names()
    response = client.chat.completions.create(
        model="gpt-4", # for paid API keys
        #model="gpt-3.5-turbo", for free-tier API keys
        messages=[
            {"role": "user",
             "content": f"""Your task is to generate a SQL query based on the user's request. Do not
                        wrap the query in quotes, and be sure to include the ; at the end of the query.
                        Guidelines:
                            - Convert any user-specified country names to their corresponding country names in {country_names}
                            - Convert any user-specified origin city names to their corresponding names in {destination_names}
                            - If the user specifies a specific destination, return {ERROR_MESSAGE_1}
                            - If the user does not specify an origin city or where they are traveling from, return {ERROR_MESSAGE_2}
                            - If the user's prompt doesn't pertain to travel recommendations or is incomprehensible, return {ERROR_MESSAGE_3}
                            - Always select DISTINCT
                            - Always ORDER BY RANDOM()
                            - Values for CostOfLiving.budget_level are 'Luxury', 'Mid-range', and 'Budget'
                            - By default, only select destinations in countries where safety_index > 0
                                - If the user asks for "safe" destinations, only select destinations in countries where safety_index > 0.5
                            - visa_requirement in VisaRequirement table represents whether a visa is required to travel from origin_country_id to destination_country_id
                                - 0 = no visa required, 0.5 = visa required, 1 = travel banned
                                - Only recommend destinations that the user is not banned from (ie, visa_requirement != 1)
                            - Temperatures in the weather table are in Celcius
                            - Use the schema below and output only the condition
                            - If no filters are mentioned, return {ERROR_MESSAGE_4}
                            - If the user specifies a time constraint but no budget constraint, include the following condition in the WHERE clause:
                                D.distance_km <= (20 * hoursoftrip)
                                where D is the distance table
                            - If the user specifies a budget constraint but no time constraint, include the following condition in the WHERE clause:
                                D.distance_km <= ((userbudget - 15 - (5 * C.daily_avg_usd)) / 0.53)
                                where D is the distance table and C is the CostofLiving table
                            - If the user specifies both time and budget, include the following condition in the WHERE clause:
                                D.distance_km <= CASE
                                  WHEN ((userbudget - 15 - (daysoftrip * C.daily_avg_usd)) / 0.53) < (20 * hoursoftrip)
                                  THEN ((userbudget - 15 - (daysoftrip * C.daily_avg_usd)) / 0.53)
                                  ELSE (20 * hoursoftrip)
                                END
                                where D is the distance table and C is the CostofLiving table
                            - If the user mentions that they want to travel internationally or abroad, include the following condition in the WHERE clause:
                                Dest.country_id != (
                                    SELECT country_id
                                    FROM Destination
                                    WHERE destination_id = D.origin_id
                                )
                        Examples:
                            # Valid request
                            User: "I am traveling from Paris and want to go somewhere with good beaches."
                            SQL Query: "SELECT DISTINCT Dest.name
                                FROM Destination AS Dest
                                JOIN Country AS C
                                    ON Dest.country_id = C.country_id
                                JOIN VisaRequirement AS V
                                    ON C.country_id = V.destination_country_id
                                WHERE Dest.tags LIKE '%beach%'
                                AND (V.visa_requirement != 1)
                                ORDER BY RANDOM()
                                LIMIT 5
                                ;"
                            
                             # Valid request
                            User: "I Want To Go Somewhere Historical In March For A Week. I Am Traveling From Philadelphia
                            SQL Query: "SELECT DISTINCT Dest.name
                            FROM Distance AS D
                            JOIN Destination AS Dest
                              ON D.destination_id = Dest.destination_id
                            JOIN Country AS C
                                ON Dest.country_id = C.country_id
                            JOIN VisaRequirement AS V
                                ON C.country_id = V.destination_country_id
                            WHERE D.origin_id = (
                                SELECT destination_id
                                FROM Destination
                                WHERE name LIKE '%Philadelphia%'
                                LIMIT 1
                            ) AND
                            D.distance_km <= (20 * 7 * 24)
                            AND (V.visa_requirement != 1)
                            AND (Dest.tags LIKE '%historical%')
                            ORDER BY RANDOM()
                            LIMIT 5
                            ;"
                            
                            # Invalid request (no origin city specified)
                            User: "I am want to go to a city in germany for 3 days."
                            Return {ERROR_MESSAGE_2}
                            
                            # Invalid request (no origin city specified)
                            User: "I want to go somewhere historical in March."
                            Return {ERROR_MESSAGE_2}
                            
                            # Invalid request (destination city already known)
                            User: "Help me plan a trip to Hong Kong."
                            Return {ERROR_MESSAGE_1}
                        ---
                        Schema: {schema}
                        ---
                        User: {prompt}
                        SQL Query: """
            }
        ]
    )
    return response.choices[0].message.content

def execute_query(query):
    """
    Executes the query, a valid SQL query, on the trip_recommender.db and returns the results as rows
    """
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        return rows
    else:
        return None

def generate_response(prompt, results):
    """
    Generates and returns a response in English based on the user's prompt from queried results.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user",
             "content": f"""Your task is to recommend that the user travels to the destinations listed in the response.
                            Note that these destinations are the queried results based on the user's original prompt.
                            Guidelines:
                                - Provide a brief (a sentence or less) introduction to your response before providing the list of destinations.
                                - Briefly (in a sentence or less) explain each destination in the response and why they are a good fit.
                                - If the results are empty, respond with {ERROR_MESSAGE_5}
                            ---
                            User's prompt: {prompt}
                            Response: {results} """
             }
        ]
    )
    return response.choices[0].message.content

def main():
    # Example usage
    schema = load_schema_from_file()
    prompt = ("I am traveling from Boston and want to go somewhere in Europe for 10 days.")
    prompt = prompt.title()
    query = generate_query(prompt, schema)
    query = query.strip(' "')
    if query in {ERROR_MESSAGE_1, ERROR_MESSAGE_2, ERROR_MESSAGE_3, ERROR_MESSAGE_4}:
        return
    else:
        results = execute_query(query)
        response = generate_response(prompt, results)
        print(response)

if __name__ == "__main__":
    main()
