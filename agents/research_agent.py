import json
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube research specialist. Return JSON with keys: topic, angle, key_points, stats, sources, seo_keywords."""
def run(niche, topic_request, channel_context=None):
ctx = f"\n\nChannel context:\n{json.dumps(channel_context,indent=2)}" if channel_context else ""
r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2048, system=SYSTEM_PROMPT, messages=[{"role":"user","content":f"Niche: {niche}\nTopic: {topic_request}{ctx}\nReturn JSON."}])
raw = r.content[0].text.strip()
if raw.startswith("```"): raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
return json.loads(raw.strip())
