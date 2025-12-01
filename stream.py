import google.generativeai as genai
import os
import asyncio

# Load API key from environment or hardcode it:
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

async def stream_llm_via_ws(ws, msg):
    try:
        # Make real streaming request to Gemini
        response = model.generate_content(
            msg,
            stream=True  # enables token-by-token streaming
        )

        # Stream tokens back over WebSocket
        async for chunk in response:
            if chunk.text:
                # Stream characters smoothly to frontend
                for ch in chunk.text:
                    await ws.send_text(ch)
                    await asyncio.sleep(0.005)

    except Exception as e:
        await ws.send_text(f"[ERROR] {str(e)}")
