
import re
from .config import CRISIS_KEYWORDS

def check_crisis(text: str):
    t = text.lower()
    for k in CRISIS_KEYWORDS:
        if k in t:
            return {"flag": True, "match": k}
    return {"flag": False}
