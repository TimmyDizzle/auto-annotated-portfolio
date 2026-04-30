import json
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube scriptwriter. Return JSON with keys: title, description, hook, sections, outro, tags, estimated_duration_minutes."""
def run(research, tone="conversational", channel_context=None):
ctx = f"\n\nChannel context:\n{json.dumps(channel_context,indent=2)}" if channel_context else ""
r = client.messages.create(model="claude-sonnet-4-6", max_tokens=4096, system=SYSTEM_PROMPT, messages=[{"role":"user","content":f"Research:\n{json.dumps(research,indent=2)}\nTone: {tone}{ctx}\nReturn JSON."}])
raw = r.content[0].text.strip()
if raw.startswith("```"): raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
return json.loads(raw.strip())
