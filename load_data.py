import wbgapi as wb
import pandas as pd
import sqlite3

def get_country_df():
    """
    Below are the potentially relevant datasets:
        # VC.IHR.PSRC.P5 - Intentional homicides (per 100,000 people)
        # PV.EST - Political Stability and Absence of Violence/Terrorism: Estimate
        # PV.PER.RNK - Political Stability and Absence of Violence/Terrorism: Percentile Rank
        # GE.EST - Government Effectiveness: Estimate
        # CC.EST - Corruption
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
    # Connect to a new SQLite DB
    conn = sqlite3.connect('trip_recommender.db')

    # Execute schema file
    with open('trip_recommender_sqlite.sql', 'r') as f:
        conn.executescript(f.read())

    df.to_sql('Country', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

def edit_db():
    conn = sqlite3.connect('trip_recommender.db')

    # Drop the Attraction table and add type attribute to Destination table
    conn.execute("DROP TABLE IF EXISTS Attraction;")
    conn.execute("ALTER TABLE Destination ADD COLUMN type TEXT;")
    conn.commit()
    conn.close()


def main():
    edit_db()
    #country_df = get_country_df()
    #insert_data(country_df)

if __name__ == '__main__':
    main()
