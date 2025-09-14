# receiver_agent.py

from uagents import Agent, Context, Model
from test_wo_anthropic import Test
from runner import test
from models import RAGResponse

def run_retriever(msg: str, runner: Test):
    return runner.run_retriever(msg)

# 1. Define the message models
class Request(Model):
    message: str

class Response(Model):
    response: str

# 2. Initialize the receiving agent
receiver = Agent(
    name="receiver_agent",
    port=8000,
    endpoint=["http://localhost:8000/submit"],
    seed="my_receiver_seed"
)


@receiver.on_event("startup")
async def send_message(ctx: Context):
    ctx.logger.info("Starting receiver agent...")
    with open('./fetch_ai/add.txt', 'w') as file:
        file.write(receiver.address)


# 4. Define the message handler
@receiver.on_message(model=Request)
async def handle_request(ctx: Context, sender: str, msg: Request):
    ctx.logger.info(f"Received request from {sender}: {msg.message}")
    # Send a response back
    await ctx.send(sender, RAGResponse(content=run_retriever(msg.message, test).to_dict()))

# 5. Run the agent
if __name__ == "__main__":
    # with open('ports.txt', 'w') as file:
    #     file.write('1')
    receiver.run()