import json, re
from datetime import datetime, timezone
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a YouTube growth strategist. Return JSON only."""

def extract_json(text):
    text = text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m: text = m.group(1)
    s, e = text.find("{"), text.rfind("}") + 1
    if s != -1 and e > s: text = text[s:e]
    return json.loads(text)

def run(script, media_assets, channel_context=None, publish_immediately=False):
    ctx = f"\n\nChannel context:\n{json.dumps(channel_context, indent=2)}" if channel_context else ""
    title = script.get("title", "video")
    tags = script.get("tags", [])
    r = client.messages.create(model="claude-sonnet-4-6", max_tokens=2048, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": (
            f"Time: {datetime.now(timezone.utc).isoformat()}\n"
            f"Video title: {title}\nTags: {json.dumps(tags)}{ctx}\n\n"
            f"Return JSON with keys: upload_metadata (object: title, description, category, privacy), "
            f"schedule (object: recommended_day, recommended_time, timezone), "
            f"checklist (list of 8 strings), ab_test_titles (list of 3 strings), "
            f"community_post (string), pinned_comment (string), "
            f"end_screen_suggestions (list of 3 strings). Return JSON only."
        )}])
    return extract_json(r.content[0].text)
