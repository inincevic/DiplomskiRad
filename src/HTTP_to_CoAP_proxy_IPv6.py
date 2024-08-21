import asyncio, fastapi
from aiocoap import *
import aiocoap

app = fastapi.FastAPI()
global context

@app.on_event("startup")
async def test_startup():
    # Create a context for the client
    global context
    context = await Context.create_client_context()

@app.get("/test")
async def test_route():
    global context
    # CoAP server URL (replace with your server's URL)
    server_url = "coap://[::1]:5683/test"

    # Create a request message
    request = Message(code=GET, uri=server_url)
    response = "No response yet"
    print("I'm here")
    
    # Send the request and get the response
    response = await context.request(request).response
    print("I'm here")
    print('Response code:', response.code)
    print('Response payload:', response.payload.decode("utf8"))
    
    return response.payload

# There will be different routes for taking temperatures from different devices
# For the purposes of simplicity, there will be two known devices: CoAPdevice1, and CoAPdevice2
# There will be two routes made accordingly for eahc of these.
@app.get("/temperature_device1")
async def get_temperature_device1():
    global context
    # CoAP server URL
    server_url = "coap://[::1]:5683/recordtemp"  ### presently, as both devices are running on the very same computer as the proxy, they take up localhost at port 5683, this will need to change

    # Create a request message
    request = Message(code=GET, uri=server_url)
    response = "No response yet"
       
    # Send the request and get the response
    response = await context.request(request).response
    print('Response code:', response.code)
    print('Response payload:', response.payload.decode("utf8"))
    temperature = response.payload.decode("utf8").split(":")[1].strip()

    return temperature

@app.get("/temperature_device2")
async def get_temperature_device2():
    global context
    # CoAP server URL
    server_url = "coap://[::1]:5683/recordtemp"  ### presently, as both devices are running on the very same computer as the proxy, they take up localhost at port 5683, this will need to change

    # Create a request message
    request = Message(code=GET, uri=server_url)
    response = "No response yet"
       
    # Send the request and get the response
    response = await context.request(request).response
    print('Response code:', response.code)
    print('Response payload:', response.payload.decode("utf8"))
    temperature = response.payload.decode("utf8").split(":")[1].strip()

    return temperature


### startup reminder:
### python -m uvicorn HTTP_to_CoAP_proxy_IPv6:app --reload --host [::1]