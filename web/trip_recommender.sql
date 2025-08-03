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
    safety_index DOUBLE,
    continent TEXT
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
    type TEXT,
    FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

-- Lodging Table
CREATE TABLE Lodging (
	lodging_id INT PRIMARY KEY,
	destination_id	INT,
	name	VARCHAR(255),
	hotel_type	VARCHAR(100),
	avg_price	DECIMAL(10, 2),
	rating	DECIMAL(3, 2),
	FOREIGN KEY("destination_id") REFERENCES "destination"("destination_id")
)

-- VisaRequirement Table
CREATE TABLE IF NOT EXISTS VisaRequirement (
    visa_requirement_id INTEGER NOT NULL PRIMARY KEY,
    origin_country_id INTEGER NOT NULL,
    destination_country_id INTEGER NOT NULL,
    visa_requirement REAL,
    FOREIGN KEY (origin_country_id) REFERENCES Country(country_id)
    FOREIGN KEY (destination_country_id) REFERENCES Country(country_id)
);

-- Weather Table
CREATE TABLE IF NOT EXISTS Weather(
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

-- Distance Table
CREATE TABLE "Distance" (
	"distance_id"	INTEGER,
	"origin_id"	INTEGER NOT NULL,
	"destination_id"	INTEGER NOT NULL,
	"distance_km"	REAL,
	PRIMARY KEY("distance_id" AUTOINCREMENT),
	FOREIGN KEY("destination_id") REFERENCES "Destination"("destination_id"),
	FOREIGN KEY("origin_id") REFERENCES "Destination"("destination_id")
)
