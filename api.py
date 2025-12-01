import json
from fastapi import APIRouter, WebSocket
from .safety import check_crisis
from .emotion import detect_emotion
from .rag_pinecone import retrieve
from .stream import stream_llm_via_ws
from .db import SessionLocal, Chat

router = APIRouter()

@router.websocket("/ws/chat")
async def ws_chat(ws: WebSocket):
    await ws.accept()

    data = await ws.receive_text()
    payload = json.loads(data)
    msg = payload.get("message","")

    # Crisis detection
    if check_crisis(msg)["flag"]:
        await ws.send_text(json.dumps({
            "type": "crisis",
            "reply": "I’m worried about your safety. Are you in danger?"
        }))
        await ws.close()
        return

    # RAG (optional) - still works but ignored in demo mode
    rag = [h["text"] for h in retrieve(msg)]

    # STREAM DEMO RESPONSE
    await stream_llm_via_ws(ws, msg)

    await ws.close()
