import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from agents import research_agent, script_agent, media_agent, publish_agent

MEMORY_PATH = Path(__file__).parent / "memory" / "channel_memory.json"

def load_memory():
    return json.loads(MEMORY_PATH.read_text()) if MEMORY_PATH.exists() else {}

def save_memory(m):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(json.dumps(m, indent=2))

def run_pipeline(niche, topic, tone="conversational", brand_colors=None, publish_now=False):
    mem = load_memory()
    ctx = mem.get("channel_context", {})
    print(f"[RESEARCH] {topic}")
    r = research_agent.run(niche, topic, ctx)
    print(f"[SCRIPT] writing...")
    s = script_agent.run(r, tone, ctx)
    print(f"[MEDIA] assets...")
    m = media_agent.run(s, brand_colors)
    print(f"[PUBLISH] packaging...")
    p = publish_agent.run(s, m, ctx, publish_now)
    mem.setdefault("video_history", []).append({"timestamp": datetime.now(timezone.utc).isoformat(), "title": s.get("title", "")})
    mem["video_history"] = mem["video_history"][-50:]
    save_memory(mem)
    return {"research": r, "script": s, "media": m, "publish": p}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--tone", default="conversational")
    args = ap.parse_args()
    res = run_pipeline(args.niche, args.topic, args.tone)
    print(f"\nTitle: {res['script'].get('title')}")
