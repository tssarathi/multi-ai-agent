from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agents.agent import get_response_from_agent
from src.config.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent")


class ChatRequest(BaseModel):
    llm_id: str
    messages: str
    allow_websearch: bool
    system_prompt: str


@app.post("/chat")
def chat(request: ChatRequest):
    logger.info(f"Chat request received: {request}")

    if request.llm_id not in config.ALLOWED_MODELS:
        raise HTTPException(
            status_code=400, detail=f"{request.llm_id} is not a valid model"
        )

    try:
        response = get_response_from_agent(
            request.llm_id,
            request.messages,
            request.allow_websearch,
            request.system_prompt,
        )
        logger.info(
            f"Successfully got response {response} from {request.llm_id} AI agent"
        )
        return {"response": response}

    except Exception as e:
        logger.error(f"Error getting response from {request.llm_id} AI agent: {e}")
        error_msg = str(e) if e else "Unknown error"
        raise HTTPException(
            status_code=500,
            detail=f"Error getting response from AI agent: {error_msg}",
        )
