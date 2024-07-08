# This code will simulate three different CoAP devices.
# All routes listed in coap_proxy.py will be used here so that they can be ran.
# It's important to note that URLs in proxy app are hard coded, so for different routes to be used,
# this device needs to be ran on different URLs (presently PORTS).

'''
This code is for now written in HTTP, I will need to check if I need rewrite the code into CoAP, or
if CoAP works with HTTP written code.
'''

import fastapi, time, httpx, sys, json, os, subprocess, asyncio

app = fastapi.FastAPI()
write_file_name = "./write_file.txt"

# Startup event that checks if the file for writing exists, and creates it if it doesn't
@app.on_event("startup")
async def open_write_file():
    if not os.path.exists(write_file_name):
        with open(write_file_name, 'w') as write_file:
            print(f"File {write_file_name} created.")

# -----------------------------------------------------------------------------------------------
# Management Routes and Methods

# Test route #1
@app.get("/")
def test_get():
    return "The worker code works."

# Test route #2
@app.get("/temperature")
def test_get():
    return "Current temperature is 34 degrees celsius."

# Routes that do the main jobs of CoAP devices

# Route that makes sure that the simple job of reversing the recieved message is done
# with a delay of 10s
@app.get("/do_work/{recieved_message}")
def do_work(recieved_message):
    
    # Print to test if the message was correctly recieved
    # print(f"I recieved the following message: {message}.")
    
    # Sleep is used to simulaate processing time
    time.sleep(10)

    return_message = recieved_message[::-1]
    
    # Prints that confirm if  and when the processes were completed correctly
    # print(f"Reversed message: {message2}")
    # print(f"Done sleeping, returning reversed message: {message2}")
    return return_message

# Route that writes down the recorded temperature
# In a realistic device with a measuring tool, this route would take the current
# measure of temperature and write it into file, but as we're simulating a network
# this temperature is being randomly generated and sent to the CoAP device.
@app.get("/write_temperature/{message}")
async def write_to_file(message):

    # Establishing the number of lines in the file, so that writing into the file can be confirmed.
    with open(write_file_name, "r") as file:
        lines = file.readlines()
        write_file_name_start_lenght = len(lines)

    # Adding a line break to the end of the message so that messages can be separated from each other.
    message_to_write = message + "\n"

    # Writing the message into the file
    with open(write_file_name, "a") as file:
            file.write(message_to_write)
    
    # Checking the current number of lines in the file.
    with open(write_file_name, "r") as file:
        lines = file.readlines()
        write_file_name_end_lenght = len(lines)

    # Checking if the message was added and returning an apropriate reply.
    if(write_file_name_end_lenght > write_file_name_start_lenght):
        return "The message has been written into the file."
    else:
        return "An error ocurred while writing into file."
    
# Route which tells the CoAP device to report on all recorded temperatures.
@app.get("/list_temperatures")
def read_from_file():
    with open(write_file_name, "r") as file:
        lines = file.readlines()
    return lines