import datetime
import logging

import asyncio

import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap

import os
write_file_name = "./write_file.txt"

    
# test route
class Test(resource.Resource):
    async def render_get(self, request):
        text = "Test successful"
        return aiocoap.Message(payload=text.encode("utf8"))

# Classes where the CoAP device's tasks are detailed

# Class where the CoAP device records the given temperature into the file
# The temperature needs to be given through the Post method, and the time
# of recording is automatically taken from the system.
class RecordTemperature(resource.Resource):
    async def render_post(self, request):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # In CoAP, body of a request is called "payload"!
        current_temperature = int(request.payload)

        # Crafting the message to send
        message_to_write = ""
        message_to_write = message_to_write + ("Time of recording: %s" % current_time)
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
            text = "The message has been written into the file."
        else:
            text = "An error ocurred while writing into file."

        return aiocoap.Message(payload = text.encode("utf8"))

# Class where the CoAP device returns all recorded temperatures
class ListTemperatures(resource.Resource):
    async def render_get(self, request):
        with open(write_file_name, "r") as file:
            lines = file.readlines()
        recorded_temperatures = ""
        for line in lines:
            recorded_temperatures = recorded_temperatures + line
        #print(recorded_temperatures)
        return aiocoap.Message(payload = recorded_temperatures.encode("utf8"))

async def main():

    # Creating the write file if it doesn't already exist
    if not os.path.exists(write_file_name):
        with open(write_file_name, 'w') as write_file:
            print(f"File {write_file_name} created.")

    # Resource tree creation
    root = resource.Site()

    root.add_resource(
        [".well-known", "core"], resource.WKCResource(root.get_resources_as_linkheader)
    )
    
    root.add_resource(["test"], Test())
    root.add_resource(["recordtemp"], RecordTemperature())
    root.add_resource(["alltemperatures"], ListTemperatures())

    # On Windows bind is necessary because the code can't pick up the localhost address and port by itself
    await aiocoap.Context.create_server_context(bind=('::1',5683), site = root)

    # Run forever
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())