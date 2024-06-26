# All routes and methods for contacting CoAP devices in this code are 
# imaginations of what CoAP devices in a realistic networks could do.
# This entire code serves as a proxy that can be contacted on a specific 
# route, and then later on send that work to CoAP devices themselves, 
# without revealing the address of the final device to the client.

'''
URLs used in this file need to be changed, as they are currently written so that they work when 
ran from the same device
'''

import fastapi, httpx, json, asyncio, random, sys, subprocess

app = fastapi.FastAPI()

# -----------------------------------------------------------------------------------------------
# Management Routes and Methods

# Test route
@app.get("/")
def test_get():
    return "The code works."

async def contact_CoAP(urlToSend):
    async with httpx.AsyncClient() as client:
        response = await client.get(urlToSend, timeout = 40)
        return response

# -----------------------------------------------------------------------------------------------
# Available routes that, when invoked, run a certain method in order to send taks to CoAP devices

# Route which sends a message to the CoAP device and expects the reversed message back 
# after a certain period of sleep on the workier
@app.get("/send_sleep/{message}")
async def send_work(message):
    # Print used for test purposes
    # print(f"Given message is: {message}.")
    ret_msg = await sleep_work(message)
    return ret_msg

# Route that tells the CoAP device to write down the current temperature
# For simplicity, these temperatures will be randomly generated.
@app.get("/record_temperature")
async def record_temperature():
    # The temperature is randomly generated here
    current_temperature = random.randint(17, 30)

    ret_msg = await write_temperature(current_temperature)
    return ret_msg

# Route that requests the CoAP device to list out all recorded temperatures.
@app.get("/list_temperatures")
async def list_temperature():
    file_contents = await get_temperatures()
    return file_contents



# -----------------------------------------------------------------------------------------------
# Methods which send specific tasks to different CoAP devices depending on the route invoked

# Method for sending to /do_work/ route where the message is just inverted after sleeping.
async def sleep_work(message):
    # Considering the fact that for a network like this, we need to assume that we know addresses 
    # of specific CoAP devices, they will be hard coded in this code.

    url = "http://127.0.0.1:8001/do_work/" + message
    # Print that confirms the final URL on which the task will be sent. Used for testing purposes.
    # print(url)
    
    resp = await contact_CoAP(url)
    return json.loads(resp.text)

# Method for sending the current temperature to CoAP device, these temperatures need to be 
# written into a file that these devices can access.
async def write_temperature(temperature):
    # Considering the fact that for a network like this, we need to assume that we know addresses 
    # of specific CoAP devices, they will be hard coded in this code.

    url = "http://127.0.0.1:8002/write_temperature/" + temperature
    # Print that confirms the final URL on which the task will be sent. Used for testing purposes.
    # print(url)
    
    resp = await contact_CoAP(url)
    return json.loads(resp.text)

# Method which tells the CoAP device to list all currently recorded temperatures
async def get_temperatures():
    
    url = "http://127.0.0.1:8003/list_temperatures"
    # Print that confirms the final URL on which the task will be sent. Used for testing purposes.
    # print(url)
    
    resp = await contact_CoAP(url)
    return json.loads(resp.text)