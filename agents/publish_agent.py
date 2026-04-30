import json
from datetime import datetime, timezone
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube growth strategist. Return JSON with keys: upload_metadata, schedule, checklist, ab_test_titles, community_post, pinned_comment, end_screen_suggestions."""
def run(script, media_assets, channel_context=None, publish_immediately=False):
ctx = f"\n\nChannel context:\n{json.dumps(channel_context,indent=2)}" if channel_context else ""
r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2048, system=SYSTEM_PROMPT, messages=[{"role":"user","content":f"Time: {datetime.now(timezone.utc).isoformat()}\nScript:\n{json.dumps(script,indent=2)}\nMedia:\n{json.dumps(media_assets,indent=2)}{ctx}\nReturn JSON."}])
raw = r.content[0].text.strip()
if raw.startswith("```"): raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
return json.loads(raw.strip())
