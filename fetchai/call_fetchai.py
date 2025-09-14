# call_fetchai.py

from uagents import Bureau, Agent, Context
from langchain_chroma import Chroma
import multiprocessing
from models import Query
from langchain_huggingface import HuggingFaceEmbeddings
from runner import vectorstore
import temp_agent
import time
import threading
import subprocess


class AgentHelper:
    def __init__(self, client: Chroma) -> None:
        self.client = client
        self.port = 8001
        self.senders: list[subprocess.Popen] = []
        with open('add.txt', 'w') as ports_file:
            ports_file.write('')

    def start(self):
        self.r = subprocess.Popen(['python', 'receiver_agent.py'])

    def send_queries(self, queries: list):
        for query in queries:
            self.send_query(query)

    def send_query(self, query: str):
        s = subprocess.Popen(['python', 'sender_agent.py', query, str(self.port)])
        self.port += 1
        self.senders.append(s)

    def close(self):
        self.r.wait()
        for i in self.senders:
            i.wait()


        


if __name__ == '__main__':
    helper = AgentHelper(client=vectorstore)
    helper.start()
    time.sleep(15)
    print('Started successfully')

    helper.send_queries(['fruit', 'metal', 'red'])
    # helper.send_query('fruit')

    helper.close()