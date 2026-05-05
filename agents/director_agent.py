import json, re
from anthropic import Anthropic
client = Anthropic()
SYSTEM_PROMPT = """You are a cinematic AI video director. Convert YouTube scripts into Veo 2 video prompts and Imagen 3 thumbnail prompts. Return JSON only."""

def extract_json(text):
    text = text.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m: text = m.group(1)
    s, e = text.find("{"), text.rfind("}") + 1
    if s != -1 and e > s: text = text[s:e]
    return json.loads(text)

def run(script, visual_style="cinematic dark dramatic high contrast"):
    title = script.get("title", "")
    segments = [{"heading": "HOOK", "content": script.get("hook", "")}]
    for s in script.get("sections", []):
        segments.append({"heading": s.get("heading", ""), "content": s.get("content", "")})
    segments.append({"heading": "OUTRO", "content": script.get("outro", "")})
    r = client.messages.create(model="claude-sonnet-4-6", max_tokens=4096, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": (
            f"Video title: {title}\nVisual style: {visual_style}\n\n"
            f"Segments:\n{json.dumps(segments, indent=2)}\n\n"
            f"Return JSON with:\n"
            f"- thumbnail_prompt (Imagen 3 prompt: eye-catching 16:9 YouTube thumbnail, dramatic lighting, ultra detailed)\n"
            f"- clips (list, one per segment, each with: segment, prompt, duration_seconds, caption)\n"
            f"Each clip prompt: cinematic Veo 2 description with camera movement, lighting, subject, mood. End with: photorealistic 4K HDR\n"
            f"Return JSON only."
        )}])
    return extract_json(r.content[0].text)
