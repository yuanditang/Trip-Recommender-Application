"""
Contains all functions pertaining to the model used in the recommendation system
    Examples:
    User: I want a cheap hotel in Boston with a pool.
    SELECT name FROM Destination WHERE clause: price < 100 AND location = 'Boston' AND has_pool = TRUE
    User: Something luxurious in New York
    SELECT name FROM Destination WHERE clause: price > 300 AND location = 'New York'
    User: I'm just browsing
    FALSE
"""
import openai
import sqlite3

# Note that, below, an environment should be used to conceal the secret (enhance security)
apikey = "PUT YOUR API KEY HERE"
client = openai.OpenAI(api_key=apikey)

def load_schema_from_file():
    with open("trip_recommender.sql", 'r') as f:
        return f.read()

def generate_query(prompt, schema):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user",
             "content": f"""Your task is to generate a SQL query based on the user's request. Do not
                        wrap the query in quotes, and be sure to include the ; at the end of the query.
                        Also note, temperatures in the weather table are in Celcius.
                        Use the schema below and output only the condition
                        If no filters are mentioned, return False.
                        Schema: {schema}
                        ---
                        User: {prompt}
                        SQL Query: """
            }
        ]
    )
    return response.choices[0].message.content

def execute_query(query):
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        print("Query results:")
        for row in rows:
            print(row)
        return rows
    else:
        print("No results found.")
        return None

def generate_response(prompt, results):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user",
             "content": f"""Your task is to answer the user's original prompt with the
                            destinations listed in the response.
                            User's prompt: {prompt}
                            Response: {results} """
             }
        ]
    )
    print(response.choices[0].message.content)

def main():
    # Example usage
    schema = load_schema_from_file()
    prompt = "I want to go somewhere warm in the winter in the united states. ideally, i wouldn't spend more than $150 a day."
    print(prompt)
    query = generate_query(prompt, schema)
    print(query)
    if query is not False:
        results = execute_query(query)
        if results is not None:
            generate_response(prompt, results)
        else:
            print("Could not find relevant results.")
    else:
        print("Please provide a more specific travel request.")

if __name__ == "__main__":
    main()
