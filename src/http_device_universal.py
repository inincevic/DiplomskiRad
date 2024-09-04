import fastapi, httpx, json
import datetime
import random, os, argparse


app = fastapi.FastAPI()
write_file_name = "./write_file.txt"
global device_name
device_name = "Device1"

# Startup tasks
@app.on_event("startup")
async def startup_method():
    global device_name

    # Creating the write file if it doesn't already exist
    if not os.path.exists(write_file_name):
        with open(write_file_name, 'w') as write_file:
            print(f"File {write_file_name} created.")

# -----------------------------------------------------------------------
# Management Routes

# Test route
@app.get("/")
def test_get():
    return "The code works."

# as the devices used for this paper are simulated, the temperatures need to be randomly generated
async def generate_random_temperature():
    random_number = round(random.uniform(25.0, 33.0),1)
    #print(random_number)
    return random_number

# ----------------------------------------------------------------------------------- 
# Routes for asking the devices for temperatures (through the proxy)
@app.get("/record_temperature")
async def get_temperature_device1():
    global device_name
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
    current_temperature = await generate_random_temperature()

    # Crafting the message to send
    message_to_write = ""
    message_to_write = message_to_write + ("Recording device: %s" % device_name)
    message_to_write = message_to_write + ("\n Time of recording: %s" % current_time)
    message_to_write = message_to_write + ("\n Recorded temperature: %s " % current_temperature)
    message_to_write = message_to_write + ("\n----------------------------------------------\n")
        
    # Establishing the number of lines in the file, so that writing into the file can be confirmed.
    with open(write_file_name, "r") as file:
        lines = file.readlines()
        write_file_name_start_lenght = len(lines)

    # Writing the message into the file
    with open(write_file_name, "a") as file:
            file.write(message_to_write)
    
    # Checking the current number of lines in the file.
    with open(write_file_name, "r") as file:
        lines = file.readlines()
        write_file_name_end_lenght = len(lines)

    # Checking if the message was added and returning an apropriate reply.
    if(write_file_name_end_lenght > write_file_name_start_lenght):
        text = "Current temperature is: %s" % current_temperature
    else:
        text = "An error ocurred while writing into file."

    return text

@app.get("/all_temperatures")
async def get_temperature_device2():
    global write_file_name
    with open(write_file_name, "r") as file:
        lines = file.readlines()
    recorded_temperatures = ""
    for line in lines:
        recorded_temperatures = recorded_temperatures + line
    #print(recorded_temperatures)
    return recorded_temperatures


## running IPv4
## python -m uvicorn http_device_universal:app --reload --port 8002

## running IPV6
## python -m uvicorn http_device_universal:app --reload --port 8002 --host '::1'