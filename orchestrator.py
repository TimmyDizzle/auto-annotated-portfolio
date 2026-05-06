import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from agents import research_agent, script_agent, media_agent, publish_agent, director_agent, voice_agent, video_agent, assembly_agent

MEMORY_PATH = Path(__file__).parent / "memory" / "channel_memory.json"
OUTPUT_PATH = Path(__file__).parent / "output"

def load_memory():
    return json.loads(MEMORY_PATH.read_text()) if MEMORY_PATH.exists() else {}

def save_memory(m):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(json.dumps(m, indent=2))

def run_pipeline(niche, topic, tone="conversational", visual_style="cinematic dark dramatic", make_video=False):
    mem = load_memory()
    ctx = mem.get("channel_context", {})
    print(f"\n{'='*55}\n  YouTube Agent Pipeline\n  {niche} | {topic}\n{'='*55}\n")
    print("[1/4] RESEARCH...")
    r = research_agent.run(niche, topic, ctx)
    print(f"      Angle: {r.get('angle','')}")
    print("[2/4] SCRIPT...")
    s = script_agent.run(r, tone, ctx)
    print(f"      Title: {s.get('title','')}")
    print("[3/4] MEDIA...")
    m = media_agent.run(s)
    print("[4/4] PUBLISH...")
    p = publish_agent.run(s, m, ctx)
    OUTPUT_PATH.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe = s.get("title","output")[:40].replace(" ","_").replace("/","-")
    run_dir = OUTPUT_PATH / f"{ts}_{safe}"
    run_dir.mkdir(exist_ok=True)
    result = {"research":r,"script":s,"media":m,"publish":p}
    (run_dir / "data.json").write_text(json.dumps(result, indent=2))
    print(f"\n--- TITLE ---\n  {s.get('title','')}")
    print(f"\n--- A/B TITLES ---")
    for t in p.get("ab_test_titles",[]): print(f"  - {t}")
    print(f"\n--- CHECKLIST ---")
    for i,item in enumerate(p.get("checklist",[]),1): print(f"  {i}. {item}")
    print(f"\n--- PINNED COMMENT ---\n  {p.get('pinned_comment','')}")
    if make_video:
        print(f"\n{'='*55}\n  VIDEO GENERATION\n{'='*55}\n")
        print("[5] DIRECTOR - Writing visual prompts...")
        d = director_agent.run(s, visual_style)
        clips = d.get("clips", [])
        print(f"      {len(clips)} clips planned")
        thumb_file = run_dir / "thumbnail_prompt.txt"
        thumb_file.write_text(d.get("thumbnail_prompt",""))
        print(f"      Thumbnail prompt saved to: {thumb_file}")
        print("[6] VOICEOVER - ElevenLabs...")
        vp = voice_agent.run(s, str(run_dir))
        print("[7] VIDEO CLIPS - Veo 2 (takes 3-5 min)...")
        cp = video_agent.run(clips, str(run_dir))
        print("[8] ASSEMBLY - Stitching together...")
        fp = assembly_agent.run(cp, vp, str(run_dir), s.get("title","video"))
        result["director"] = d
        result["final_video_path"] = fp
        (run_dir / "data.json").write_text(json.dumps(result, indent=2))
        print(f"\n{'='*55}\n  DONE!\n  Video: {fp}\n  Folder: {run_dir}\n{'='*55}")
    else:
        print(f"\n{'='*55}\n  Script done! Saved to: {run_dir}\n  Add --video to generate the actual video\n{'='*55}")
    mem.setdefault("video_history",[]).append({"timestamp":datetime.now(timezone.utc).isoformat(),"title":s.get("title",""),"niche":niche})
    mem["video_history"] = mem["video_history"][-50:]
    save_memory(mem)
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--tone", default="conversational")
    ap.add_argument("--style", default="cinematic dark dramatic")
    ap.add_argument("--video", action="store_true")
    args = ap.parse_args()
    run_pipeline(args.niche, args.topic, args.tone, args.style, args.video)
