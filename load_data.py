import wbgapi as wb
import pandas as pd
import sqlite3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO

query = """
-- USA Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(193, 'Boston (Manchester)', 42.3601, -71.0589, 'Major northeastern city with rich history', 'city,historical', 'urban'),
(193, 'Springfield-Holyoke', 42.1015, -72.5898, 'Western Massachusetts metro area', 'city', 'urban'),
(193, 'Hartford & New Haven', 41.7637, -72.6851, 'Connecticut metropolitan region', 'city', 'urban'),
(193, 'Providence-New Bedford', 41.8240, -71.4128, 'Rhode Island and southeastern Massachusetts area', 'city,coastal', 'urban'),
(193, 'Portland-Auburn', 43.6591, -70.2568, 'Southern Maine metropolitan area', 'city,coastal', 'urban'),
(193, 'Bangor', 44.8016, -68.7712, 'Eastern Maine city', 'city', 'urban'),
(193, 'Presque Isle', 46.6812, -68.0159, 'Northern Maine region', 'city,rural', 'urban'),
(193, 'Burlington-Plattsburgh', 44.4759, -73.2121, 'Lake Champlain region', 'city,lakeside', 'urban'),
(193, 'New York', 40.7128, -74.0060, 'Largest US metropolitan area', 'city,megacity', 'urban'),
(193, 'Albany-Schenectady-Troy', 42.6526, -73.7562, 'New York state capital region', 'city', 'urban'),
(193, 'Buffalo', 42.8864, -78.8784, 'Western New York city near Niagara Falls', 'city', 'urban'),
(193, 'Rochester NY', 43.1566, -77.6088, 'Finger Lakes region city', 'city', 'urban'),
(193, 'Syracuse', 43.0481, -76.1474, 'Central New York city', 'city', 'urban'),
(193, 'Binghamton', 42.0987, -75.9180, 'Southern Tier region of NY', 'city', 'urban'),
(193, 'Elmira (Corning)', 42.0898, -76.8077, 'Southern Tier region', 'city', 'urban'),
(193, 'Utica', 43.1009, -75.2327, 'Mohawk Valley region', 'city', 'urban'),
(193, 'Watertown', 43.9748, -75.9108, 'Northern New York near Fort Drum', 'city', 'urban'),
(193, 'Philadelphia', 39.9526, -75.1652, 'Historic Pennsylvania city', 'city,historical', 'urban'),
(193, 'Pittsburgh', 40.4406, -79.9959, 'Western Pennsylvania city', 'city', 'urban'),
(193, 'Harrisburg-Lancaster-Lebanon-York', 40.2732, -76.8867, 'South central Pennsylvania region', 'city', 'urban'),
(193, 'Wilkes Barre-Scranton-Hazleton', 41.2465, -75.8819, 'Northeastern Pennsylvania region', 'city', 'urban'),
(193, 'Johnstown-Altoona-State College', 40.3267, -78.9220, 'Central Pennsylvania region', 'city', 'urban'),
(193, 'Erie', 42.1292, -80.0851, 'Northwestern Pennsylvania on Lake Erie', 'city,lakeside', 'urban'),
(193, 'Baltimore', 39.2904, -76.6122, 'Maryland''s largest city', 'city,coastal', 'urban'),
(193, 'Salisbury', 38.3607, -75.5994, 'Eastern Shore of Maryland', 'city,coastal', 'urban'),
(193, 'Washington D.C. (Hagerstown)', 38.9072, -77.0369, 'US capital region', 'city,capital', 'urban'),
(193, 'Norfolk-Portsmouth-Newport News', 36.8508, -76.2859, 'Hampton Roads region of Virginia', 'city,coastal', 'urban'),
(193, 'Richmond-Petersburg', 37.5407, -77.4360, 'Virginia capital region', 'city', 'urban'),
(193, 'Roanoke-Lynchburg', 37.2710, -79.9414, 'Western Virginia region', 'city', 'urban'),
(193, 'Charlottesville', 38.0293, -78.4767, 'Home of University of Virginia', 'city,university', 'urban'),
(193, 'Harrisonburg', 38.4496, -78.8689, 'Shenandoah Valley city', 'city', 'urban'),
(193, 'Charleston-Huntington', 38.3498, -81.6326, 'West Virginia capital region', 'city', 'urban'),
(193, 'Clarksburg-Weston', 39.2806, -80.3445, 'North central West Virginia', 'city', 'urban'),
(193, 'Wheeling-Steubenville', 40.0630, -80.7209, 'Northern panhandle of West Virginia', 'city', 'urban'),
(193, 'Bluefield-Beckley-Oak Hill', 37.2692, -81.2223, 'Southern West Virginia', 'city', 'urban'),
(193, 'Parkersburg', 39.2667, -81.5615, 'Western West Virginia', 'city', 'urban'),
(193, 'Charlotte', 35.2271, -80.8431, 'Largest North Carolina city', 'city', 'urban'),
(193, 'Raleigh-Durham (Fayetteville)', 35.7796, -78.6382, 'Research Triangle region', 'city,university', 'urban'),
(193, 'Greensboro-High Point-Winston-Salem', 36.0726, -79.7920, 'Piedmont Triad region', 'city', 'urban'),
(193, 'Greenville-Spartanburg-Asheville-Anderson', 34.8526, -82.3940, 'Upstate South Carolina/Western NC', 'city', 'urban'),
(193, 'Greenville-New Bern-Washington', 35.6127, -77.3663, 'Eastern North Carolina region', 'city,coastal', 'urban'),
(193, 'Wilmington NC', 34.2104, -77.8868, 'Coastal North Carolina city', 'city,coastal', 'urban'),
(193, 'Columbia SC', 34.0007, -81.0348, 'South Carolina capital', 'city', 'urban'),
(193, 'Charleston SC', 32.7765, -79.9311, 'Historic coastal city', 'city,historical,coastal', 'urban'),
(193, 'Myrtle Beach-Florence', 33.6891, -78.8867, 'Popular beach destination', 'beach,coastal', 'resort'),
(193, 'Greenwood-Greenville', 34.1854, -82.1618, 'Upstate South Carolina region', 'city', 'urban'),
(193, 'Atlanta', 33.7490, -84.3880, 'Georgia capital and largest city', 'city', 'urban'),
(193, 'Savannah', 32.0809, -81.0912, 'Historic coastal Georgia city', 'city,historical,coastal', 'urban'),
(193, 'Columbus GA', 32.4609, -84.9877, 'Western Georgia city', 'city', 'urban'),
(193, 'Augusta-Aiken', 33.4735, -82.0105, 'Georgia-South Carolina border region', 'city', 'urban'),
(193, 'Macon', 32.8407, -83.6324, 'Central Georgia city', 'city', 'urban'),
(193, 'Albany GA', 31.5785, -84.1557, 'Southwest Georgia city', 'city', 'urban'),
(193, 'Miami-Fort Lauderdale', 25.7617, -80.1918, 'Southeast Florida metro area', 'city,beach,coastal', 'urban'),
(193, 'Tampa-St. Petersburg (Sarasota)', 27.9506, -82.4572, 'West central Florida region', 'city,beach,coastal', 'urban'),
(193, 'Orlando-Daytona Beach-Melbourne', 28.5383, -81.3792, 'Central Florida tourist region', 'city,theme-parks', 'urban'),
(193, 'West Palm Beach-Fort Pierce', 26.7153, -80.0534, 'Southeast Florida coastal region', 'city,beach,coastal', 'urban'),
(193, 'Jacksonville', 30.3322, -81.6557, 'Northeast Florida city', 'city,coastal', 'urban'),
(193, 'Fort Myers-Naples', 26.6406, -81.8723, 'Southwest Florida coastal region', 'city,beach,coastal', 'urban'),
(193, 'Tallahassee-Thomasville', 30.4383, -84.2807, 'North Florida region', 'city', 'urban'),
(193, 'Gainesville', 29.6516, -82.3248, 'North central Florida city', 'city,university', 'urban'),
(193, 'Panama City', 30.1588, -85.6602, 'Northwest Florida beach destination', 'city,beach,coastal', 'urban'),
(193, 'Louisville', 38.2527, -85.7585, 'Kentucky''s largest city', 'city', 'urban'),
(193, 'Lexington', 38.0406, -84.5037, 'Kentucky horse country', 'city', 'urban'),
(193, 'Bowling Green', 36.9685, -86.4808, 'South central Kentucky city', 'city', 'urban'),
(193, 'Paducah-Cape Girardeau-Harrisburg', 37.0834, -88.6000, 'Western Kentucky region', 'city', 'urban'),
(193, 'Nashville', 36.1627, -86.7816, 'Tennessee capital and music city', 'city,music', 'urban'),
(193, 'Memphis', 35.1495, -90.0490, 'Western Tennessee city', 'city,music', 'urban'),
(193, 'Knoxville', 35.9606, -83.9207, 'Eastern Tennessee city', 'city', 'urban'),
(193, 'Chattanooga', 35.0456, -85.3097, 'Southeast Tennessee city', 'city', 'urban'),
(193, 'Tri-Cities TN-VA', 36.5484, -82.5618, 'Tennessee-Virginia border region', 'city', 'urban'),
(193, 'Jackson TN', 35.6145, -88.8139, 'West Tennessee city', 'city', 'urban'),
(193, 'Birmingham (Anniston and Tuscaloosa)', 33.5207, -86.8025, 'Alabama''s largest city', 'city', 'urban'),
(193, 'Mobile-Pensacola (Fort Walton Beach)', 30.6954, -88.0399, 'Gulf Coast region', 'city,beach,coastal', 'urban'),
(193, 'Huntsville-Decatur (Florence)', 34.7304, -86.5861, 'Northern Alabama region', 'city', 'urban'),
(193, 'Montgomery-Selma', 32.3668, -86.3000, 'Alabama capital region', 'city,historical', 'urban'),
(193, 'Dothan', 31.2232, -85.3905, 'Southeast Alabama city', 'city', 'urban'),
(193, 'Jackson MS', 32.2988, -90.1848, 'Mississippi capital', 'city', 'urban'),
(193, 'Columbus-Tupelo-West Point-Starkville', 33.4957, -88.4273, 'Northeast Mississippi region', 'city', 'urban'),
(193, 'Biloxi-Gulfport', 30.3960, -88.8853, 'Mississippi Gulf Coast', 'city,beach,coastal', 'urban'),
(193, 'Hattiesburg-Laurel', 31.3271, -89.2903, 'Southeast Mississippi region', 'city', 'urban'),
(193, 'Meridian', 32.3643, -88.7037, 'East central Mississippi city', 'city', 'urban'),
(193, 'Little Rock-Pine Bluff', 34.7465, -92.2896, 'Arkansas capital region', 'city', 'urban'),
(193, 'Fort Smith-Fayetteville-Springdale-Rogers', 35.3859, -94.3985, 'Northwest Arkansas region', 'city', 'urban'),
(193, 'Jonesboro', 35.8423, -90.7043, 'Northeast Arkansas city', 'city', 'urban'),
(193, 'Monroe-El Dorado', 32.5093, -92.1193, 'Arkansas-Louisiana border region', 'city', 'urban'),
(193, 'New Orleans', 29.9511, -90.0715, 'Historic Louisiana city', 'city,historical,coastal', 'urban'),
(193, 'Baton Rouge', 30.4515, -91.1871, 'Louisiana capital', 'city', 'urban'),
(193, 'Lafayette LA', 30.2241, -92.0198, 'South central Louisiana city', 'city', 'urban'),
(193, 'Shreveport-Texarkana', 32.5252, -93.7502, 'Northwest Louisiana region', 'city', 'urban'),
(193, 'Lake Charles', 30.2266, -93.2174, 'Southwest Louisiana city', 'city', 'urban'),
(193, 'Alexandria LA', 31.3113, -92.4451, 'Central Louisiana city', 'city', 'urban'),
(193, 'Oklahoma City', 35.4676, -97.5164, 'Oklahoma capital', 'city', 'urban'),
(193, 'Tulsa', 36.1540, -95.9928, 'Northeast Oklahoma city', 'city', 'urban'),
(193, 'Sherman-Ada', 33.6357, -96.6089, 'Oklahoma-Texas border region', 'city', 'urban'),
(193, 'Dallas-Fort Worth', 32.7767, -96.7970, 'North Texas metroplex', 'city', 'urban'),
(193, 'Houston', 29.7604, -95.3698, 'Largest Texas city', 'city', 'urban'),
(193, 'San Antonio', 29.4241, -98.4936, 'South central Texas city', 'city,historical', 'urban'),
(193, 'Austin TX', 30.2672, -97.7431, 'Texas capital', 'city,music', 'urban'),
(193, 'El Paso (Las Cruces)', 31.7619, -106.4850, 'West Texas city', 'city', 'urban'),
(193, 'Harlingen-Weslaco-Brownsville-McAllen', 26.1906, -97.6961, 'Rio Grande Valley region', 'city', 'urban'),
(193, 'Corpus Christi', 27.8006, -97.3964, 'South Texas coastal city', 'city,coastal', 'urban'),
(193, 'Waco-Temple-Bryan', 31.5493, -97.1467, 'Central Texas region', 'city', 'urban'),
(193, 'Beaumont-Port Arthur', 30.0802, -94.1266, 'Southeast Texas region', 'city', 'urban'),
(193, 'Tyler-Longview (Lufkin & Nacogdoches)', 32.3513, -95.3011, 'East Texas region', 'city', 'urban'),
(193, 'Amarillo', 35.2220, -101.8313, 'Texas Panhandle city', 'city', 'urban'),
(193, 'Lubbock', 33.5779, -101.8552, 'West Texas city', 'city', 'urban'),
(193, 'Odessa-Midland', 31.8457, -102.3676, 'West Texas oil region', 'city', 'urban'),
(193, 'Wichita Falls & Lawton', 33.9137, -98.4934, 'North Texas region', 'city', 'urban'),
(193, 'Abilene-Sweetwater', 32.4487, -99.7331, 'West central Texas region', 'city', 'urban'),
(193, 'San Angelo', 31.4638, -100.4370, 'West central Texas city', 'city', 'urban'),
(193, 'Laredo', 27.5306, -99.4803, 'South Texas border city', 'city', 'urban'),
(193, 'Victoria', 28.8053, -97.0036, 'South Texas city', 'city', 'urban'),
(193, 'Cleveland-Akron (Canton)', 41.4993, -81.6944, 'Northeast Ohio region', 'city', 'urban'),
(193, 'Columbus OH', 39.9612, -82.9988, 'Ohio capital', 'city', 'urban'),
(193, 'Cincinnati', 39.1031, -84.5120, 'Southwest Ohio city', 'city', 'urban'),
(193, 'Dayton', 39.7589, -84.1916, 'West central Ohio city', 'city', 'urban'),
(193, 'Toledo', 41.6639, -83.5552, 'Northwest Ohio city', 'city', 'urban'),
(193, 'Youngstown', 41.0998, -80.6495, 'Northeast Ohio city', 'city', 'urban'),
(193, 'Lima', 40.7426, -84.1052, 'West central Ohio city', 'city', 'urban'),
(193, 'Zanesville', 39.9406, -82.0132, 'East central Ohio city', 'city', 'urban'),
(193, 'Indianapolis', 39.7684, -86.1581, 'Indiana capital', 'city', 'urban'),
(193, 'Fort Wayne', 41.0793, -85.1394, 'Northeast Indiana city', 'city', 'urban'),
(193, 'South Bend-Elkhart', 41.6764, -86.2520, 'North central Indiana region', 'city', 'urban'),
(193, 'Evansville', 37.9716, -87.5711, 'Southwest Indiana city', 'city', 'urban'),
(193, 'Lafayette IN', 40.4167, -86.8753, 'West central Indiana city', 'city,university', 'urban'),
(193, 'Terre Haute', 39.4667, -87.4139, 'West central Indiana city', 'city', 'urban'),
(193, 'Chicago', 41.8781, -87.6298, 'Illinois'' largest city', 'city', 'urban'),
(193, 'Champaign-Urbana & Springfield-Decatur', 40.1164, -88.2434, 'Central Illinois region', 'city,university', 'urban'),
(193, 'Peoria-Bloomington', 40.6936, -89.5890, 'Central Illinois region', 'city', 'urban'),
(193, 'Rockford', 42.2711, -89.0937, 'Northern Illinois city', 'city', 'urban'),
(193, 'Quincy-Hannibal-Keokuk', 39.9356, -91.4099, 'Western Illinois region', 'city', 'urban'),
(193, 'Davenport-Rock Island-Moline', 41.5236, -90.5776, 'Quad Cities region', 'city', 'urban'),
(193, 'Detroit', 42.3314, -83.0458, 'Michigan''s largest city', 'city', 'urban'),
(193, 'Grand Rapids-Kalamazoo-Battle Creek', 42.9634, -85.6681, 'West Michigan region', 'city', 'urban'),
(193, 'Flint-Saginaw-Bay City', 43.0125, -83.6875, 'East central Michigan region', 'city', 'urban'),
(193, 'Lansing', 42.7325, -84.5555, 'Michigan capital', 'city', 'urban'),
(193, 'Traverse City-Cadillac', 44.7631, -85.6206, 'Northern Michigan region', 'city,lakeside', 'urban'),
(193, 'Marquette', 46.5435, -87.3954, 'Upper Peninsula city', 'city', 'urban'),
(193, 'Alpena', 45.0617, -83.4328, 'Northeast Michigan city', 'city', 'urban'),
(193, 'Milwaukee', 43.0389, -87.9065, 'Wisconsin''s largest city', 'city', 'urban'),
(193, 'Madison', 43.0731, -89.4012, 'Wisconsin capital', 'city', 'urban'),
(193, 'Green Bay-Appleton', 44.5133, -88.0133, 'Northeast Wisconsin region', 'city', 'urban'),
(193, 'La Crosse-Eau Claire', 43.8014, -91.2396, 'Western Wisconsin region', 'city', 'urban'),
(193, 'Wausau-Rhinelander', 44.9591, -89.6301, 'North central Wisconsin region', 'city', 'urban'),
(193, 'Duluth-Superior', 46.7867, -92.1005, 'Lake Superior port cities', 'city,lakeside', 'urban'),
(193, 'Minneapolis-St. Paul', 44.9778, -93.2650, 'Twin Cities metro area', 'city', 'urban'),
(193, 'Rochester-Mason City-Austin', 44.0121, -92.4802, 'Southern Minnesota region', 'city', 'urban'),
(193, 'Mankato', 44.1636, -93.9994, 'South central Minnesota city', 'city', 'urban'),
(193, 'Des Moines-Ames', 41.5868, -93.6250, 'Iowa capital region', 'city', 'urban'),
(193, 'Cedar Rapids-Waterloo-Iowa City & Dubuque', 41.9779, -91.6656, 'Eastern Iowa region', 'city', 'urban'),
(193, 'Sioux City', 42.4999, -96.4003, 'Western Iowa city', 'city', 'urban'),
(193, 'Ottumwa-Kirksville', 41.0125, -92.4149, 'Southern Iowa region', 'city', 'urban'),
(193, 'St. Louis', 38.6270, -90.1994, 'Missouri''s largest city', 'city', 'urban'),
(193, 'Kansas City', 39.0997, -94.5786, 'Western Missouri city', 'city', 'urban'),
(193, 'Springfield MO', 37.2090, -93.2923, 'Southwest Missouri city', 'city', 'urban'),
(193, 'Columbia-Jefferson City', 38.9517, -92.3341, 'Central Missouri region', 'city', 'urban'),
(193, 'Joplin-Pittsburg', 37.0842, -94.5133, 'Southwest Missouri region', 'city', 'urban'),
(193, 'St. Joseph', 39.7675, -94.8467, 'Northwest Missouri city', 'city', 'urban'),
(193, 'Fargo-Valley City', 46.8772, -96.7898, 'Eastern North Dakota region', 'city', 'urban'),
(193, 'Minot-Bismarck-Dickinson (Williston)', 46.8772, -96.7898, 'Western North Dakota region', 'city', 'urban'),
(193, 'Sioux Falls (Mitchell)', 43.5460, -96.7313, 'Largest South Dakota city', 'city', 'urban'),
(193, 'Rapid City', 44.0805, -103.2310, 'Western South Dakota city', 'city', 'urban'),
(193, 'Omaha', 41.2565, -95.9345, 'Nebraska''s largest city', 'city', 'urban'),
(193, 'Lincoln & Hastings-Kearney', 40.8136, -96.7026, 'Eastern Nebraska region', 'city', 'urban'),
(193, 'North Platte', 41.1239, -100.7654, 'Western Nebraska city', 'city', 'urban'),
(193, 'Cheyenne-Scottsbluff', 41.1400, -104.8202, 'Wyoming-Nebraska border region', 'city', 'urban'),
(193, 'Wichita-Hutchinson Plus', 37.6872, -97.3301, 'South central Kansas region', 'city', 'urban'),
(193, 'Topeka', 39.0558, -95.6890, 'Kansas capital', 'city', 'urban'),
(193, 'Phoenix (Prescott)', 33.4484, -112.0740, 'Arizona capital', 'city', 'urban'),
(193, 'Tucson (Sierra Vista)', 32.2226, -110.9747, 'Southern Arizona city', 'city', 'urban'),
(193, 'Yuma-El Centro', 32.6927, -114.6277, 'Southwest Arizona region', 'city', 'urban'),
(193, 'Albuquerque-Santa Fe', 35.0844, -106.6504, 'New Mexico''s largest city', 'city', 'urban'),
(193, 'Billings', 45.7833, -108.5007, 'Montana''s largest city', 'city', 'urban'),
(193, 'Missoula', 46.8721, -113.9940, 'Western Montana city', 'city', 'urban'),
(193, 'Great Falls', 47.4943, -111.2833, 'Central Montana city', 'city', 'urban'),
(193, 'Butte-Bozeman', 45.9839, -112.5001, 'Southwest Montana region', 'city', 'urban'),
(193, 'Helena', 46.5884, -112.0245, 'Montana capital', 'city', 'urban'),
(193, 'Glendive', 47.1056, -104.7125, 'Eastern Montana city', 'city', 'urban'),
(193, 'Boise', 43.6150, -116.2023, 'Idaho capital', 'city', 'urban'),
(193, 'Idaho Falls-Pocatello (Jackson)', 43.4917, -112.0339, 'Eastern Idaho region', 'city', 'urban'),
(193, 'Twin Falls', 42.5627, -114.4609, 'Southern Idaho city', 'city', 'urban'),
(193, 'Cheyenne-Scottsbluff', 41.1399, -104.8202, 'Wyoming capital', 'city', 'urban'),
(193, 'Casper-Riverton', 42.8666, -106.3131, 'Central Wyoming region', 'city', 'urban'),
(193, 'Denver', 39.7392, -104.9903, 'Colorado capital', 'city', 'urban'),
(193, 'Colorado Springs-Pueblo', 38.8339, -104.8214, 'Southern Colorado region', 'city', 'urban'),
(193, 'Grand Junction-Montrose', 39.0639, -108.5506, 'Western Colorado region', 'city', 'urban'),
(193, 'Las Vegas', 36.1699, -115.1398, 'Nevada''s largest city', 'city,entertainment', 'urban'),
(193, 'Reno', 39.5296, -119.8138, 'Northern Nevada city', 'city', 'urban'),
(193, 'Salt Lake City', 40.7608, -111.8910, 'Utah capital', 'city', 'urban'),
(193, 'Los Angeles', 34.0522, -118.2437, 'Southern California metro area', 'city,entertainment,coastal', 'urban'),
(193, 'San Francisco-Oakland-San Jose', 37.7749, -122.4194, 'Northern California metro area', 'city,coastal', 'urban'),
(193, 'San Diego', 32.7157, -117.1611, 'Southern California coastal city', 'city,coastal', 'urban'),
(193, 'Sacramento-Stockton-Modesto', 38.5816, -121.4944, 'Central California region', 'city', 'urban'),
(193, 'Fresno-Visalia', 36.7378, -119.7871, 'Central California region', 'city', 'urban'),
(193, 'Santa Barbara-Santa Maria-San Luis Obispo', 34.4208, -119.6982, 'Central California coast', 'city,coastal', 'urban'),
(193, 'Bakersfield', 35.3733, -119.0187, 'Southern California city', 'city', 'urban'),
(193, 'Monterey-Salinas', 36.6002, -121.8947, 'Central California coast', 'city,coastal', 'urban'),
(193, 'Palm Springs', 33.8303, -116.5453, 'Southern California resort area', 'resort', 'urban'),
(193, 'Chico-Redding', 39.7285, -121.8375, 'Northern California region', 'city', 'urban'),
(193, 'Eureka', 40.8021, -124.1637, 'Northern California coastal city', 'city,coastal', 'urban'),
(193, 'Portland OR', 45.5152, -122.6784, 'Oregon''s largest city', 'city', 'urban'),
(193, 'Eugene', 44.0521, -123.0868, 'Western Oregon city', 'city', 'urban'),
(193, 'Medford-Klamath Falls', 42.3265, -122.8756, 'Southern Oregon region', 'city', 'urban'),
(193, 'Bend OR', 44.0582, -121.3153, 'Central Oregon city', 'city', 'urban'),
(193, 'Seattle-Tacoma', 47.6062, -122.3321, 'Washington''s largest metro area', 'city,coastal', 'urban'),
(193, 'Spokane', 47.6588, -117.4260, 'Eastern Washington city', 'city', 'urban'),
(193, 'Yakima-Pasco-Richland-Kennewick', 46.6021, -120.5059, 'Central Washington region', 'city', 'urban'),
(193, 'Anchorage', 61.2181, -149.9003, 'Alaska''s largest city', 'city', 'urban'),
(193, 'Fairbanks', 64.8378, -147.7164, 'Interior Alaska city', 'city', 'urban'),
(193, 'Juneau', 58.3019, -134.4197, 'Alaska capital', 'city', 'urban'),
(193, 'Honolulu', 21.3069, -157.8583, 'Hawaii capital', 'city,beach,coastal', 'urban'),
(193, 'San Juan', 18.4655, -66.1057, 'Puerto Rico capital', 'city,beach,coastal', 'urban'),
(193, 'St. Thomas', 18.3358, -64.8964, 'US Virgin Islands main island', 'island,beach,coastal', 'resort'),
(193, 'Guam', 13.4443, 144.7937, 'Pacific island territory', 'island,beach,coastal', 'resort'),
(193, 'Pago Pago', -14.2710, -170.1322, 'American Samoa capital', 'island,beach,coastal', 'resort');

-- Canada Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(33, 'Vancouver', 49.2827, -123.1207, 'West coast Canadian city', 'city,coastal', 'urban'),
(33, 'Victoria', 48.4284, -123.3656, 'British Columbia capital', 'city,coastal', 'urban'),
(33, 'Whistler', 50.1163, -122.9574, 'Mountain resort town', 'mountain,ski', 'resort'),
(33, 'Kelowna', 49.8879, -119.4960, 'Okanagan Valley city', 'city,lakeside', 'urban'),
(33, 'Calgary', 51.0447, -114.0719, 'Alberta city near Rockies', 'city', 'urban'),
(33, 'Edmonton', 53.5461, -113.4938, 'Alberta capital', 'city', 'urban'),
(33, 'Banff', 51.1784, -115.5708, 'Rocky Mountain resort town', 'mountain,ski', 'resort'),
(33, 'Jasper', 52.8737, -118.0814, 'Rocky Mountain national park', 'mountain', 'nature'),
(33, 'Regina', 50.4452, -104.6189, 'Saskatchewan capital', 'city', 'urban'),
(33, 'Saskatoon', 52.1332, -106.6700, 'Saskatchewan''s largest city', 'city', 'urban'),
(33, 'Winnipeg', 49.8951, -97.1384, 'Manitoba capital', 'city', 'urban'),
(33, 'Churchill', 58.7684, -94.1650, 'Northern Manitoba polar bear destination', 'wildlife', 'nature'),
(33, 'Toronto', 43.6532, -79.3832, 'Ontario capital and largest city', 'city', 'urban'),
(33, 'Ottawa', 45.4215, -75.6972, 'Canada''s capital', 'city,capital', 'urban'),
(33, 'Niagara Falls', 43.0896, -79.0849, 'Famous waterfall destination', 'waterfall', 'nature'),
(33, 'Thunder Bay', 48.3824, -89.2461, 'Northwestern Ontario city', 'city', 'urban'),
(33, 'Montreal', 45.5017, -73.5673, 'Quebec''s largest city', 'city', 'urban'),
(33, 'Quebec City', 46.8139, -71.2080, 'Quebec capital', 'city,historical', 'urban'),
(33, 'Gatineau', 45.4765, -75.7013, 'Quebec city near Ottawa', 'city', 'urban'),
(33, 'Fredericton', 45.9636, -66.6431, 'New Brunswick capital', 'city', 'urban'),
(33, 'Saint John', 45.2733, -66.0633, 'New Brunswick port city', 'city,coastal', 'urban'),
(33, 'Moncton', 46.0878, -64.7782, 'New Brunswick city', 'city', 'urban'),
(33, 'Charlottetown', 46.2382, -63.1311, 'Prince Edward Island capital', 'city,coastal', 'urban'),
(33, 'Summerside', 46.3939, -63.7894, 'Prince Edward Island city', 'city,coastal', 'urban'),
(33, 'Halifax', 44.6488, -63.5752, 'Nova Scotia capital', 'city,coastal', 'urban'),
(33, 'Sydney', 46.1368, -60.1942, 'Nova Scotia city', 'city,coastal', 'urban'),
(33, 'Yarmouth', 43.8371, -66.1176, 'Nova Scotia coastal town', 'town,coastal', 'urban'),
(33, 'St. John''s', 47.5615, -52.7126, 'Newfoundland capital', 'city,coastal', 'urban'),
(33, 'Corner Brook', 48.9500, -57.9333, 'Newfoundland city', 'city', 'urban'),
(33, 'Whitehorse', 60.7212, -135.0568, 'Yukon capital', 'city', 'urban'),
(33, 'Dawson City', 64.0601, -139.4333, 'Historic Yukon gold rush town', 'town,historical', 'urban'),
(33, 'Yellowknife', 62.4540, -114.3718, 'Northwest Territories capital', 'city', 'urban'),
(33, 'Inuvik', 68.3617, -133.7305, 'Northwest Territories town', 'town', 'urban'),
(33, 'Iqaluit', 63.7467, -68.5170, 'Nunavut capital', 'city', 'urban'),
(33, 'Rankin Inlet', 62.8084, -92.0853, 'Nunavut community', 'town', 'urban');

-- Mexico Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(120, 'Tijuana', 32.5149, -117.0382, 'Border city in Baja California', 'city', 'urban'),
(120, 'Ensenada', 31.8616, -116.6057, 'Baja California coastal city', 'city,coastal', 'urban'),
(120, 'Cabo San Lucas', 22.8905, -109.9167, 'Baja California resort destination', 'beach,resort', 'resort'),
(120, 'La Paz', 24.1426, -110.3128, 'Baja California Sur capital', 'city,coastal', 'urban'),
(120, 'Monterrey', 25.6866, -100.3161, 'Northern Mexico''s largest city', 'city', 'urban'),
(120, 'Chihuahua', 28.6329, -106.0691, 'Northern Mexico city', 'city', 'urban'),
(120, 'Hermosillo', 29.0892, -110.9613, 'Sonora state capital', 'city', 'urban'),
(120, 'Mazatlán', 23.2494, -106.4111, 'Pacific coast resort city', 'city,beach,coastal', 'urban'),
(120, 'Puerto Vallarta', 20.6534, -105.2253, 'Pacific coast resort city', 'city,beach,coastal', 'urban'),
(120, 'Acapulco', 16.8531, -99.8237, 'Pacific coast resort city', 'city,beach,coastal', 'urban'),
(120, 'Zihuatanejo', 17.6434, -101.5521, 'Pacific coast resort town', 'town,beach,coastal', 'resort'),
(120, 'Mexico City', 19.4326, -99.1332, 'Mexico''s capital and largest city', 'city,capital', 'urban'),
(120, 'Guadalajara', 20.6597, -103.3496, 'Jalisco state capital', 'city', 'urban'),
(120, 'Guanajuato', 21.0190, -101.2574, 'Colonial city in central Mexico', 'city,historical', 'urban'),
(120, 'San Miguel de Allende', 20.9153, -100.7444, 'Colonial city in central Mexico', 'city,historical', 'urban'),
(120, 'Veracruz', 19.1738, -96.1342, 'Gulf coast port city', 'city,coastal', 'urban'),
(120, 'Tampico', 22.2551, -97.8686, 'Gulf coast city', 'city,coastal', 'urban'),
(120, 'Cancún', 21.1619, -86.8515, 'Yucatan Peninsula resort city', 'city,beach,coastal', 'resort'),
(120, 'Playa del Carmen', 20.6296, -87.0739, 'Yucatan Peninsula resort town', 'town,beach,coastal', 'resort'),
(120, 'Mérida', 20.9674, -89.5926, 'Yucatan state capital', 'city,historical', 'urban'),
(120, 'Tulum', 20.2114, -87.4654, 'Yucatan Peninsula beach and ruins', 'beach,historical', 'resort'),
(120, 'Oaxaca', 17.0732, -96.7266, 'Southern Mexico colonial city', 'city,historical', 'urban'),
(120, 'San Cristóbal de las Casas', 16.7369, -92.6376, 'Chiapas highland city', 'city', 'urban');

-- Caribbean Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(45, 'Havana', 23.1136, -82.3666, 'Cuba''s capital', 'city,historical,coastal', 'urban'),
(45, 'Varadero', 23.1394, -81.2860, 'Cuba''s beach resort area', 'beach,coastal', 'resort'),
(92, 'Kingston', 17.9714, -76.7922, 'Jamaica''s capital', 'city,coastal', 'urban'),
(92, 'Montego Bay', 18.4663, -77.9189, 'Jamaica''s tourist hub', 'city,beach,coastal', 'resort'),
(53, 'Santo Domingo', 18.4861, -69.9312, 'Dominican Republic capital', 'city,historical,coastal', 'urban'),
(53, 'Punta Cana', 18.5601, -68.3725, 'Dominican Republic resort area', 'beach,coastal', 'resort'),
(82, 'Port-au-Prince', 18.5944, -72.3074, 'Haiti''s capital', 'city', 'urban'),
(28, 'Bridgetown', 13.0975, -59.6165, 'Barbados capital', 'city,beach,coastal', 'urban'),
(185, 'Port of Spain', 10.6549, -61.5019, 'Trinidad and Tobago capital', 'city,coastal', 'urban'),
(1, 'Oranjestad', 12.5092, -70.0086, 'Aruba''s capital', 'city,beach,coastal', 'urban'),
(10, 'St. John''s', 17.1185, -61.8449, 'Antigua and Barbuda capital', 'city,beach,coastal', 'urban'),
(100, 'Basseterre', 17.3026, -62.7177, 'St. Kitts and Nevis capital', 'city,coastal', 'urban'),
(21, 'Nassau', 25.0343, -77.3963, 'Bahamas capital', 'city,beach,coastal', 'urban'),
(21, 'Freeport', 26.5333, -78.7000, 'Bahamas city', 'city,beach,coastal', 'urban'),
(25, 'Hamilton', 32.2949, -64.7834, 'Bermuda capital', 'city,beach,coastal', 'urban'),
(46, 'George Town', 19.2869, -81.3674, 'Cayman Islands capital', 'city,beach,coastal', 'urban'),
(107, 'Castries', 14.0101, -60.9875, 'St. Lucia capital', 'city,beach,coastal', 'urban'),
(74, 'St. George''s', 12.0561, -61.7486, 'Grenada capital', 'city,beach,coastal', 'urban'),
(195, 'Kingstown', 13.1600, -61.2248, 'St. Vincent and the Grenadines capital', 'city,beach,coastal', 'urban');

-- South America Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(196, 'Caracas', 10.4806, -66.9036, 'Venezuela''s capital', 'city', 'urban'),
(196, 'Margarita Island', 10.9856, -63.9469, 'Venezuelan island resort', 'island,beach,coastal', 'resort'),
(41, 'Bogotá', 4.7110, -74.0721, 'Colombia''s capital', 'city', 'urban'),
(41, 'Cartagena', 10.3910, -75.4794, 'Colombian coastal city', 'city,historical,coastal', 'urban'),
(41, 'Medellín', 6.2442, -75.5812, 'Colombian city', 'city', 'urban'),
(41, 'San Andrés', 12.5567, -81.7185, 'Colombian island', 'island,beach,coastal', 'resort'),
(78, 'Georgetown', 6.8013, -58.1553, 'Guyana''s capital', 'city,coastal', 'urban'),
(171, 'Paramaribo', 5.8520, -55.2038, 'Suriname''s capital', 'city,coastal', 'urban'),
(55, 'Quito', -0.1807, -78.4678, 'Ecuador''s capital', 'city,historical', 'urban'),
(55, 'Guayaquil', -2.1962, -79.8862, 'Ecuador''s largest city', 'city,coastal', 'urban'),
(55, 'Galápagos Islands', -0.9538, -90.9656, 'Ecuadorian archipelago', 'island,wildlife', 'nature'),
(145, 'Lima', -12.0464, -77.0428, 'Peru''s capital', 'city,coastal', 'urban'),
(145, 'Cusco', -13.5319, -71.9675, 'Gateway to Machu Picchu', 'city,historical', 'urban'),
(145, 'Machu Picchu', -13.1631, -72.5450, 'Inca ruins', 'historical', 'nature'),
(26, 'La Paz', -16.4897, -68.1193, 'Bolivia''s administrative capital', 'city', 'urban'),
(26, 'Sucre', -19.0196, -65.2620, 'Bolivia''s constitutional capital', 'city,historical', 'urban'),
(26, 'Uyuni Salt Flats', -20.1338, -67.4891, 'Bolivian salt desert', 'natural-wonder', 'nature'),
(35, 'Santiago', -33.4489, -70.6693, 'Chile''s capital', 'city', 'urban'),
(35, 'Valparaíso', -33.0472, -71.6127, 'Chilean coastal city', 'city,coastal', 'urban'),
(35, 'Atacama Desert', -23.8369, -69.1307, 'Driest desert in the world', 'desert', 'nature'),
(35, 'Patagonia', -51.6226, -72.3093, 'Southern Chile region', 'wilderness', 'nature'),
(7, 'Buenos Aires', -34.6037, -58.3816, 'Argentina''s capital', 'city', 'urban'),
(7, 'Mendoza', -32.8895, -68.8458, 'Argentine wine region', 'city,wine', 'urban'),
(7, 'Bariloche', -41.1335, -71.3103, 'Argentine lake district', 'city,lakeside', 'urban'),
(7, 'Iguazu Falls', -25.6953, -54.4367, 'Argentina-Brazil border waterfalls', 'waterfall', 'nature'),
(192, 'Montevideo', -34.9011, -56.1645, 'Uruguay''s capital', 'city,coastal', 'urban'),
(192, 'Punta del Este', -34.9608, -54.9444, 'Uruguayan beach resort', 'beach,coastal', 'resort'),
(153, 'Asunción', -25.2637, -57.5759, 'Paraguay''s capital', 'city', 'urban'),
(27, 'São Paulo', -23.5505, -46.6333, 'Brazil''s largest city', 'city', 'urban'),
(27, 'Rio de Janeiro', -22.9068, -43.1729, 'Brazil''s famous coastal city', 'city,beach,coastal', 'urban'),
(27, 'Belo Horizonte', -19.9167, -43.9345, 'Brazilian city', 'city', 'urban'),
(27, 'Salvador', -12.9714, -38.5014, 'Brazilian coastal city', 'city,historical,coastal', 'urban'),
(27, 'Recife', -8.0476, -34.8770, 'Brazilian coastal city', 'city,coastal', 'urban'),
(27, 'Manaus', -3.1190, -60.0217, 'Brazilian Amazon city', 'city', 'urban'),
(27, 'Brasília', -15.7942, -47.8822, 'Brazil''s capital', 'city,capital', 'urban'),
(27, 'Porto Alegre', -30.0346, -51.2177, 'Southern Brazilian city', 'city', 'urban');


-- Europe Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
-- Norway
(138, 'Oslo', 59.9139, 10.7522, 'Norway''s capital', 'city,coastal', 'urban'),
(138, 'Bergen', 60.3913, 5.3221, 'Norwegian coastal city', 'city,coastal', 'urban'),
(138, 'Trondheim', 63.4305, 10.3951, 'Norwegian historical city', 'city,historical', 'urban'),
(138, 'Tromsø', 69.6496, 18.9560, 'Arctic Norwegian city', 'city,arctic', 'urban'),
(138, 'Fjords region', 62.0, 7.0, 'Norwegian fjord landscape', 'nature,fjords', 'nature'),

-- Sweden
(174, 'Stockholm', 59.3293, 18.0686, 'Sweden''s capital', 'city,coastal', 'urban'),
(174, 'Gothenburg', 57.7089, 11.9746, 'Swedish coastal city', 'city,coastal', 'urban'),
(174, 'Malmö', 55.6049, 13.0038, 'Southern Swedish city', 'city,coastal', 'urban'),
(174, 'Lapland', 67.0, 20.0, 'Northern Swedish wilderness', 'wilderness,arctic', 'nature'),

-- Denmark
(52, 'Copenhagen', 55.6761, 12.5683, 'Denmark''s capital', 'city,coastal', 'urban'),
(52, 'Aarhus', 56.1629, 10.2039, 'Danish city', 'city,coastal', 'urban'),
(52, 'Odense', 55.4038, 10.4024, 'Danish city', 'city', 'urban'),

-- Finland
(61, 'Helsinki', 60.1699, 24.9384, 'Finland''s capital', 'city,coastal', 'urban'),
(61, 'Turku', 60.4518, 22.2666, 'Finnish coastal city', 'city,coastal', 'urban'),
(61, 'Rovaniemi', 66.5039, 25.7294, 'Arctic Finnish city', 'city,arctic', 'urban'),

-- Iceland
(89, 'Reykjavik', 64.1466, -21.9426, 'Iceland''s capital', 'city,coastal', 'urban'),
(89, 'Blue Lagoon', 63.8804, -22.4495, 'Geothermal spa', 'spa,geothermal', 'resort'),
(89, 'Ring Road destinations', 64.9, -19.0, 'Icelandic scenic route', 'nature,scenic-route', 'nature'),

-- Estonia
(59, 'Tallinn', 59.4370, 24.7536, 'Estonia''s capital', 'city,coastal', 'urban'),

-- Latvia
(113, 'Riga', 56.9496, 24.1052, 'Latvia''s capital', 'city,coastal', 'urban'),

-- Lithuania
(111, 'Vilnius', 54.6872, 25.2797, 'Lithuania''s capital', 'city', 'urban'),

-- United Kingdom
(66, 'London', 51.5074, -0.1278, 'UK capital', 'city', 'urban'),
(66, 'Manchester', 53.4808, -2.2426, 'UK city', 'city', 'urban'),
(66, 'Birmingham', 52.4862, -1.8904, 'UK city', 'city', 'urban'),
(66, 'Liverpool', 53.4084, -2.9916, 'UK city', 'city,coastal', 'urban'),
(66, 'Bath', 51.3813, -2.3640, 'UK historical city', 'city,historical', 'urban'),
(66, 'Oxford', 51.7520, -1.2577, 'UK university city', 'city,university', 'urban'),
(66, 'Cambridge', 52.2053, 0.1218, 'UK university city', 'city,university', 'urban'),
(66, 'Edinburgh', 55.9533, -3.1883, 'Scotland''s capital', 'city', 'urban'),
(66, 'Glasgow', 55.8642, -4.2518, 'Scottish city', 'city', 'urban'),
(66, 'Highlands', 57.5, -5.0, 'Scottish highland region', 'nature,highlands', 'nature'),
(66, 'Cardiff', 51.4816, -3.1791, 'Wales'' capital', 'city,coastal', 'urban'),
(66, 'Snowdonia', 53.0, -4.0, 'Welsh mountain region', 'nature,mountains', 'nature'),
(66, 'Belfast', 54.5973, -5.9301, 'Northern Ireland capital', 'city,coastal', 'urban'),
(66, 'Giant''s Causeway', 55.2408, -6.5116, 'Northern Irish natural wonder', 'nature,geological', 'nature'),

-- Ireland
(86, 'Dublin', 53.3498, -6.2603, 'Ireland''s capital', 'city,coastal', 'urban'),
(86, 'Cork', 51.8969, -8.4863, 'Irish city', 'city,coastal', 'urban'),
(86, 'Galway', 53.2707, -9.0568, 'Irish city', 'city,coastal', 'urban'),
(86, 'Ring of Kerry', 51.9, -9.8, 'Irish scenic route', 'nature,scenic-route', 'nature'),

-- France
(63, 'Paris', 48.8566, 2.3522, 'France''s capital', 'city', 'urban'),
(63, 'Lyon', 45.7640, 4.8357, 'French city', 'city', 'urban'),
(63, 'Marseille', 43.2965, 5.3698, 'French coastal city', 'city,coastal', 'urban'),
(63, 'Nice', 43.7102, 7.2620, 'French Riviera city', 'city,beach,coastal', 'urban'),
(63, 'Bordeaux', 44.8378, -0.5792, 'French wine city', 'city,wine', 'urban'),
(63, 'Loire Valley', 47.5, 1.0, 'French valley with castles', 'historical,castles', 'nature'),
(63, 'Normandy', 49.0, -1.0, 'French coastal region', 'historical,coastal', 'nature'),
(63, 'Brittany', 48.0, -3.0, 'French coastal region', 'coastal', 'nature'),
(63, 'French Alps', 45.5, 6.5, 'Mountainous region', 'mountains,ski', 'nature'),

-- Netherlands
(137, 'Amsterdam', 52.3676, 4.9041, 'Netherlands'' capital', 'city', 'urban'),
(137, 'Rotterdam', 51.9244, 4.4777, 'Dutch city', 'city,coastal', 'urban'),
(137, 'The Hague', 52.0705, 4.3007, 'Dutch city', 'city,coastal', 'urban'),
(137, 'Utrecht', 52.0907, 5.1214, 'Dutch city', 'city', 'urban'),

-- Belgium
(15, 'Brussels', 50.8503, 4.3517, 'Belgium''s capital', 'city', 'urban'),
(15, 'Bruges', 51.2093, 3.2247, 'Belgian historical city', 'city,historical', 'urban'),
(15, 'Antwerp', 51.2194, 4.4025, 'Belgian city', 'city', 'urban'),
(15, 'Ghent', 51.0543, 3.7174, 'Belgian city', 'city,historical', 'urban'),

-- Luxembourg
(112, 'Luxembourg City', 49.6116, 6.1319, 'Luxembourg''s capital', 'city', 'urban'),

-- Germany
(49, 'Berlin', 52.5200, 13.4050, 'Germany''s capital', 'city', 'urban'),
(49, 'Munich', 48.1351, 11.5820, 'German city', 'city', 'urban'),
(49, 'Frankfurt', 50.1109, 8.6821, 'German financial city', 'city', 'urban'),
(49, 'Hamburg', 53.5511, 9.9937, 'German port city', 'city,coastal', 'urban'),
(49, 'Cologne', 50.9375, 6.9603, 'German city', 'city', 'urban'),
(49, 'Dresden', 51.0504, 13.7373, 'German historical city', 'city,historical', 'urban'),
(49, 'Black Forest', 48.0, 8.0, 'German forest region', 'nature,forest', 'nature'),
(49, 'Romantic Road', 49.0, 10.0, 'German scenic route', 'historical,scenic-route', 'nature'),

-- Austria
(12, 'Vienna', 48.2082, 16.3738, 'Austria''s capital', 'city', 'urban'),
(12, 'Salzburg', 47.8095, 13.0550, 'Austrian city', 'city', 'urban'),
(12, 'Innsbruck', 47.2692, 11.4041, 'Austrian alpine city', 'city,mountains', 'urban'),
(12, 'Hallstatt', 47.5622, 13.6493, 'Austrian lakeside village', 'village,lakeside', 'urban'),

-- Switzerland
(34, 'Zurich', 47.3769, 8.5417, 'Swiss city', 'city,lakeside', 'urban'),
(34, 'Geneva', 46.2044, 6.1432, 'Swiss city', 'city,lakeside', 'urban'),
(34, 'Bern', 46.9480, 7.4474, 'Swiss capital', 'city', 'urban'),
(34, 'Lucerne', 47.0502, 8.3093, 'Swiss city', 'city,lakeside', 'urban'),
(34, 'Interlaken', 46.6863, 7.8632, 'Swiss mountain town', 'town,mountains', 'urban'),
(34, 'Zermatt', 46.0207, 7.7491, 'Swiss alpine resort', 'town,mountains,ski', 'resort'),

-- Poland
(149, 'Warsaw', 52.2297, 21.0122, 'Poland''s capital', 'city', 'urban'),
(149, 'Krakow', 50.0647, 19.9450, 'Polish historical city', 'city,historical', 'urban'),
(149, 'Gdansk', 54.3520, 18.6466, 'Polish coastal city', 'city,coastal', 'urban'),
(149, 'Wroclaw', 51.1079, 17.0385, 'Polish city', 'city', 'urban'),

-- Czech Republic
(48, 'Prague', 50.0755, 14.4378, 'Czech capital', 'city,historical', 'urban'),
(48, 'Český Krumlov', 48.8109, 14.3152, 'Czech historical town', 'town,historical', 'urban'),
(48, 'Brno', 49.1951, 16.6068, 'Czech city', 'city', 'urban'),

-- Slovakia
(172, 'Bratislava', 48.1486, 17.1077, 'Slovakia''s capital', 'city', 'urban'),
(172, 'Košice', 48.7164, 21.2611, 'Slovak city', 'city', 'urban'),

-- Hungary
(83, 'Budapest', 47.4979, 19.0402, 'Hungary''s capital', 'city', 'urban'),
(83, 'Debrecen', 47.5316, 21.6273, 'Hungarian city', 'city', 'urban'),

-- Russia
(157, 'Moscow', 55.7558, 37.6173, 'Russia''s capital', 'city', 'urban'),
(157, 'St. Petersburg', 59.9343, 30.3351, 'Russian cultural capital', 'city,historical', 'urban'),
(157, 'Golden Ring cities', 57.0, 40.0, 'Russian historical cities', 'historical', 'urban'),
(157, 'Trans-Siberian Railway cities', 55.0, 85.0, 'Cities along railway route', 'historical', 'urban'),

-- Ukraine
(191, 'Kyiv', 50.4501, 30.5234, 'Ukraine''s capital', 'city', 'urban'),
(191, 'Lviv', 49.8397, 24.0297, 'Ukrainian historical city', 'city,historical', 'urban'),
(191, 'Odessa', 46.4825, 30.7233, 'Ukrainian coastal city', 'city,coastal', 'urban'),

-- Belarus
(23, 'Minsk', 53.9045, 27.5615, 'Belarus'' capital', 'city', 'urban'),
(23, 'Brest', 52.0938, 23.6852, 'Belarusian city', 'city', 'urban'),

-- Romania
(156, 'Bucharest', 44.4268, 26.1025, 'Romania''s capital', 'city', 'urban'),
(156, 'Transylvania', 46.0, 25.0, 'Romanian historical region', 'historical', 'nature'),
(156, 'Black Sea Coast', 44.0, 28.0, 'Romanian coastal region', 'coastal', 'nature'),

-- Bulgaria
(19, 'Sofia', 42.6977, 23.3219, 'Bulgaria''s capital', 'city', 'urban'),
(19, 'Plovdiv', 42.1354, 24.7453, 'Bulgarian historical city', 'city,historical', 'urban'),
(19, 'Black Sea resorts', 42.5, 27.5, 'Bulgarian coastal resorts', 'beach,coastal', 'resort'),

-- Moldova
(117, 'Chișinău', 47.0105, 28.8638, 'Moldova''s capital', 'city', 'urban'),

-- Spain
(58, 'Madrid', 40.4168, -3.7038, 'Spain''s capital', 'city', 'urban'),
(58, 'Barcelona', 41.3851, 2.1734, 'Spanish coastal city', 'city,coastal', 'urban'),
(58, 'Seville', 37.3891, -5.9845, 'Spanish historical city', 'city,historical', 'urban'),
(58, 'Valencia', 39.4699, -0.3763, 'Spanish coastal city', 'city,coastal', 'urban'),
(58, 'Granada', 37.1773, -3.5986, 'Spanish historical city', 'city,historical', 'urban'),
(58, 'Bilbao', 43.2630, -2.9350, 'Spanish city', 'city,coastal', 'urban'),
(58, 'Balearic Islands', 39.5, 3.0, 'Spanish archipelago', 'island,beach,coastal', 'resort'),
(58, 'Canary Islands', 28.0, -15.5, 'Spanish archipelago', 'island,beach,coastal', 'resort'),

-- Portugal
(152, 'Lisbon', 38.7223, -9.1393, 'Portugal''s capital', 'city,coastal', 'urban'),
(152, 'Porto', 41.1579, -8.6291, 'Portuguese city', 'city,coastal', 'urban'),
(152, 'Algarve', 37.0, -8.0, 'Portuguese coastal region', 'beach,coastal', 'resort'),
(152, 'Madeira', 32.6669, -16.9241, 'Portuguese island', 'island,beach,coastal', 'resort'),
(152, 'Azores', 38.5, -28.0, 'Portuguese archipelago', 'island,volcanic', 'nature'),

-- Italy
(91, 'Rome', 41.9028, 12.4964, 'Italy''s capital', 'city,historical', 'urban'),
(91, 'Milan', 45.4642, 9.1900, 'Italian fashion capital', 'city', 'urban'),
(91, 'Venice', 45.4408, 12.3155, 'Italian canal city', 'city,historical,coastal', 'urban'),
(91, 'Florence', 43.7696, 11.2558, 'Italian Renaissance city', 'city,historical', 'urban'),
(91, 'Naples', 40.8518, 14.2681, 'Italian coastal city', 'city,coastal', 'urban'),
(91, 'Tuscany', 43.0, 11.0, 'Italian region', 'countryside,wine', 'nature'),
(91, 'Amalfi Coast', 40.6340, 14.6027, 'Italian coastal region', 'coastal,scenic', 'nature'),
(91, 'Sicily', 37.6, 14.0, 'Italian island', 'island,historical', 'nature'),
(91, 'Sardinia', 40.0, 9.0, 'Italian island', 'island,beach,coastal', 'resort'),

-- Greece
(73, 'Athens', 37.9838, 23.7275, 'Greece''s capital', 'city,historical,coastal', 'urban'),
(73, 'Thessaloniki', 40.6401, 22.9444, 'Greek city', 'city,coastal', 'urban'),
(73, 'Santorini', 36.3932, 25.4615, 'Greek island', 'island,beach,coastal', 'resort'),
(73, 'Mykonos', 37.4467, 25.3289, 'Greek island', 'island,beach,coastal', 'resort'),
(73, 'Crete', 35.2401, 24.8093, 'Greek island', 'island,beach,coastal', 'resort'),
(73, 'Rhodes', 36.4345, 28.2176, 'Greek island', 'island,beach,coastal', 'resort'),

-- Turkey (European part)
(187, 'Istanbul (European side)', 41.0082, 28.9784, 'European part of Istanbul', 'city,historical,coastal', 'urban'),

-- Malta
(124, 'Valletta', 35.8989, 14.5146, 'Malta''s capital', 'city,coastal', 'urban'),
(124, 'Gozo', 36.0443, 14.2512, 'Maltese island', 'island,beach,coastal', 'resort'),

-- Cyprus
(47, 'Nicosia', 35.1856, 33.3823, 'Cyprus'' capital', 'city', 'urban'),
(47, 'Limassol', 34.7071, 33.0226, 'Cypriot coastal city', 'city,coastal', 'urban'),

-- Croatia
(81, 'Zagreb', 45.8150, 15.9819, 'Croatia''s capital', 'city', 'urban'),
(81, 'Split', 43.5081, 16.4402, 'Croatian coastal city', 'city,coastal', 'urban'),
(81, 'Dubrovnik', 42.6507, 18.0944, 'Croatian coastal city', 'city,historical,coastal', 'urban'),
(81, 'Plitvice Lakes', 44.8654, 15.5820, 'Croatian national park', 'nature,lakes', 'nature'),

-- Slovenia
(173, 'Ljubljana', 46.0569, 14.5058, 'Slovenia''s capital', 'city', 'urban'),
(173, 'Lake Bled', 46.3690, 14.1136, 'Slovenian alpine lake', 'lake,mountains', 'nature'),

-- Bosnia and Herzegovina
(22, 'Sarajevo', 43.8563, 18.4131, 'Bosnia''s capital', 'city', 'urban'),
(22, 'Mostar', 43.3438, 17.8078, 'Bosnian historical city', 'city,historical', 'urban'),

-- Serbia
(168, 'Belgrade', 44.8206, 20.4622, 'Serbia''s capital', 'city', 'urban'),
(168, 'Novi Sad', 45.2671, 19.8335, 'Serbian city', 'city', 'urban'),

-- Montenegro
(126, 'Podgorica', 42.4304, 19.2594, 'Montenegro''s capital', 'city', 'urban'),
(126, 'Kotor', 42.4247, 18.7712, 'Montenegrin coastal town', 'town,historical,coastal', 'urban'),

-- North Macedonia
(122, 'Skopje', 41.9973, 21.4280, 'North Macedonia''s capital', 'city', 'urban'),
(122, 'Ohrid', 41.1231, 20.8016, 'Macedonian lakeside town', 'town,lakeside', 'urban'),

-- Albania
(4, 'Tirana', 41.3275, 19.8187, 'Albania''s capital', 'city', 'urban'),
(4, 'Albanian Riviera', 40.0, 19.8, 'Albanian coastal region', 'beach,coastal', 'nature'),

-- Kosovo
(201, 'Pristina', 42.6629, 21.1655, 'Kosovo''s capital', 'city', 'urban');

-- Africa Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
-- North Africa
-- Egypt
(56, 'Cairo', 30.0444, 31.2357, 'Egypt''s capital', 'city,historical', 'urban'),
(56, 'Luxor', 25.6872, 32.6396, 'Egyptian historical city', 'city,historical', 'urban'),
(56, 'Aswan', 24.0889, 32.8998, 'Egyptian city on the Nile', 'city,historical', 'urban'),
(56, 'Alexandria', 31.2001, 29.9187, 'Egyptian coastal city', 'city,historical,coastal', 'urban'),
(56, 'Red Sea resorts', 27.0, 34.0, 'Egyptian beach resorts', 'beach,coastal', 'resort'),

-- Libya
(106, 'Tripoli', 32.8872, 13.1913, 'Libya''s capital', 'city,coastal', 'urban'),
(106, 'Benghazi', 32.1167, 20.0667, 'Libyan city', 'city,coastal', 'urban'),

-- Tunisia
(186, 'Tunis', 36.8065, 10.1815, 'Tunisia''s capital', 'city,coastal', 'urban'),
(186, 'Carthage', 36.8545, 10.3306, 'Tunisian historical site', 'historical', 'nature'),
(186, 'Djerba', 33.8078, 10.8451, 'Tunisian island', 'island,beach,coastal', 'resort'),

-- Algeria
(54, 'Algiers', 36.7538, 3.0588, 'Algeria''s capital', 'city,coastal', 'urban'),
(54, 'Oran', 35.6971, -0.6337, 'Algerian coastal city', 'city,coastal', 'urban'),

-- Morocco
(115, 'Casablanca', 33.5731, -7.5898, 'Moroccan city', 'city,coastal', 'urban'),
(115, 'Marrakech', 31.6295, -7.9811, 'Moroccan historical city', 'city,historical', 'urban'),
(115, 'Fez', 34.0181, -5.0078, 'Moroccan historical city', 'city,historical', 'urban'),
(115, 'Rabat', 34.0209, -6.8416, 'Morocco''s capital', 'city,coastal', 'urban'),
(115, 'Chefchaouen', 35.1714, -5.2699, 'Moroccan blue city', 'town,historical', 'urban'),

-- Western Sahara
(115, 'Laayoune', 27.1536, -13.2033, 'Western Sahara city', 'city', 'urban'),

-- West Africa
-- Nigeria
(135, 'Lagos', 6.5244, 3.3792, 'Nigeria''s largest city', 'city,coastal', 'urban'),
(135, 'Abuja', 9.0579, 7.4951, 'Nigeria''s capital', 'city', 'urban'),
(135, 'Calabar', 4.9746, 8.3417, 'Nigerian coastal city', 'city,coastal', 'urban'),

-- Ghana
(68, 'Accra', 5.6037, -0.1870, 'Ghana''s capital', 'city,coastal', 'urban'),
(68, 'Kumasi', 6.6720, -1.5711, 'Ghanaian city', 'city', 'urban'),
(68, 'Cape Coast', 5.1315, -1.2795, 'Ghanaian coastal city', 'city,historical,coastal', 'urban'),

-- Senegal
(161, 'Dakar', 14.7167, -17.4677, 'Senegal''s capital', 'city,coastal', 'urban'),
(161, 'Saint-Louis', 16.0326, -16.4896, 'Senegalese historical city', 'city,historical,coastal', 'urban'),

-- Mali
(123, 'Bamako', 12.6392, -8.0029, 'Mali''s capital', 'city', 'urban'),
(123, 'Timbuktu', 16.7666, -3.0026, 'Malian historical city', 'city,historical', 'urban'),

-- Burkina Faso
(17, 'Ouagadougou', 12.3714, -1.5197, 'Burkina Faso''s capital', 'city', 'urban'),

-- Niger
(134, 'Niamey', 13.5136, 2.1098, 'Niger''s capital', 'city', 'urban'),

-- Benin
(16, 'Cotonou', 6.3725, 2.3617, 'Benin''s largest city', 'city,coastal', 'urban'),
(16, 'Porto-Novo', 6.4969, 2.6289, 'Benin''s capital', 'city', 'urban'),

-- Togo
(179, 'Lomé', 6.1304, 1.2158, 'Togo''s capital', 'city,coastal', 'urban'),

-- Ivory Coast
(37, 'Abidjan', 5.3599, -4.0083, 'Ivory Coast''s largest city', 'city,coastal', 'urban'),
(37, 'Yamoussoukro', 6.8276, -5.2893, 'Ivory Coast''s capital', 'city', 'urban'),

-- Guinea
(69, 'Conakry', 9.6412, -13.5784, 'Guinea''s capital', 'city,coastal', 'urban'),

-- Sierra Leone
(164, 'Freetown', 8.4840, -13.2299, 'Sierra Leone''s capital', 'city,coastal', 'urban'),

-- Liberia
(105, 'Monrovia', 6.3008, -10.7972, 'Liberia''s capital', 'city,coastal', 'urban'),

-- Mauritania
(129, 'Nouakchott', 18.0735, -15.9582, 'Mauritania''s capital', 'city,coastal', 'urban'),

-- Gambia
(70, 'Banjul', 13.4549, -16.5790, 'Gambia''s capital', 'city,coastal', 'urban'),

-- Guinea-Bissau
(71, 'Bissau', 11.8636, -15.5846, 'Guinea-Bissau''s capital', 'city,coastal', 'urban'),

-- Cape Verde
(43, 'Praia', 14.9330, -23.5133, 'Cape Verde''s capital', 'city,coastal', 'urban'),
(43, 'Mindelo', 16.8860, -24.9884, 'Cape Verdean city', 'city,coastal', 'urban'),

-- Central Africa
-- Democratic Republic of Congo
(39, 'Kinshasa', -4.4419, 15.2663, 'DRC''s capital', 'city', 'urban'),
(39, 'Lubumbashi', -11.6878, 27.5026, 'DRC city', 'city', 'urban'),

-- Cameroon
(38, 'Yaoundé', 3.8480, 11.5021, 'Cameroon''s capital', 'city', 'urban'),
(38, 'Douala', 4.0511, 9.7679, 'Cameroonian coastal city', 'city,coastal', 'urban'),

-- Central African Republic
(32, 'Bangui', 4.3947, 18.5582, 'CAR''s capital', 'city', 'urban'),

-- Chad
(178, 'N''Djamena', 12.1348, 15.0557, 'Chad''s capital', 'city', 'urban'),

-- Congo
(40, 'Brazzaville', -4.2634, 15.2429, 'Congo''s capital', 'city', 'urban'),

-- Gabon
(65, 'Libreville', 0.4162, 9.4673, 'Gabon''s capital', 'city,coastal', 'urban'),

-- Equatorial Guinea
(72, 'Malabo', 3.7504, 8.7371, 'Equatorial Guinea''s capital', 'city,coastal', 'urban'),

-- São Tomé and Príncipe
(170, 'São Tomé', 0.3302, 6.7333, 'São Tomé and Príncipe capital', 'city,coastal', 'urban'),

-- East Africa
-- Ethiopia
(60, 'Addis Ababa', 9.1450, 38.7648, 'Ethiopia''s capital', 'city', 'urban'),
(60, 'Lalibela', 12.0317, 39.0419, 'Ethiopian historical site', 'historical', 'nature'),
(60, 'Gondar', 12.6075, 37.4585, 'Ethiopian historical city', 'city,historical', 'urban'),

-- Kenya
(96, 'Nairobi', -1.2864, 36.8172, 'Kenya''s capital', 'city', 'urban'),
(96, 'Mombasa', -4.0435, 39.6682, 'Kenyan coastal city', 'city,coastal', 'urban'),
(96, 'Masai Mara', -1.5816, 35.2518, 'Kenyan wildlife reserve', 'wildlife,safari', 'nature'),

-- Tanzania
(189, 'Dar es Salaam', -6.7924, 39.2083, 'Tanzania''s largest city', 'city,coastal', 'urban'),
(189, 'Zanzibar', -6.1659, 39.2026, 'Tanzanian island', 'island,beach,coastal', 'resort'),
(189, 'Serengeti', -2.3333, 34.8333, 'Tanzanian national park', 'wildlife,safari', 'nature'),
(189, 'Kilimanjaro', -3.0674, 37.3556, 'Highest mountain in Africa', 'mountain', 'nature'),

-- Uganda
(190, 'Kampala', 0.3136, 32.5811, 'Uganda''s capital', 'city', 'urban'),
(190, 'Bwindi', -1.0574, 29.7195, 'Ugandan gorilla sanctuary', 'wildlife', 'nature'),

-- Rwanda
(158, 'Kigali', -1.9441, 30.0619, 'Rwanda''s capital', 'city', 'urban'),
(158, 'Volcanoes National Park', -1.4433, 29.5385, 'Rwandan gorilla sanctuary', 'wildlife', 'nature'),

-- Burundi
(14, 'Bujumbura', -3.3614, 29.3599, 'Burundi''s capital', 'city,lakeside', 'urban'),

-- Somalia
(167, 'Mogadishu', 2.0371, 45.3438, 'Somalia''s capital', 'city,coastal', 'urban'),

-- Djibouti
(50, 'Djibouti City', 11.5721, 43.1456, 'Djibouti''s capital', 'city,coastal', 'urban'),

-- Eritrea
(57, 'Asmara', 15.3229, 38.9251, 'Eritrea''s capital', 'city', 'urban'),

-- South Sudan
(169, 'Juba', 4.8594, 31.5713, 'South Sudan''s capital', 'city', 'urban'),

-- Sudan
(160, 'Khartoum', 15.5007, 32.5599, 'Sudan''s capital', 'city', 'urban'),

-- Southern Africa
-- South Africa
(203, 'Cape Town', -33.9249, 18.4241, 'South African coastal city', 'city,coastal', 'urban'),
(203, 'Johannesburg', -26.2041, 28.0473, 'South African city', 'city', 'urban'),
(203, 'Durban', -29.8587, 31.0218, 'South African coastal city', 'city,coastal', 'urban'),
(203, 'Kruger National Park', -23.9884, 31.5547, 'South African wildlife reserve', 'wildlife,safari', 'nature'),
(203, 'Garden Route', -34.0, 23.0, 'South African scenic route', 'coastal,scenic', 'nature'),

-- Namibia
(133, 'Windhoek', -22.5609, 17.0658, 'Namibia''s capital', 'city', 'urban'),
(133, 'Sossusvlei', -24.7333, 15.4167, 'Namibian desert dunes', 'desert', 'nature'),
(133, 'Etosha', -18.8556, 16.3294, 'Namibian national park', 'wildlife,safari', 'nature'),

-- Botswana
(31, 'Gaborone', -24.6282, 25.9231, 'Botswana''s capital', 'city', 'urban'),
(31, 'Okavango Delta', -19.2833, 22.9000, 'Botswanan inland delta', 'wildlife,safari', 'nature'),

-- Zimbabwe
(205, 'Harare', -17.8252, 31.0335, 'Zimbabwe''s capital', 'city', 'urban'),
(205, 'Victoria Falls', -17.9243, 25.8572, 'Zimbabwe-Zambia border waterfalls', 'waterfall', 'nature'),

-- Zambia
(204, 'Lusaka', -15.3875, 28.3228, 'Zambia''s capital', 'city', 'urban'),
(204, 'Livingstone', -17.8531, 25.8615, 'Zambian city near Victoria Falls', 'city', 'urban'),

-- Mozambique
(128, 'Maputo', -25.9692, 32.5732, 'Mozambique''s capital', 'city,coastal', 'urban'),
(128, 'Bazaruto Archipelago', -21.6333, 35.4833, 'Mozambican islands', 'island,beach,coastal', 'resort'),

-- Angola
(3, 'Luanda', -8.8390, 13.2894, 'Angola''s capital', 'city,coastal', 'urban'),

-- Malawi
(131, 'Lilongwe', -13.9626, 33.7741, 'Malawi''s capital', 'city', 'urban'),
(131, 'Lake Malawi', -12.0, 34.0, 'African Great Lake', 'lake', 'nature'),

-- Madagascar
(118, 'Antananarivo', -18.8792, 47.5079, 'Madagascar''s capital', 'city', 'urban'),
(118, 'Nosy Be', -13.3422, 48.2598, 'Madagascan island', 'island,beach,coastal', 'resort'),

-- Mauritius
(130, 'Port Louis', -20.1609, 57.5012, 'Mauritius'' capital', 'city,coastal', 'urban'),
(130, 'Beach resorts', -20.2, 57.5, 'Mauritian beach resorts', 'beach,coastal', 'resort'),

-- Seychelles
(176, 'Victoria', -4.6204, 55.4550, 'Seychelles'' capital', 'city,coastal', 'urban'),
(176, 'Island resorts', -4.6, 55.5, 'Seychellois island resorts', 'island,beach,coastal', 'resort'),

-- Comoros
(42, 'Moroni', -11.7172, 43.2473, 'Comoros'' capital', 'city,coastal', 'urban'),

-- Eswatini
(175, 'Mbabane', -26.3054, 31.1367, 'Eswatini''s capital', 'city', 'urban'),

-- Lesotho
(110, 'Maseru', -29.3101, 27.4786, 'Lesotho''s capital', 'city', 'urban');

-- Asia Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
-- East Asia
-- China
(36, 'Beijing', 39.9042, 116.4074, 'China''s capital', 'city,historical', 'urban'),
(36, 'Shanghai', 31.2304, 121.4737, 'China''s largest city', 'city,coastal', 'urban'),
(36, 'Hong Kong', 22.3193, 114.1694, 'Chinese special administrative region', 'city,coastal', 'urban'),
(36, 'Guangzhou', 23.1291, 113.2644, 'Chinese city', 'city', 'urban'),
(36, 'Xi''an', 34.3416, 108.9398, 'Chinese historical city', 'city,historical', 'urban'),
(36, 'Chengdu', 30.5728, 104.0668, 'Chinese city', 'city', 'urban'),
(36, 'Guilin', 25.2345, 110.1799, 'Chinese scenic city', 'city,scenic', 'urban'),
(36, 'Tibet (Lhasa)', 29.6548, 91.1406, 'Tibetan autonomous region', 'historical', 'nature'),

-- Japan
(94, 'Tokyo', 35.6762, 139.6503, 'Japan''s capital', 'city', 'urban'),
(94, 'Osaka', 34.6937, 135.5023, 'Japanese city', 'city,coastal', 'urban'),
(94, 'Kyoto', 35.0116, 135.7681, 'Japanese historical city', 'city,historical', 'urban'),
(94, 'Hiroshima', 34.3853, 132.4553, 'Japanese city', 'city,coastal', 'urban'),
(94, 'Sapporo', 43.0618, 141.3545, 'Japanese city', 'city', 'urban'),
(94, 'Okinawa', 26.2124, 127.6809, 'Japanese island', 'island,beach,coastal', 'resort'),

-- South Korea
(101, 'Seoul', 37.5665, 126.9780, 'South Korea''s capital', 'city', 'urban'),
(101, 'Busan', 35.1796, 129.0756, 'South Korean coastal city', 'city,coastal', 'urban'),
(101, 'Jeju Island', 33.4996, 126.5312, 'South Korean island', 'island,beach,coastal', 'resort'),

-- North Korea
(151, 'Pyongyang', 39.0392, 125.7625, 'North Korea''s capital', 'city', 'urban'),

-- Mongolia
(127, 'Ulaanbaatar', 47.8864, 106.9057, 'Mongolia''s capital', 'city', 'urban'),
(127, 'Gobi Desert', 43.5, 103.0, 'Mongolian desert', 'desert', 'nature'),

-- Taiwan
(36, 'Taipei', 25.0330, 121.5654, 'Taiwan''s capital', 'city', 'urban'),
(36, 'Kaohsiung', 22.6273, 120.3014, 'Taiwanese city', 'city,coastal', 'urban'),
(36, 'Taroko Gorge', 24.1589, 121.6016, 'Taiwanese scenic area', 'nature,canyon', 'nature'),

-- Southeast Asia
-- Thailand
(180, 'Bangkok', 13.7563, 100.5018, 'Thailand''s capital', 'city', 'urban'),
(180, 'Chiang Mai', 18.7061, 98.9817, 'Northern Thai city', 'city', 'urban'),
(180, 'Phuket', 7.8804, 98.3923, 'Thai island', 'island,beach,coastal', 'resort'),
(180, 'Pattaya', 12.9236, 100.8825, 'Thai beach city', 'city,beach,coastal', 'resort'),
(180, 'Koh Samui', 9.5120, 99.9986, 'Thai island', 'island,beach,coastal', 'resort'),

-- Vietnam
(198, 'Hanoi', 21.0278, 105.8342, 'Vietnam''s capital', 'city', 'urban'),
(198, 'Ho Chi Minh City', 10.8231, 106.6297, 'Vietnam''s largest city', 'city', 'urban'),
(198, 'Ha Long Bay', 20.9101, 107.1839, 'Vietnamese scenic bay', 'nature,coastal', 'nature'),
(198, 'Hoi An', 15.8801, 108.3380, 'Vietnamese historical town', 'town,historical,coastal', 'urban'),
(198, 'Da Nang', 16.0544, 108.2022, 'Vietnamese coastal city', 'city,coastal', 'urban'),

-- Cambodia
(98, 'Phnom Penh', 11.5564, 104.9282, 'Cambodia''s capital', 'city', 'urban'),
(98, 'Siem Reap', 13.3671, 103.8448, 'Gateway to Angkor Wat', 'city,historical', 'urban'),

-- Laos
(103, 'Vientiane', 17.9757, 102.6331, 'Laos'' capital', 'city', 'urban'),
(103, 'Luang Prabang', 19.8834, 102.1347, 'Laotian historical city', 'city,historical', 'urban'),

-- Myanmar
(125, 'Yangon', 16.8409, 96.1735, 'Myanmar''s largest city', 'city', 'urban'),
(125, 'Bagan', 21.1722, 94.8601, 'Myanmar historical site', 'historical', 'nature'),
(125, 'Mandalay', 21.9588, 96.0891, 'Myanmar city', 'city', 'urban'),

-- Malaysia
(132, 'Kuala Lumpur', 3.1390, 101.6869, 'Malaysia''s capital', 'city', 'urban'),
(132, 'Penang', 5.4164, 100.3327, 'Malaysian island', 'island,coastal', 'resort'),
(132, 'Langkawi', 6.3500, 99.8000, 'Malaysian archipelago', 'island,beach,coastal', 'resort'),
(132, 'Borneo (Sabah Sarawak)', 4.0, 114.0, 'Malaysian part of Borneo', 'island,wildlife', 'nature'),

-- Singapore
(162, 'Singapore', 1.3521, 103.8198, 'City-state', 'city,coastal', 'urban'),

-- Indonesia
(84, 'Jakarta', -6.2088, 106.8456, 'Indonesia''s capital', 'city,coastal', 'urban'),
(84, 'Bali', -8.3405, 115.0920, 'Indonesian island', 'island,beach,coastal', 'resort'),
(84, 'Yogyakarta', -7.7956, 110.3695, 'Indonesian cultural city', 'city,historical', 'urban'),
(84, 'Sumatra', -0.5897, 101.3431, 'Indonesian island', 'island,wildlife', 'nature'),
(84, 'Sulawesi', -2.1333, 120.2667, 'Indonesian island', 'island,wildlife', 'nature'),

-- Philippines
(146, 'Manila', 14.5995, 120.9842, 'Philippines'' capital', 'city,coastal', 'urban'),
(146, 'Cebu', 10.3157, 123.8854, 'Philippine island city', 'city,coastal', 'urban'),
(146, 'Boracay', 11.9674, 121.9248, 'Philippine island', 'island,beach,coastal', 'resort'),
(146, 'Palawan', 10.0, 118.8, 'Philippine island', 'island,beach,coastal', 'resort'),

-- Brunei
(29, 'Bandar Seri Begawan', 4.9031, 114.9398, 'Brunei''s capital', 'city,coastal', 'urban'),

-- East Timor
(183, 'Dili', -8.5569, 125.5603, 'East Timor''s capital', 'city,coastal', 'urban'),

-- South Asia
-- India
(85, 'Delhi', 28.7041, 77.1025, 'India''s capital', 'city', 'urban'),
(85, 'Mumbai', 19.0760, 72.8777, 'India''s financial capital', 'city,coastal', 'urban'),
(85, 'Bangalore', 12.9716, 77.5946, 'Indian tech city', 'city', 'urban'),
(85, 'Kolkata', 22.5726, 88.3639, 'Indian city', 'city', 'urban'),
(85, 'Chennai', 13.0827, 80.2707, 'Indian coastal city', 'city,coastal', 'urban'),
(85, 'Goa', 15.2993, 74.1240, 'Indian beach state', 'beach,coastal', 'resort'),
(85, 'Kerala', 10.0, 76.5, 'Indian coastal state', 'beach,coastal', 'nature'),
(85, 'Rajasthan (Jaipur Udaipur)', 26.0, 74.0, 'Indian historical region', 'historical', 'nature'),
(85, 'Agra (Taj Mahal)', 27.1767, 78.0081, 'Indian historical city', 'city,historical', 'urban'),
(85, 'Varanasi', 25.3176, 82.9739, 'Indian holy city', 'city,religious', 'urban'),

-- Pakistan
(143, 'Islamabad', 33.6844, 73.0479, 'Pakistan''s capital', 'city', 'urban'),
(143, 'Karachi', 24.8607, 67.0011, 'Pakistan''s largest city', 'city,coastal', 'urban'),
(143, 'Lahore', 31.5204, 74.3587, 'Pakistani city', 'city', 'urban'),

-- Bangladesh
(18, 'Dhaka', 23.8103, 90.4125, 'Bangladesh''s capital', 'city', 'urban'),
(18, 'Chittagong', 22.3569, 91.7832, 'Bangladeshi coastal city', 'city,coastal', 'urban'),

-- Sri Lanka
(109, 'Colombo', 6.9271, 79.8612, 'Sri Lanka''s commercial capital', 'city,coastal', 'urban'),
(109, 'Kandy', 7.2906, 80.6337, 'Sri Lankan cultural city', 'city', 'urban'),
(109, 'Galle', 6.0535, 80.2210, 'Sri Lankan coastal city', 'city,historical,coastal', 'urban'),

-- Nepal
(139, 'Kathmandu', 27.7172, 85.3240, 'Nepal''s capital', 'city', 'urban'),
(139, 'Pokhara', 28.2096, 83.9856, 'Nepalese lakeside city', 'city,lakeside', 'urban'),
(139, 'Everest region', 27.9881, 86.9250, 'Mount Everest area', 'mountains', 'nature'),

-- Bhutan
(30, 'Thimphu', 27.4728, 89.6390, 'Bhutan''s capital', 'city', 'urban'),
(30, 'Paro', 27.4333, 89.4167, 'Bhutanese city', 'city', 'urban'),

-- Maldives
(119, 'Malé', 4.1755, 73.5093, 'Maldives'' capital', 'city,coastal', 'urban'),
(119, 'Resort islands', 4.0, 73.0, 'Maldives resort islands', 'island,beach,coastal', 'resort'),

-- Central Asia
-- Kazakhstan
(95, 'Nur-Sultan (Astana)', 51.1605, 71.4704, 'Kazakhstan''s capital', 'city', 'urban'),
(95, 'Almaty', 43.2220, 76.8512, 'Kazakhstan''s largest city', 'city', 'urban'),

-- Uzbekistan
(194, 'Tashkent', 41.2995, 69.2401, 'Uzbekistan''s capital', 'city', 'urban'),
(194, 'Samarkand', 39.6270, 66.9750, 'Uzbek historical city', 'city,historical', 'urban'),
(194, 'Bukhara', 39.7681, 64.4556, 'Uzbek historical city', 'city,historical', 'urban'),

-- Turkmenistan
(182, 'Ashgabat', 37.9601, 58.3261, 'Turkmenistan''s capital', 'city', 'urban'),

-- Kyrgyzstan
(97, 'Bishkek', 42.8746, 74.5698, 'Kyrgyzstan''s capital', 'city', 'urban'),
(97, 'Issyk-Kul', 42.5, 77.5, 'Kyrgyz lake', 'lake', 'nature'),

-- Tajikistan
(181, 'Dushanbe', 38.5598, 68.7870, 'Tajikistan''s capital', 'city', 'urban'),

-- Afghanistan
(2, 'Kabul', 34.5553, 69.2075, 'Afghanistan''s capital', 'city', 'urban'),

-- Western Asia (Middle East)
-- Turkey
(187, 'Istanbul', 41.0082, 28.9784, 'Turkish city spanning two continents', 'city,historical,coastal', 'urban'),
(187, 'Ankara', 39.9334, 32.8597, 'Turkey''s capital', 'city', 'urban'),
(187, 'Cappadocia', 38.6433, 34.8309, 'Turkish historical region', 'historical', 'nature'),
(187, 'Antalya', 36.8969, 30.7133, 'Turkish coastal city', 'city,beach,coastal', 'urban'),
(187, 'Ephesus', 37.9397, 27.3406, 'Turkish historical site', 'historical', 'nature'),

-- Iran
(87, 'Tehran', 35.6892, 51.3890, 'Iran''s capital', 'city', 'urban'),
(87, 'Isfahan', 32.6546, 51.6680, 'Iranian historical city', 'city,historical', 'urban'),
(87, 'Shiraz', 29.5918, 52.5837, 'Iranian city', 'city', 'urban'),
(87, 'Persepolis', 29.9355, 52.8916, 'Iranian historical site', 'historical', 'nature'),

-- Iraq
(88, 'Baghdad', 33.3152, 44.3661, 'Iraq''s capital', 'city', 'urban'),
(88, 'Erbil', 36.1901, 44.0089, 'Iraqi city', 'city', 'urban'),

-- Syria
(177, 'Damascus', 33.5138, 36.2765, 'Syria''s capital', 'city,historical', 'urban'),
(177, 'Aleppo', 36.2021, 37.1343, 'Syrian historical city', 'city,historical', 'urban'),

-- Lebanon
(104, 'Beirut', 33.8938, 35.5018, 'Lebanon''s capital', 'city,coastal', 'urban'),
(104, 'Baalbek', 34.0058, 36.2181, 'Lebanese historical site', 'historical', 'nature'),

-- Israel
(90, 'Jerusalem', 31.7683, 35.2137, 'Holy city', 'city,historical', 'urban'),
(90, 'Tel Aviv', 32.0853, 34.7818, 'Israeli coastal city', 'city,beach,coastal', 'urban'),
(90, 'Dead Sea', 31.5, 35.5, 'Salt lake bordering Israel', 'lake', 'nature'),
(90, 'Eilat', 29.5577, 34.9519, 'Israeli resort city', 'city,beach,coastal', 'resort'),

-- Palestine
(154, 'Bethlehem', 31.7054, 35.2024, 'Palestinian city', 'city,religious', 'urban'),
(154, 'Ramallah', 31.9074, 35.1884, 'Palestinian city', 'city', 'urban'),

-- Jordan
(93, 'Amman', 31.9454, 35.9284, 'Jordan''s capital', 'city', 'urban'),
(93, 'Petra', 30.3285, 35.4444, 'Jordanian historical city', 'historical', 'nature'),
(93, 'Wadi Rum', 29.5833, 35.4167, 'Jordanian desert valley', 'desert', 'nature'),

-- Saudi Arabia
(159, 'Riyadh', 24.7136, 46.6753, 'Saudi Arabia''s capital', 'city', 'urban'),
(159, 'Jeddah', 21.5433, 39.1728, 'Saudi coastal city', 'city,coastal', 'urban'),
(159, 'Mecca', 21.3891, 39.8579, 'Saudi holy city', 'city,religious', 'urban'),
(159, 'Medina', 24.5247, 39.5692, 'Saudi holy city', 'city,religious', 'urban'),

-- Yemen
(202, 'Sana''a', 15.3694, 44.1910, 'Yemen''s capital', 'city', 'urban'),
(202, 'Aden', 12.7855, 45.0187, 'Yemeni coastal city', 'city,coastal', 'urban'),

-- Oman
(142, 'Muscat', 23.5859, 58.4059, 'Oman''s capital', 'city,coastal', 'urban'),
(142, 'Salalah', 17.0151, 54.0924, 'Omani coastal city', 'city,coastal', 'urban'),

-- United Arab Emirates
(6, 'Dubai', 25.2048, 55.2708, 'UAE city', 'city,coastal', 'urban'),
(6, 'Abu Dhabi', 24.4539, 54.3773, 'UAE''s capital', 'city,coastal', 'urban'),
(6, 'Sharjah', 25.3463, 55.4209, 'UAE city', 'city,coastal', 'urban'),

-- Qatar
(155, 'Doha', 25.2769, 51.5200, 'Qatar''s capital', 'city,coastal', 'urban'),

-- Bahrain
(20, 'Manama', 26.2285, 50.5860, 'Bahrain''s capital', 'city,coastal', 'urban'),

-- Kuwait
(102, 'Kuwait City', 29.3759, 47.9774, 'Kuwait''s capital', 'city,coastal', 'urban'),

-- Armenia
(8, 'Yerevan', 40.1792, 44.4991, 'Armenia''s capital', 'city', 'urban'),

-- Georgia
(67, 'Tbilisi', 41.7151, 44.8271, 'Georgia''s capital', 'city', 'urban'),
(67, 'Batumi', 41.6458, 41.6417, 'Georgian coastal city', 'city,coastal', 'urban'),

-- Azerbaijan
(13, 'Baku', 40.4093, 49.8671, 'Azerbaijan''s capital', 'city,coastal', 'urban');

-- Oceania Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
-- Australia
(11, 'Sydney', -33.8688, 151.2093, 'Australian city', 'city,coastal', 'urban'),
(11, 'Melbourne', -37.8136, 144.9631, 'Australian city', 'city,coastal', 'urban'),
(11, 'Brisbane', -27.4698, 153.0251, 'Australian city', 'city,coastal', 'urban'),
(11, 'Perth', -31.9505, 115.8605, 'Australian city', 'city,coastal', 'urban'),
(11, 'Adelaide', -34.9285, 138.6007, 'Australian city', 'city,coastal', 'urban'),
(11, 'Hobart', -42.8821, 147.3272, 'Australian city', 'city,coastal', 'urban'),
(11, 'Darwin', -12.4634, 130.8456, 'Australian city', 'city,coastal', 'urban'),
(11, 'Canberra', -35.2809, 149.1300, 'Australia''s capital', 'city', 'urban'),
(11, 'Blue Mountains', -33.7, 150.3, 'Australian mountain region', 'mountains', 'nature'),
(11, 'Byron Bay', -28.6474, 153.6020, 'Australian coastal town', 'town,beach,coastal', 'urban'),
(11, 'Hunter Valley', -32.9271, 151.4765, 'Australian wine region', 'wine', 'nature'),
(11, 'Great Ocean Road', -38.6806, 143.3923, 'Australian scenic route', 'coastal,scenic', 'nature'),
(11, 'Phillip Island', -38.4833, 145.2333, 'Australian island', 'island,wildlife', 'nature'),
(11, 'Gold Coast', -28.0167, 153.4000, 'Australian beach city', 'city,beach,coastal', 'resort'),
(11, 'Cairns', -16.9203, 145.7710, 'Australian gateway to the Great Barrier Reef', 'city,coastal', 'urban'),
(11, 'Great Barrier Reef', -18.0, 147.0, 'World''s largest coral reef system', 'reef,marine-life', 'nature'),
(11, 'Whitsundays', -20.2833, 148.9167, 'Australian archipelago', 'island,beach,coastal', 'resort'),
(11, 'Margaret River', -33.9550, 115.0750, 'Australian wine region', 'wine', 'nature'),
(11, 'Broome', -17.9618, 122.2362, 'Australian coastal town', 'town,beach,coastal', 'urban'),
(11, 'Kangaroo Island', -35.8376, 137.2639, 'Australian island', 'island,wildlife', 'nature'),
(11, 'Barossa Valley', -34.5417, 138.9617, 'Australian wine region', 'wine', 'nature'),
(11, 'Launceston', -41.4332, 147.1441, 'Australian city', 'city', 'urban'),
(11, 'Cradle Mountain', -41.6833, 145.9500, 'Australian mountain', 'mountain', 'nature'),
(11, 'Alice Springs', -23.6980, 133.8807, 'Australian outback town', 'town,desert', 'urban'),
(11, 'Uluru', -25.3444, 131.0369, 'Australian sandstone monolith', 'desert,geological', 'nature'),

-- New Zealand
(141, 'Auckland', -36.8485, 174.7633, 'New Zealand''s largest city', 'city,coastal', 'urban'),
(141, 'Wellington', -41.2865, 174.7762, 'New Zealand''s capital', 'city,coastal', 'urban'),
(141, 'Christchurch', -43.5321, 172.6362, 'New Zealand city', 'city,coastal', 'urban'),
(141, 'Queenstown', -45.0312, 168.6626, 'New Zealand resort town', 'town,lakeside', 'resort'),
(141, 'Rotorua', -38.1368, 176.2497, 'New Zealand geothermal city', 'city,geothermal', 'urban'),
(141, 'Bay of Islands', -35.2167, 174.1667, 'New Zealand archipelago', 'island,beach,coastal', 'resort'),
(141, 'Milford Sound', -44.6414, 167.8958, 'New Zealand fjord', 'fjord', 'nature'),
(141, 'Franz Josef Glacier', -43.3880, 170.1817, 'New Zealand glacier', 'glacier', 'nature'),

-- Pacific Islands
-- Papua New Guinea
(148, 'Port Moresby', -9.4438, 147.1803, 'Papua New Guinea''s capital', 'city,coastal', 'urban'),

-- Fiji
(62, 'Suva', -18.1248, 178.4501, 'Fiji''s capital', 'city,coastal', 'urban'),
(62, 'Nadi', -17.8, 177.4167, 'Fijian city', 'city,coastal', 'urban'),

-- Solomon Islands
(163, 'Honiara', -9.4456, 159.9729, 'Solomon Islands'' capital', 'city,coastal', 'urban'),

-- Vanuatu
(199, 'Port Vila', -17.7333, 168.3273, 'Vanuatu''s capital', 'city,coastal', 'urban'),

-- New Caledonia
(63, 'Nouméa', -22.2558, 166.4505, 'New Caledonia''s capital', 'city,coastal', 'urban'),

-- Palau
(147, 'Koror', 7.3435, 134.4786, 'Palau''s largest city', 'city,coastal', 'urban'),

-- Federated States of Micronesia
(64, 'Palikir', 6.9147, 158.1610, 'Micronesia''s capital', 'city', 'urban'),

-- Marshall Islands
(121, 'Majuro', 7.0897, 171.3803, 'Marshall Islands'' capital', 'city,coastal', 'urban'),

-- Nauru
(140, 'Yaren', -0.5467, 166.9211, 'Nauru''s de facto capital', 'city,coastal', 'urban'),

-- Kiribati
(99, 'Tarawa', 1.3291, 172.9790, 'Kiribati''s capital', 'city,coastal', 'urban'),

-- Samoa
(200, 'Apia', -13.8507, -171.7514, 'Samoa''s capital', 'city,coastal', 'urban'),

-- Tonga
(184, 'Nuku''alofa', -21.1393, -175.2049, 'Tonga''s capital', 'city,coastal', 'urban'),

-- French Polynesia
(63, 'Tahiti', -17.6509, -149.4260, 'French Polynesian island', 'island,beach,coastal', 'resort'),
(63, 'Bora Bora', -16.5004, -151.7415, 'French Polynesian island', 'island,beach,coastal', 'resort'),

-- Cook Islands
(141, 'Rarotonga', -21.2291, -159.7764, 'Cook Islands'' main island', 'island,beach,coastal', 'resort'),

-- Tuvalu
(188, 'Funafuti', -8.5203, 179.1945, 'Tuvalu''s capital', 'city,coastal', 'urban'),

-- Niue
(141, 'Alofi', -19.0554, -169.9179, 'Niue''s capital', 'city,coastal', 'urban'),

-- Tokelau
(141, 'Tokelau', -9.1667, -171.8333, 'Tokelau atoll', 'island,beach,coastal', 'resort'),

-- Pitcairn Islands
(66, 'Pitcairn Islands', -25.0667, -130.1000, 'Remote Pacific islands', 'island,beach,coastal', 'resort');

-- Antarctica Destinations
INSERT INTO Destination (country_id, name, latitude, longitude, description, tags, type) 
VALUES 
(193, 'McMurdo Station', -77.8463, 166.6683, 'US Antarctic research station', 'research-station', 'science'),
(193, 'Amundsen-Scott South Pole Station', -90.0000, 0.0000, 'US station at the South Pole', 'research-station', 'science'),
(33, 'Rothera Research Station', -67.5675, -68.1274, 'UK Antarctic research station', 'research-station', 'science'),
(11, 'Mawson Station', -67.6025, 62.8736, 'Australian Antarctic research station', 'research-station', 'science'),
(193, 'Antarctic Peninsula', -69.0000, -65.0000, 'Northernmost part of Antarctica', 'wilderness', 'nature'),
(193, 'South Shetland Islands', -62.0000, -58.0000, 'Antarctic archipelago', 'island,wilderness', 'nature'),
(193, 'Ross Sea region', -76.5000, 175.0000, 'Antarctic sea and coast', 'wilderness', 'nature');
"""

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
    temp_df = fetch_nasa_data(lat, lon, "T2M")
    precip_df = fetch_nasa_data(lat, lon, "PRECTOTCORR")
    climate_df = pd.concat([temp_df, precip_df], axis=1)
    climate_df["destination_id"] = dest_id
    return climate_df

def populate_weather_table():
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

def query_db():
    conn = sqlite3.connect('trip_recommender.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info(Weather);")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def alter_weather_schema():
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
    weather_df = populate_weather_table()
    # alter_weather_schema() # was used to update the weather schema
    conn = sqlite3.connect('trip_recommender.db')
    weather_df = weather_df.reset_index().rename(columns={"index": "weather_id"})

    cols = weather_df.columns.tolist()
    last_col = cols.pop()
    cols.insert(2, last_col)
    weather_df = weather_df[cols]

    weather_df.to_sql(name='Weather', con=conn, if_exists='append', index=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Weather")
    for row in cursor.fetchall():
        print(row)


if __name__ == '__main__':
    main()
