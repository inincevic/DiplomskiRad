import datetime
import logging

import asyncio

import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat
import aiocoap

import os
write_file_name = "./write_file.txt"

### will do a rework, but keep this
class Welcome(resource.Resource):
    representations = {
        ContentFormat.TEXT: b"This is a test server used for purposes of testing stuff",
        ContentFormat.LINKFORMAT: b"</.well-known/core>,ct=40",
        # ad-hoc for application/xhtml+xml;charset=utf-8
        # ContentFormat(65000): b'<html xmlns="http://www.w3.org/1999/xhtml">'
        # b"<head><title>aiocoap demo</title></head>"
        # b"<body><h1>Welcome to the aiocoap demo server!</h1>"
        # b'<ul><li><a href="time">Current time</a></li>'
        # b'<li><a href="whoami">Report my network address</a></li>'
        # b"</ul></body></html>",
    }

    default_representation = ContentFormat.TEXT

    async def render_get(self, request):
        cf = (
            self.default_representation
            if request.opt.accept is None
            else request.opt.accept
        )
        try:
            return aiocoap.Message(payload=self.representations[cf], content_format=cf)
        except KeyError:
            raise aiocoap.error.UnsupportedContentFormat


### Definitely could delete
class BlockResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.set_content(
            b"This is the resource's default content. It is padded "
            b"with numbers to be large enough to trigger blockwise "
            b"transfer.\n"
        )

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print("PUT payload: %s" % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)


### Could learn from this.
### To delete
class SeparateLargeResource(resource.Resource):
    """Example resource which supports the GET method. It uses asyncio.sleep to
    simulate a long-running operation, and thus forces the protocol to send
    empty ACK first."""

    def get_link_description(self):
        # Publish additional data in .well-known/core
        return dict(**super().get_link_description(), title="A large resource")

    async def render_get(self, request):
        await asyncio.sleep(3)

        payload = (
            "Three rings for the elven kings under the sky, seven rings "
            "for dwarven lords in their halls of stone, nine rings for "
            "mortal men doomed to die, one ring for the dark lord on his "
            "dark throne.".encode("ascii")
        )
        return aiocoap.Message(payload=payload)

# Time resource, could use
class TimeResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode("ascii")
        return aiocoap.Message(payload=payload)
    
### my test route
class Test(resource.Resource):
    async def render_get(self, request):
        text = "Test successful"
        return aiocoap.Message(payload=text.encode("utf8"))

# Classes where the CoAP device's tasks are detailed
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

async def main():

    if not os.path.exists(write_file_name):
        with open(write_file_name, 'w') as write_file:
            print(f"File {write_file_name} created.")

    # Resource tree creation
    root = resource.Site()

    root.add_resource(
        [".well-known", "core"], resource.WKCResource(root.get_resources_as_linkheader)
    )
    root.add_resource([""], Welcome())
    root.add_resource(["time"], TimeResource())
    root.add_resource(["other", "block"], BlockResource())
    root.add_resource(["other", "separate"], SeparateLargeResource())
    root.add_resource(["test"], Test())
    root.add_resource(["recordtemp"], RecordTemperature())

    await aiocoap.Context.create_server_context(bind=('127.0.0.1',5683), site = root)

    # Run forever
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())