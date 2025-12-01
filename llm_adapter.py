import google.generativeai as genai
from .config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(user_msg, ctx=None):
    model = genai.GenerativeModel("gemini-pro")

    prompt = user_msg
    if ctx:
        prompt += "\n\nContext:\n" + "\n".join(ctx)

    response = model.generate_content(prompt)
    return response.text
