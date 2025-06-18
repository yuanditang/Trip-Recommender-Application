-- Attraction Table
CREATE TABLE IF NOT EXISTS Attraction (
    attraction_id INTEGER NOT NULL PRIMARY KEY,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type VARCHAR(50),
    rating DOUBLE,
    description TEXT,
    url TEXT,
    FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
);

-- CostOfLiving Table
CREATE TABLE IF NOT EXISTS CostOfLiving (
    cost_of_living_id INTEGER NOT NULL PRIMARY KEY,
    destination_id INTEGER NOT NULL,
    daily_avg_usd DOUBLE,
    avg_cost_for_food DOUBLE,
    budget_level VARCHAR(25),
    FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
);

-- Country Table
CREATE TABLE IF NOT EXISTS Country (
    country_id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    iso_code VARCHAR(10) NOT NULL,
    safety_index DOUBLE
);

-- Destination Table
CREATE TABLE IF NOT EXISTS Destination (
    destination_id INTEGER NOT NULL PRIMARY KEY,
    country_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    description TEXT,
    tags VARCHAR(50),
    FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

-- Lodging Table
CREATE TABLE IF NOT EXISTS Lodging (
    lodging_id INTEGER NOT NULL PRIMARY KEY,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type VARCHAR(50),
    avg_price_per_night DOUBLE NOT NULL,
    rating DOUBLE,
    url TEXT,
    description TEXT,
    FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
);

-- TransportOption Table
CREATE TABLE IF NOT EXISTS TransportOption (
    transport_id INTEGER NOT NULL PRIMARY KEY,
    destination_id INTEGER NOT NULL,
    origin_city TEXT NOT NULL,
    transport_type VARCHAR(50) NOT NULL,
    avg_duration_hours DOUBLE NOT NULL,
    avg_price_usd DOUBLE NOT NULL,
    carrier_name TEXT,
    notes TEXT,
    FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
);

-- VisaRequirement Table
CREATE TABLE IF NOT EXISTS VisaRequirement (
    visa_requirement_id INTEGER NOT NULL PRIMARY KEY,
    destination_country_id INTEGER NOT NULL,
    visa_required_origin_countries TEXT,
    banned_origin_countries TEXT,
    FOREIGN KEY (destination_country_id) REFERENCES Country(country_id)
);

-- Weather Table
CREATE TABLE IF NOT EXISTS Weather (
    weather_id INTEGER NOT NULL PRIMARY KEY,
    destination_id INTEGER NOT NULL,
    avg_monthly_temp_c TEXT,
    avg_monthly_precip_mm TEXT,
    best_travel_months TEXT,
    FOREIGN KEY (destination_id) REFERENCES Destination(destination_id)
);