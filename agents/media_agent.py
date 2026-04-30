import json
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube visual specialist. Return JSON with keys: thumbnail, broll, graphics, music, chapter_markers."""
def run(script, brand_colors=None):
colors = f"\n\nBrand colors: {', '.join(brand_colors)}" if brand_colors else ""
r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2048, system=SYSTEM_PROMPT, messages=[{"role":"user","content":f"Script:\n{json.dumps(script,indent=2)}{colors}\nReturn JSON."}])
raw = r.content[0].text.strip()
if raw.startswith("```"): raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
return json.loads(raw.strip())
