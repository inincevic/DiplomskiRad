import datetime, random, asyncio
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap
import argparse

import os
write_file_name = "./write_file.txt"
global device_name
device_name = ""

# as the devices used for this paper are simulated, the temperatures need to be randomly generated
async def generate_random_temperature():
    random_number = round(random.uniform(25.0, 33.0),1)
    #print(random_number)
    return random_number

# test route, checking if the CoAP device is working as it should
class Test(resource.Resource):
    async def render_get(self, request):
        text = "Test successful"
        return aiocoap.Message(payload=text.encode("utf8"))


# Classes where the CoAP device's tasks are detailed

# Class where the CoAP device randomly generates a temperature, 
# records that temperature into the file and returns it 
# to the service that requested the temperature
# The temperature is randomly generated through the generate_random_temperature() method
# Time of recording is automatically recorded by the system
class RecordTemperature(resource.Resource):
    async def render_get(self, request):
        global device_name
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # In CoAP, body of a request is called "payload"!
        current_temperature = await generate_random_temperature()

        # Crafting the message to write
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

        return aiocoap.Message(payload = text.encode("utf8"))

# Class where the CoAP device returns all recorded temperatures
class ListTemperatures(resource.Resource):
    async def render_get(self, request):
        # opening the file to read all temperatures recorded into it
        with open(write_file_name, "r") as file:
            lines = file.readlines()
        recorded_temperatures = ""
        for line in lines:
            recorded_temperatures = recorded_temperatures + line
        
        # print(recorded_temperatures)

        return aiocoap.Message(payload = recorded_temperatures.encode("utf8"))

async def main():

    # Creating the write file if it doesn't already exist
    if not os.path.exists(write_file_name):
        with open(write_file_name, 'w') as write_file:
            print(f"File {write_file_name} created.")

    # Resource tree creation
    root = resource.Site()

    # Adding resources, or routes, to the device
    root.add_resource(
        [".well-known", "core"], resource.WKCResource(root.get_resources_as_linkheader)
    )
    
    root.add_resource(["test"], Test())
    root.add_resource(["recordtemp"], RecordTemperature())
    root.add_resource(["alltemperatures"], ListTemperatures())

    # On Windows bind is necessary because the code can't pick up the localhost address and port by itself
    await aiocoap.Context.create_server_context(bind=('127.0.0.1',5683), site = root)

    # Run forever
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    # as the name for the device is used when recording temperatures, an argument needs to be
    # recorded from the arguments that were imput when the device was started
    parser = argparse.ArgumentParser(description="Parser is used for the name of the device that is running.")
    parser.add_argument("name", help="Please put in the name of this device")
    args = parser.parse_args()
    device_name = args.name
    asyncio.run(main())