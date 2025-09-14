# call_fetchai.py

import time
import subprocess

class AgentHelper:
    def __init__(self) -> None:
        # self.client = client
        self.port = 8001
        self.senders: list[subprocess.Popen] = []

    def start(self):
        self.r = subprocess.Popen(['python', 'fetch_ai/receiver_agent.py'])

    def send_queries(self, queries: list):
        for query in queries:
            self.send_query(query)

    def send_query(self, query: str):
        # print(['python', 'sender_agent.py', query, str(self.port)])
        s = subprocess.Popen(['python', 'fetch_ai/sender_agent.py', query, str(self.port)])
        self.port += 1
        self.senders.append(s)

    def close(self):
        self.r.wait()
        for i in self.senders:
            i.wait()

    def force_close(self):
        self.r.kill()
        for i in self.senders:
            i.kill()


        


if __name__ == '__main__':
    helper = AgentHelper()
    helper.start()
    time.sleep(15)
    print('Started successfully')

    helper.send_queries(['how about debt of Intuit?', 'how about detail information of income of Intuit?', 'Can you show me the financial income and revenue of Intuit'])
    # helper.send_query('fruit')

    