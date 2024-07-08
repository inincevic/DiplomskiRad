import asyncio, fastapi
from aiocoap import *

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
    server_url = "coap://127.0.0.1:5683/whoami"


    # Create a request message
    request = Message(code=GET, uri=server_url)
    response = "No response yet"
    print("I'm here")
    try:
        # Send the request and get the response
        response = await context.request(request).response
        print("I'm here")
        print('Response code:', response.code)
        print('Response payload:', response.payload.decode('utf-8'))
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    return response