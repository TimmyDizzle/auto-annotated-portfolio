import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from agents import research_agent, script_agent, media_agent, publish_agent

MEMORY_PATH = Path(__file__).parent / "memory" / "channel_memory.json"
OUTPUT_PATH = Path(__file__).parent / "output"

def load_memory():
    return json.loads(MEMORY_PATH.read_text()) if MEMORY_PATH.exists() else {}

def save_memory(m):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(json.dumps(m, indent=2))

def run_pipeline(niche, topic, tone="conversational", brand_colors=None, publish_now=False):
    mem = load_memory()
    ctx = mem.get("channel_context", {})
    print(f"\n{'='*55}")
    print(f"  YouTube Agent Pipeline")
    print(f"  Niche: {niche}")
    print(f"  Topic: {topic}")
    print(f"{'='*55}\n")
    print("[1/4] RESEARCH...")
    r = research_agent.run(niche, topic, ctx)
    print(f"      Angle: {r.get('angle','')}")
    print("[2/4] SCRIPT...")
    s = script_agent.run(r, tone, ctx)
    print(f"      Title: {s.get('title','')}")
    print(f"      Duration: ~{s.get('estimated_duration_minutes','?')} min")
    print("[3/4] MEDIA ASSETS...")
    m = media_agent.run(s, brand_colors)
    print(f"      Music mood: {m.get('music',{}).get('mood','')}")
    print("[4/4] PUBLISH PACKAGE...")
    p = publish_agent.run(s, m, ctx, publish_now)
    sch = p.get("schedule", {})
    print(f"      Best upload: {sch.get('recommended_day','')} at {sch.get('recommended_time','')}")
    OUTPUT_PATH.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe = s.get("title","output")[:40].replace(" ","_").replace("/","-")
    out = OUTPUT_PATH / f"{ts}_{safe}.json"
    out.write_text(json.dumps({"research":r,"script":s,"media":m,"publish":p}, indent=2))
    mem.setdefault("video_history",[]).append({"timestamp":datetime.now(timezone.utc).isoformat(),"title":s.get("title",""),"niche":niche})
    mem["video_history"] = mem["video_history"][-50:]
    save_memory(mem)
    print(f"\n{'='*55}")
    print(f"  COMPLETE! Full results saved to:")
    print(f"  {out}")
    print(f"{'='*55}")
    print(f"\n--- VIDEO TITLE ---")
    print(f"  {s.get('title','')}")
    print(f"\n--- DESCRIPTION ---")
    print(f"  {s.get('description','')}")
    print(f"\n--- HOOK (first 30 seconds) ---")
    print(f"  {s.get('hook','')}")
    print(f"\n--- UPLOAD CHECKLIST ---")
    for i, item in enumerate(p.get("checklist",[]), 1):
        print(f"  {i}. {item}")
    print(f"\n--- 3 TITLE OPTIONS TO A/B TEST ---")
    for t in p.get("ab_test_titles",[]):
        print(f"  - {t}")
    print(f"\n--- PINNED COMMENT (paste this after upload) ---")
    print(f"  {p.get('pinned_comment','')}")
    print(f"\n--- THUMBNAIL CONCEPT ---")
    thumb = m.get("thumbnail",{})
    print(f"  Text: {thumb.get('text','')}")
    print(f"  Style: {thumb.get('style','')}")
    print(f"\n--- CHAPTER MARKERS ---")
    for c in m.get("chapter_markers",[]):
        print(f"  {c.get('time','')} - {c.get('title','')}")
    return {"research":r,"script":s,"media":m,"publish":p}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--tone", default="conversational")
    args = ap.parse_args()
    run_pipeline(args.niche, args.topic, args.tone)
