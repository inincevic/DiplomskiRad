import asyncio, fastapi, httpx, json
from aiocoap import *

app = fastapi.FastAPI()

# test route for testing hte connection to the HTTP device
@app.get("/test")
async def test_route():
    
    # HTTP server URL
    server_url = "http://[::1]:8002/test"

    # Sending a HTTP request
    async with httpx.AsyncClient() as client:
        response = await client.get(server_url, timeout = 25)
        resp_test = json.loads(response.text)
    
    # Returning the response
    return resp_test

# There will be different routes for taking temperatures from different devices
# For the purposes of simplicity, there will be two known devices: CoAPdevice1, and CoAPdevice2
# There will be two routes made accordingly for eahc of these.
@app.get("/temperature_device1")
async def get_temperature_device1():
    # CoAP server URL, with this example, both servers run on the same IP and port
    # thus it's impossible to run them at the same time on the same host
    server_url = "http://[::1]:8002/record_temperature"

    # Sending a HTTP request
    async with httpx.AsyncClient() as client:
        response = await client.get(server_url, timeout = 25)
        recorded_temperature = json.loads(response.text)
    
    # Returning the response
    print(recorded_temperature)

    return recorded_temperature

@app.get("/temperature_device2")
async def get_temperature_device2():
    # CoAP server URL, with this example, both servers run on the same IP and port
    # thus it's impossible to run them at the same time on the same host
    server_url = "http://[::1]:8002/record_temperature"

    # Sending a HTTP request
    async with httpx.AsyncClient() as client:
        response = await client.get(server_url, timeout = 25)
        recorded_temperature = json.loads(response.text)
    
    # Returning the response
    print(recorded_temperature)

    return recorded_temperature

## running this code
## python -m uvicorn HTTP_to_HTTP_proxy_IPv4:app --reload --port 8000 --host '::1'