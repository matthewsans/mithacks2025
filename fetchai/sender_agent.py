# sender_agent.py

from uagents import Agent, Context, Model
import asyncio
from models import RAGResponse, Query
import sys

# 1. Define the message models (must be the same as the receiver's)
class Request(Model):
    message: str

class Response(Model):
    response: str

# 2. Set the address of the receiving agent
# NOTE: This address needs to be the actual address printed when you run receiver_agent.py

# 3. Initialize the sending agent

port = sys.argv[2]
sender = Agent(
    name="sender_agent",
    seed="my_sender_seed",
    port=int(port),
    endpoint=[f"http://localhost:{port}/submit"]
)

# 4. Fund the agent's wallet

# 5. Define the startup event to send the message
@sender.on_event("startup")
async def send_message(ctx: Context):
    ctx.logger.info("Starting sender agent...")

    with open('add.txt', 'r') as file:
        receiver = file.readlines()[0].strip()
        await ctx.send(receiver, Request(message=message))
    

# 6. Define the message handler for the response
@sender.on_message(model=RAGResponse)
async def handle_response(ctx: Context, sender: str, msg: RAGResponse):
    ctx.logger.info(f"Received response from {sender}: {msg.content}")
    # Stop the agent after the response is received

# 6. Define the message handler for the response
# @sender.on_message(model=Request)
# async def send_command(ctx: Query, sender: str, msg: Query):
#     ctx.logger.info(f"Received response from {sender}: {msg.message}")
#     await ctx.send(msg.destination, Request(message=msg.message))
#     # Stop the agent after the response is received
#     # await asyncio.sleep(5)

# 7. Run the agent
if __name__ == "__main__":
    message = sys.argv[1]
    sender.run()