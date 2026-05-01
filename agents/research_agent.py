import json
from anthropic import Anthropic

client = Anthropic()
SYSTEM_PROMPT = "You are a YouTube research specialist. Always respond with valid JSON only, no extra text."

def run(niche, topic_request, channel_context=None):
    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": (
            f"Return a JSON object with keys: topic, angle, "
            f"key_points (list of 5 strings), stats (list of 3 strings), "
            f"sources (list of 3 strings), seo_keywords (list of 5 strings).\n\n"
            f"Niche: {niche}\nTopic: {topic_request}"
        )}]
    )
    raw = r.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
