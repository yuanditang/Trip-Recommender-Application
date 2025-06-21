def load_cost_of_living_data(csv_path='/mnt/data/living cost.csv'):
    # Load CSV
    df = pd.read_csv(csv_path)

    # Clean up DataFrame
    df = df.rename(columns={
        'Rank': 'cost_of_living_id',
        'City': 'city_name',
        'Groceries Index': 'avg_cost_for_food',
        'Cost of Living Index': 'cost_index'
    })

    # Drop rows without valid cities or cost index
    df = df.dropna(subset=['city_name', 'cost_index'])

    # Connect to the DB and fetch destination IDs
    conn = sqlite3.connect('trip_recommender.db')
    dest_df = pd.read_sql_query("SELECT destination_id, name FROM Destination", conn)

    # Merge to get destination_id
    df = df.merge(dest_df, how='left', left_on='city_name', right_on='name')

    # Assign budget_level based on cost_index
    def classify_budget(cost):
        if cost < 50:
            return 'Low'
        elif cost < 80:
            return 'Medium'
        else:
            return 'High'

    df['budget_level'] = df['cost_index'].apply(classify_budget)

    # Prepare final DataFrame for insertion
    final_df = df[['cost_of_living_id', 'destination_id', 'avg_cost_for_food', 'budget_level']].copy()
    final_df['daily_avg_usd'] = None  # or set default/estimated values

    # Ensure the CostOfLiving table exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS CostOfLiving (
            cost_of_living_id INTEGER NOT NULL PRIMARY KEY,
            destination_id INTEGER NOT NULL,
            daily_avg_usd DOUBLE,
            avg_cost_for_food DOUBLE,
            budget_level VARCHAR(25),
            FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
        );
    ''')

    # Insert into DB
    final_df.to_sql('CostOfLiving', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()