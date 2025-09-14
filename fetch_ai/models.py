# models.py

from uagents import Model

class Query(Model):
    content: str
    sender: str
    destination: str

class RAGResponse(Model):
    content: dict

class Request(Model):
    message: str