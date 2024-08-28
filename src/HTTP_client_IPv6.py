import fastapi, httpx, json
import datetime
import psycopg2


app = fastapi.FastAPI()
proxy_url = "http://[::1]:8000"
conn = ""
cursor = ""
table_name = ""


# Startup tasks
@app.on_event("startup")
async def startup_method():
    global conn, cursor, table_name

    # Connecting to the database using my connection string
    CONNECTION = "postgres://tsdbadmin:icpv9i2l4ewanuzw@nc0exan2js.pephiae70q.tsdb.cloud.timescale.com:30892/tsdb?sslmode=require"
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    table_name = "temperatures_IPv6"

# Shurdown tasks
@app.on_event("shutdown")
async def shutdown_method():
    global conn, cursor
    if conn:
        cursor.close()
        conn.close()


# -----------------------------------------------------------------------
# Management Routes

# Test route
@app.get("/")
def test_get():
    return "The code works."


# ----------------------------------------------------------------------------------- 
# Routes for asking the devices for temperatures (through the proxy)
@app.get("/temperature_dev1")
async def get_temperature_device1():
    url = proxy_url + "/temperature_device1"

    print("Asking Device 1 for the recorded temperature.")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout = 25)
        recorded_temperature = json.loads(response.text)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Inserting recieved temperature into the database
    cursor.execute(f"""
        INSERT INTO {table_name} (device, time, temperature)
        VALUES (%s, %s, %s);
    """, ("Device 1", current_time, float(recorded_temperature)))
    conn.commit()
    print("Data inserted successfully.")

    return recorded_temperature

@app.get("/temperature_dev2")
async def get_temperature_device2():
    url = proxy_url + "/temperature_device2"

    print("Asking Device 2 for the recorded temperature.")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout = 25)
        recorded_temperature = json.loads(response.text)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Inserting recieved temperature into the database
    cursor.execute(f"""
        INSERT INTO {table_name} (device, time, temperature)
        VALUES (%s, %s, %s);
    """, ("Device 2", current_time, float(recorded_temperature)))
    conn.commit()
    print("Data inserted successfully.")

    return recorded_temperature

@app.get("/all_recored_temperatures")
async def get_all_temperatures():
    all_recorded = []
    # Fetching all temperatures from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    # Parsing the result of the query so that ID is not returned
    all_recorded = [(item[1], item[2], item[3]) for item in rows]

    return all_recorded

### python -m uvicorn HTTP_to_CoAP_proxy_IPv6:app --reload --host '::1'