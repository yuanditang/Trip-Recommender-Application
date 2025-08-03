import wbgapi as wb
import pandas as pd
import sqlite3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO
from bs4 import BeautifulSoup
import re

def get_demonyms():
    """
    Helper function for get_visa_reqs. Demonyms are used instead of country names in Wikipedia's URLs for
    visa requirements
    """
    country_demonyms = {
    #"Aruba": "Aruban",
    "Afghanistan": "Afghan",
    "Angola": "Angolan",
    "Albania": "Albanian",
    "Andorra": "Andorran",
    "United Arab Emirates": "Emirati",
    "Argentina": "Argentine",
    "Armenia": "Armenian",
    #"American Samoa": "American Samoan",
    "Antigua and Barbuda": "Antigua and Barbuda",
    "Australia": "Australian",
    "Austria": "Austrian",
    "Azerbaijan": "Azerbaijani",
    "Burundi": "Burundian",
    "Belgium": "Belgian",
    "Benin": "Beninese",
    "Burkina Faso": "Burkinabé",
    "Bangladesh": "Bangladeshi",
    "Bulgaria": "Bulgarian",
    "Bahrain": "Bahraini",
    "Bahamas": "Bahamian",
    "Bosnia and Herzegovina": "Bosnia and Herzegovina",
    "Belarus": "Belarusian",
    "Belize": "Belizean",
    #"Bermuda": "Bermudian",
    "Bolivia": "Bolivian",
    "Brazil": "Brazilian",
    "Barbados": "Barbadian",
    "Brunei": "Bruneian",
    "Bhutan": "Bhutanese",
    "Botswana": "Botswana",
    "Central African Republic": "Central African",
    "Canada": "Canadian",
    "Switzerland": "Swiss",
    "Chile": "Chilean",
    "China": "Chinese",
    "Côte d'Ivoire": "Ivorian",
    "Cameroon": "Cameroonian",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    "Republic of the Congo": "Republic of the Congo",
    "Colombia": "Colombian",
    "Comoros": "Comorian",
    "Cape Verde": "Cape Verdean",
    "Costa Rica": "Costa Rican",
    "Cuba": "Cuban",
    #"Cayman Islands": "Caymanian",
    "Cyprus": "Cypriot",
    "Czech Republic": "Czech",
    "Germany": "German",
    "Djibouti": "Djiboutian",
    "Dominica": "Dominica",
    "Denmark": "Danish",
    "Dominican Republic": "Dominican Republic",
    "Algeria": "Algerian",
    "Ecuador": "Ecuadorian",
    "Egypt": "Egyptian",
    "Eritrea": "Eritrean",
    "Spain": "Spanish",
    "Estonia": "Estonian",
    "Ethiopia": "Ethiopian",
    "Finland": "Finnish",
    "Fiji": "Fijian",
    "France": "French",
    "Micronesia": "Micronesian",
    "Gabon": "Gabonese",
    "United Kingdom": "British",
    "Georgia": "Georgian",
    "Ghana": "Ghanaian",
    "Guinea": "Guinean",
    "Gambia": "Gambian",
    "Guinea-Bissau": "Guinea-Bissauan",
    "Equatorial Guinea": "Equatorial Guinean",
    "Greece": "Greek",
    "Grenada": "Grenadian",
    "Greenland": "Greenlandic",
    "Guatemala": "Guatemalan",
    #"Guam": "Guamanian",
    "Guyana": "Guyanese",
    "Hong Kong": "Chinese citizens of Hong Kong",
    "Honduras": "Honduran",
    "Croatia": "Croatian",
    "Haiti": "Haitian",
    "Hungary": "Hungarian",
    "Indonesia": "Indonesian",
    "India": "Indian",
    "Ireland": "Irish",
    "Iran": "Iranian",
    "Iraq": "Iraqi",
    "Iceland": "Icelandic",
    "Israel": "Israeli",
    "Italy": "Italian",
    "Jamaica": "Jamaican",
    "Jordan": "Jordanian",
    "Japan": "Japanese",
    "Kazakhstan": "Kazakhstani",
    "Kenya": "Kenyan",
    "Kyrgyzstan": "Kyrgyzstani",
    "Cambodia": "Cambodian",
    "Kiribati": "Kiribati",
    "Saint Kitts and Nevis": "Saint Kitts and Nevis",
    "South Korea": "South Korean",
    "Kuwait": "Kuwaiti",
    "Laos": "Laotian",
    "Lebanon": "Lebanese",
    "Liberia": "Liberian",
    "Libya": "Libyan",
    "Saint Lucia": "Saint Lucian",
    "Liechtenstein": "Liechtenstein",
    "Sri Lanka": "Sri Lankan",
    "Lesotho": "Lesotho",
    "Lithuania": "Lithuanian",
    "Luxembourg": "Luxembourgish",
    "Latvia": "Latvian",
    "Macau": "Chinese citizens of Macau",
    "Morocco": "Moroccan",
    "Monaco": "Monegasque",
    "Moldova": "Moldovan",
    "Madagascar": "Malagasy",
    "Maldives": "Maldivian",
    "Mexico": "Mexican",
    "Marshall Islands": "Marshall Islands",
    "North Macedonia": "North Macedonia",
    "Mali": "Malian",
    "Malta": "Maltese",
    "Myanmar": "Myanmar",
    "Montenegro": "Montenegrin",
    "Mongolia": "Mongolian",
    "Mozambique": "Mozambican",
    "Mauritania": "Mauritanian",
    "Mauritius": "Mauritian",
    "Malawi": "Malawian",
    "Malaysia": "Malaysian",
    "Namibia": "Namibian",
    "Niger": "Nigerien",
    "Nigeria": "Nigerian",
    "Nicaragua": "Nicaraguan",
    "Netherlands": "Dutch",
    "Norway": "Norwegian",
    "Nepal": "Nepalese",
    "Nauru": "Nauruan",
    "New Zealand": "New Zealand",
    "Oman": "Omani",
    "Pakistan": "Pakistani",
    "Panama": "Panamanian",
    "Peru": "Peruvian",
    "Philippines": "Philippine",
    "Palau": "Palauan",
    "Papua New Guinea": "Papua New Guinean",
    "Poland": "Polish",
    #"Puerto Rico": "Puerto Rican",
    "North Korea": "North Korean",
    "Portugal": "Portuguese",
    "Paraguay": "Paraguayan",
    "Palestine": "Palestinian",
    "Qatar": "Qatari",
    "Romania": "Romanian",
    "Russia": "Russian",
    "Rwanda": "Rwandan",
    "Saudi Arabia": "Saudi",
    "Sudan": "Sudanese",
    "Senegal": "Senegalese",
    "Singapore": "Singapore",
    "Solomon Islands": "Solomon Islands",
    "Sierra Leone": "Sierra Leonean",
    "El Salvador": "Salvadoran",
    "San Marino": "Sammarinese",
    "Somalia": "Somali",
    "Serbia": "Serbian",
    "South Sudan": "South Sudanese",
    "São Tomé and Príncipe": "Santomean",
    "Suriname": "Surinamese",
    "Slovakia": "Slovak",
    "Slovenia": "Slovenian",
    "Sweden": "Swedish",
    "Eswatini": "Swazi",
    "Seychelles": "Seychellois",
    "Syria": "Syrian",
    "Chad": "Chadian",
    "Togo": "Togolese",
    "Thailand": "Thai",
    "Taiwan": "Taiwanese",
    "Tajikistan": "Tajikistani",
    "Turkmenistan": "Turkmenistani",
    "Timor-Leste": "East Timorese",
    "Tonga": "Tongan",
    "Trinidad and Tobago": "Trinidad and Tobago",
    "Tunisia": "Tunisian",
    "Turkey": "Turkish",
    "Tuvalu": "Tuvaluan",
    "Tanzania": "Tanzanian",
    "Uganda": "Ugandan",
    "Ukraine": "Ukrainian",
    "Uruguay": "Uruguayan",
    "United States": "United States",
    "Uzbekistan": "Uzbekistani",
    "Saint Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Vatican City": "Vatican",
    "Venezuela": "Venezuelan",
    #"Virgin Islands (U.S.)": "U.S. Virgin Islander",
    "Vietnam": "Vietnamese",
    "Vanuatu": "Vanuatu",
    "Samoa": "Samoan",
    "Kosovo": "Kosovar",
    "Yemen": "Yemeni",
    "South Africa": "South African",
    "Zambia": "Zambian",
    "Zimbabwe": "Zimbabwean"
    }
    demonyms = pd.DataFrame((country_demonyms.items()), columns=["Country", "Demonym"])

    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Country;")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    table = pd.DataFrame(rows, columns=columns)
    demonyms = demonyms.merge(table, left_on='Country', right_on='name')
    demonyms = demonyms[['country_id', 'Demonym']]
    demonyms['Demonym'] = demonyms['Demonym'].replace(" ", "_")
    return demonyms

def get_visa_reqs():
    """
    Uses BeautifulSoup to extract visa requirements from Wikipedia. Writes to visa_requirements.csv to store results.
    """
    # https://en.wikipedia.org/wiki/Category:Visa_requirements_by_nationality
    dems = get_demonyms()
    i = 0
    for dem in dems.itertuples():
        url = f"https://en.wikipedia.org/wiki/Visa_requirements_for_{dem[2]}_citizens"
        if dem[2] == "North Macedonia": # North Macedonia has a different URL format
            url = f"https://en.wikipedia.org/wiki/Visa_requirements_for_citizens_of_North_Macedonia"
        elif dem[2][:20] == "Chinese citizens of ": # Chinese territories have a different URL format
            url = f"https://en.wikipedia.org/wiki/Visa_requirements_for_{dem[2]}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"{dem[2]}")
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.findAll('table')
            if tables:
                for table in tables:
                    df = pd.read_html(StringIO(str(table)))[0]

                    # Remove irrelevant/inconsistent columns
                    for c in df.columns:
                        cleaned = re.sub(r"[^\x20-\x7E]", "", str(c))
                        if re.match(r"Reciprocity(?: \[Note \d+\])?$", str(cleaned)) or re.match(r"Unnamed:?(?: \d+)?$", str(c)):
                            df = df.drop(columns=[c])

                    # Confirm table is the visa table
                    cols = [c for c in df.columns]
                    accepted_cols =[['Country', 'Visa requirement', 'Allowed stay', 'Notes (excluding departure fees)'], ['Country / Region', 'Visa requirement', 'Allowed stay', 'Notes (excluding departure fees)'], ['Country', 'Visa requirement', 'Allowed stay', 'Notes'], ['Country / Region', 'Visa requirement', 'Allowed stay', 'Notes'], ['Country', 'Entry requirement', 'Stay duration', 'Notes (excluding departure fees)']]
                    if cols not in accepted_cols:
                        continue

                    # Remove any added notes to columns and standardize country names
                    if "Visa requirement" in cols:
                        df["Visa requirement"] = df["Visa requirement"].astype(str).apply(lambda x: re.sub(r"\[\d+\]", "", x))
                    if "Entry requirement" in cols:
                        df["Entry requirement"] = df["Entry requirement"].astype(str).apply(lambda x: re.sub(r"\[\d+\]", "", x))
                    if "Country" in cols:
                        df["Country"] = df["Country"].astype(str).apply(lambda x: re.sub(r"\[\d+\]", "", x))
                        df["Country"] = df["Country"].str.replace(" and territories", "", regex=False)
                        df["Country"] = df["Country"].str.replace(" and Crown dependencies", "", regex=False)
                        df["Country"] = df["Country"].str.replace("People's Republic of ", "", regex=False)
                    if "Country / Region" in cols:
                        df["Country / Region"] = df["Country / Region"].astype(str).apply(lambda x: re.sub(r"\[\d+\]", "", x))
                        df["Country / Region"] = df["Country / Region"].str.replace(" and territories", "", regex=False)
                        df["Country / Region"] = df["Country / Region"].str.replace(" and Crown dependencies", "", regex=False)
                        df["Country / Region"] = df["Country / Region"].str.replace("People's Republic of ", "", regex=False)

                    # Add origin_country_id col and rename country col
                    df["origin_country_id"] = dem[1]
                    df = df.rename(columns={"Country": "destination_country", "Country / Region": "destination_country"})
                    df["destination_country"] = df["destination_country"].str.replace("China (People's Republic of)", "China", regex=False)
                    df["destination_country"] = df["destination_country"].str.replace("Mainland China", "China", regex=False)
                    # Write to file
                    if i == 0:
                        df.to_csv(f"visa_requirements.csv", index=False)
                        break
                    else:
                        df.to_csv(f"visa_requirements.csv", mode='a', header=False, index=False)
                        break
            i += 1
        else:
            print(f"\nFailed to retrieve page for {dem[2]}. Status code: {response.status_code}\n")

def create_visa_schema():
    """
    Function used to create the schema of the VisaRequirement table
    """
    visa_requirements_dict = {
        "evisa": 0.5,
        "visa required": 0.5,
        "evisa / visa on arrival": 0,
        "visa on arrival": 0,
        "online visa": 0.5,
        "online visa / visa on arrival": 0,
        "visa not required": 0,
        "visa not required (conditional)": 0,
        "electronic travel authorisation": 0,
        "e-voa": 0,
        "free visa on arrival": 0,
        "entry permit on arrival": 0,
        "electronic border system": 0.5,
        "eta / visa on arrival": 0,
        "admission refused": 1,
        "pre-enrolment": 0.5,
        "evisa.": 0.5,
        "pre-visa on arrival": 0,
        "e-visa": 0.5,
        "evisa/visa on arrival": 0,
        "electronic travel authorization": 0,
        "freedom of movement": 0,
        "free evisa": 0.5,
        "visa not required (conditional) / evisa": 0,
        "evisitor": 0,
        "e-voa / visa on arrival": 0,
        "electronic travel authority": 0,
        "evisa / free visa on arrival": 0,
        "free visitor's permit on arrival": 0,
        "electronic visa": 0.5,
        "visa waiver program": 0,
        "travel restricted by uae government": 1,
        "online visa required": 0.5,
        "visa not required / evisa": 0,
        "visa on arrival / evisa": 0,
        "easy visitor permit": 0,
        "visitor's permit on arrival": 0,
        "permit on arrival": 0,
        "electronical travel authorization": 0,
        "tourist card required": 0.5,
        "special permit required": 0.5,
        "e-voa/visa on arrival": 0,
        "online visitor e600 visa": 0,
        "partial visa restrictions": 0.5,
        "evisa required": 0.5,
        "evisa/ visa on arrival": 0,
        "electronic travel authorization/ visa on arrival": 0,
        "k-eta required": 0.5,
        "electronic travel authorisation required": 0.5,
        "de facto visa required": 0.5,
        "visa not required / e-voa": 0,
        "eta / online visa": 0.5,
        "evisa / visa not required": 0,
        "online visa / free visa on arrival": 0,
        "free eta / visa on arrival": 0,
        "visitor e600 visa": 0.5,
        "e-tourist card": 0.5,
        "eta / visa not required": 0,
        "ease": 0.5,
        "eta-il": 0.5,
        "freedom of movement (european netherlands)": 0,
        "nzeta": 0,
        "eta": 0,
        "evisa /visa on arrival": 0,
        "e-visa/visa on arrival": 0,
        "visa on arrival /evisa": 0,
        "electronic travel authorization/visa on arrival": 0,
        "visa free": 0,
        "eta required": 0,
        "visa on arrival (conditional)": 0,
        "visa on arrvival": 0,
        "online visa/visa on arrival": 0,
        "korean electronic travel authorization": 0.5,
        "visa de facto required": 0.5,
        "freedom of movement (in mainland denmark)": 0,
        "eta}}": 0,
        "electronic entry visa": 0.5,
        "tourist card / evisa": 0.5,
        "electronic visa waiver / visa on arrival": 0,
        "k-eta": 0.5,
        "free entry permit on arrival": 0,
        "seychelles electronic border system": 0,
        "admission restricted": 0.5,
        "visa on arrival (ease)": 0,
        "visa waiver registration": 0.5,
        "free eta/ visa on arrival": 0,
        "travel banned[note 2][citation needed]": 1,
        "electronic visa eta": 0.5,
        "travel illegal under israeli law": 1,
        "permission required": 0.5,
        "visa required / visa on arrival": 0,
        "e-visa / visa on arrival": 0,
        "free evisa / visa on arrival": 0,
        "visa not required / free evisa": 0,
        "travel banned": 1,
        "particular visit regime": 0,
        "visa reqiored": 0.5,
        "free visitor’s permit on arrival": 0,
        "electronic travel authorisation/ visa on arrival": 0,
        "visa not required (conditions apply)": 0,
        "evisa / visa on arrival ": 0,
        "free visitor permit on arrival": 0,
        "visa required (conditional eta)": 0.5,
        "visa not required[note 1]": 0,
        "eta /visa on arrival": 0,
        "eta/ visa on arrival": 0,
        "travel banned by the malaysian government": 1,
        "evisitor or electronic travel authority": 0,
        "invitation only": 0.5,
        "invitation required": 0.5,
        "currently suspended": 1,
        "online visa (conditional)": 0.5,
        "indefinite": 0.5,
        "freedom of movement (mainland denmark)": 0,
        "e-visa /visa on arrival": 0,
        "free visa on arrival ": 0,
        "electronic authorization": 0.5,
        "evisa / visa on arrival}": 0,
        "visa not required (conditionally)": 0,
        "visa on arrival or evisa": 0,
        "evisa or visa on arrival": 0,
        "esta": 0.5,
        "tourist card / evisa[citation needed]": 0.5,
        "e-voa / visa on arrival[citation needed]": 0,
        "evisa / visa on arrival[citation needed]": 0,
        "visa not required[citation needed]": 0,
        "russian evisa": 0.5,
        "evisa on arrival": 0,
        "visa on arrival/evisa": 0,
        "electronic authorization system": 0.5,
        "tourist card required / evisa": 0.5,
        "evisa / visa on arrival (conditional)": 0,
        "admission suspended": 1,
        "travel restricted by u.s. government": 1,
        "freedom of movement (conditional)": 0,
        "visa required.": 0.5,
        "id card valid": 0.5,
        "travel certificate required": 0.5,
        "affidavit of identity required": 0.5,
        "home return permit travel (freedom of movement)": 0,
        "with mainland travel permit for taiwan residents or chinese travel document only, including airside transit": 0
    }
    not_found = set()
    visa_df = pd.read_csv("visa_requirements.csv")
    for idx, row in visa_df.iterrows():
        # First change destination country name to country_id
        visa_df.at[idx, "Visa requirement"] = visa_requirements_dict.get(row["Visa requirement"].lower().rstrip(), row["Visa requirement"].lower().rstrip())
    visa_df = visa_df.rename(columns={"Visa requirement": "visa_requirement"})
    visa_df = visa_df[["origin_country_id", "destination_country", "visa_requirement"]]
    visa_df.to_csv("simplified_visa_table.csv", index=False)

def clean_countries():
    """
    Used to standardize country names. Updates the Country table with these standardized names.
    """
    updated_country_names = {
        "Bahamas, The": "Bahamas",
        "Brunei Darussalam": "Brunei",
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Congo, Rep.": "Republic of the Congo",
        "Cabo Verde": "Cape Verde",
        "Czechia": "Czech Republic",
        "Egypt, Arab Rep.": "Egypt",
        "Micronesia, Fed. Sts.": "Micronesia",
        "Gambia, The": "Gambia",
        "Hong Kong SAR, China": "Hong Kong",
        "Iran, Islamic Rep.": "Iran",
        "Kyrgyz Republic": "Kyrgyzstan",
        "St. Kitts and Nevis": "Saint Kitts and Nevis",
        "Korea, Rep.": "South Korea",
        "Lao PDR": "Laos",
        "St. Lucia": "Saint Lucia",
        "Macao SAR, China": "Macau",
        "Korea, Dem. People's Rep.": "North Korea",
        "West Bank and Gaza": "Palestine",
        "Russian Federation": "Russia",
        "Sao Tome and Principe": "São Tomé and Príncipe",
        "Slovak Republic": "Slovakia",
        "Syrian Arab Republic": "Syria",
        "Turkiye": "Turkey",
        "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
        "Venezuela, RB": "Venezuela",
        "Virgin Islands (U.S.)": "U.S. Virgin Islands",
        "Viet Nam": "Vietnam",
        "Yemen, Rep.": "Yemen"
    }
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    for key, value in updated_country_names.items():
        cursor.execute(f"UPDATE Country SET name = ? WHERE name = ?;", (value, key))
    conn.commit()
    cursor.execute("SELECT * FROM Country")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def get_country_df():
    """
    Uses the World Bank API's PV.EST dataset (Political Stability and Absence of Violence/Terrorism: Estimate)
    to create and return a dataframe of countries as well as their safety indices. Returns the DataFrame.
    """

    countries = pd.DataFrame(wb.economy.list())
    countries = countries[countries['region'] != 'Aggregates']
    country_df = countries[['id', 'value']].rename(columns={
        'id': 'iso_code',
        'value': 'Country'
    })

    # Fetch latest data (2023 is the latest year)
    safety_df = wb.data.DataFrame(['PV.EST'], time=2023, labels=True).dropna()
    country_df = country_df.merge(safety_df, on='Country').rename(columns={
        'PV.EST': 'safety_index',
        'Country': 'name'
    })
    country_df.index.name = 'country_id'

    return country_df

def insert_data(df):
    """
    Helper function used to append a pandas DataFrame to the database
    """
    # Connect to a SQLite DB
    conn = sqlite3.connect('trip_recommender.db')

    # Execute schema file
    try:
        with open('trip_recommender.sql', 'r') as f:
            conn.executescript(f.read())

        df.to_sql('Country', conn, if_exists='append', index=False)
        conn.commit()
    finally:
        conn.close()

def insert_edge_countries():
    """
    Used to insert "Taiwan" and "Vatican City" into Countries, as these were not listed in the
    World Bank's dataset. To calculate safety indices, the 'parent' country's safety index was
    used as an approximation (ie, Vatican City is a city-state within Italy, and Taiwan is a
    disputed territory of China)
    """
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(country_id) FROM Country")
    max_id = cursor.fetchone()[0] or 0
    start_id = max_id + 1
    cursor.execute("SELECT name, safety_index FROM Country WHERE name IN ('China', 'Italy');")
    safety_keys = dict(cursor.fetchall())
    conn.close()

    missing_countries = {"country_id": list(range(start_id, start_id + 2)),
                         "name": ["Taiwan", "Vatican City"],
                         "iso_code": ["TWN", "VAT"],
                         "safety_index": [safety_keys["China"], safety_keys["Italy"]]
                         }

    missing_countries_df = pd.DataFrame(missing_countries)
    insert_data(missing_countries_df)

def fetch_nasa_data(lat, lon, parameter):
    """
    Helper function for get_climate_data. Used to fetch NASA climate data for a single geographic cell.
    Returns a single line of a csv containing the NASA climate data for that cell.
    """
    nasa_url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start": 2014, #YYYY
        "end": 2024, #YYYY
        "parameters": parameter,
        "community": "AG", # Agroclimatology
        "format": "csv",
        "time-standard": "utc",
        "header": False # header contains metadata on request
    }
    response = requests.get(nasa_url, params=params)
    if "failed to complete your request" in response.text:
        raise ValueError(response.text)
    else:
        climate_df = pd.read_csv(StringIO(response.text)).drop('YEAR', axis=1)
        mean_climate_df = climate_df.mean(numeric_only=True).to_frame().T
        mean_climate_df = mean_climate_df.add_prefix(f"mean_{'temp' if parameter == 'T2M' else 'precip'}_")
        mean_climate_df.columns = mean_climate_df.columns.str.lower()
        return mean_climate_df

def get_climate_data(dest_id, lat, lon):
    """
    Used to fetch climate data for a single location using NASA's API
    """
    temp_df = fetch_nasa_data(lat, lon, "T2M")
    precip_df = fetch_nasa_data(lat, lon, "PRECTOTCORR")
    climate_df = pd.concat([temp_df, precip_df], axis=1)
    climate_df["destination_id"] = dest_id
    return climate_df

def populate_weather_table():
    """
    Function used to populate the weather table with temperature (degrees C) and precipitation (mm/day) data.
    """
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute("SELECT destination_id, latitude, longitude FROM Destination")
    rows = cursor.fetchall()
    weather_table = pd.DataFrame(columns=['mean_temp_jan', 'mean_temp_feb', 'mean_temp_mar', 'mean_temp_apr',
       'mean_temp_may', 'mean_temp_jun', 'mean_temp_jul', 'mean_temp_aug',
       'mean_temp_sep', 'mean_temp_oct', 'mean_temp_nov', 'mean_temp_dec',
       'mean_temp_ann', 'mean_precip_jan', 'mean_precip_feb',
       'mean_precip_mar', 'mean_precip_apr', 'mean_precip_may',
       'mean_precip_jun', 'mean_precip_jul', 'mean_precip_aug',
       'mean_precip_sep', 'mean_precip_oct', 'mean_precip_nov',
       'mean_precip_dec', 'mean_precip_ann', 'destination_id'])

    i = 1
    with ThreadPoolExecutor(max_workers=7) as executor:
        results = [executor.submit(get_climate_data, row[0], row[1], row[2]) for row in rows]
        for f in as_completed(results):
            row_climate = f.result()
            weather_table = pd.concat([weather_table, row_climate], ignore_index=True)
            print(f"Row {i} added")
            i += 1

    return weather_table

def query_db(table_name):
    """
    Function that is used to query the database. Provides an overview of tables and rows.
    Mostly used to assist with debugging.
    """
    print(f"{table_name}:")
    conn = sqlite3.connect('web/trip_recommender.db')
    cursor = conn.cursor()
    try:
        print("Schema:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print("Head:")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except:
        print(f"{table_name} not found")
    print("\n")
    conn.close()

def alter_weather_schema():
    """
    Function that was used to update the weather table schema
    """
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    script = """
    CREATE TABLE IF NOT EXISTS Weather_New (
        weather_id INTEGER NOT NULL PRIMARY KEY,
        destination_id INTEGER NOT NULL,
        mean_temp_jan REAL,
        mean_temp_feb REAL,
        mean_temp_mar REAL,
        mean_temp_apr REAL,
        mean_temp_may REAL,
        mean_temp_jun REAL,
        mean_temp_jul REAL,
        mean_temp_aug REAL,
        mean_temp_sep REAL,
        mean_temp_oct REAL,
        mean_temp_nov REAL,
        mean_temp_dec REAL,
        mean_temp_ann REAL,
        mean_precip_jan REAL,
        mean_precip_feb REAL,
        mean_precip_mar REAL,
        mean_precip_apr REAL,
        mean_precip_may REAL,
        mean_precip_jun REAL,
        mean_precip_jul REAL,
        mean_precip_aug REAL,
        mean_precip_sep REAL,
        mean_precip_oct REAL,
        mean_precip_nov REAL,
        mean_precip_dec REAL,
        mean_precip_ann REAL,
        FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
    );
    DROP TABLE Weather;
    ALTER TABLE Weather_New RENAME TO Weather;
    """
    conn.executescript(script)
    conn.commit()
    conn.close()

def main():
    query_db("Country")

if __name__ == "__main__":
    main()