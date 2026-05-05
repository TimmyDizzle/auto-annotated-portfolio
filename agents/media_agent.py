import json, re
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube visual specialist. Return JSON only."""

def extract_json(text):
    text = text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m: text = m.group(1)
    s, e = text.find("{"), text.rfind("}") + 1
    if s != -1 and e > s: text = text[s:e]
    return json.loads(text)

def run(script, brand_colors=None):
    colors = f"\n\nBrand colors: {', '.join(brand_colors)}" if brand_colors else ""
    title = script.get("title", "video")
    sections = [x.get("heading", "") for x in script.get("sections", [])]
    r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2048, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": (
            f"Video title: {title}\nSections: {json.dumps(sections)}{colors}\n\n"
            f"Return JSON with keys: thumbnail (object: text, colors, style), "
            f"broll (list of 5 strings), graphics (list of 3 strings), "
            f"music (object: mood, genre, tempo), "
            f"chapter_markers (list of objects: time, title). Return JSON only."
        )}])
    return extract_json(r.content[0].text)
