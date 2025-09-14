from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.build_rag_queries.main import break_down
from fetch_ai.call_fetchai import AgentHelper
from fetch_ai.sender_agent import get_responses
from backend.build_html.main import get_html
import time
import uvicorn

# Create FastAPI app
app = FastAPI(title="Question to HTML API")

# Request model
class QuestionRequest(BaseModel):
    user_question: str


@app.post("/get-html")
def get_html_from_question(request: QuestionRequest):
    try:
        agent_helper = AgentHelper()
        agent_helper.start()
        time.sleep(15)  # Give the agent time to start

        simplified_question_list = break_down(request.user_question)
        agent_helper.send_queries(simplified_question_list)

        response = get_responses()
        print("test")

        agent_helper.force_close()

        # Read response from file (as in your code)
        with open("response.txt", "r") as file:
            response = file.read()

        html = get_html(response)

        return {"html": html}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("workflow_api:app", host="0.0.0.0", port=8002, reload=True)

