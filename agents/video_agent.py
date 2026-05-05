import os, time
from pathlib import Path
from google import genai
from google.genai import types

def generate_clip(client, prompt, duration_seconds, output_path):
    op = client.models.generate_videos(
        model="veo-2.0-generate-001", prompt=prompt,
        config=types.GenerateVideoConfig(aspect_ratio="16:9", duration_seconds=duration_seconds, enhance_prompt=True))
    print(f"        Waiting for Veo 2...", end="", flush=True)
    while not op.done:
        time.sleep(15)
        op = client.operations.get(op)
        print(".", end="", flush=True)
    print(" done")
    Path(output_path).write_bytes(op.result.generated_videos[0].video.video_bytes)
    return output_path

def run(clips, output_dir):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    output_dir = Path(output_dir)
    clip_paths = []
    for i, clip in enumerate(clips):
        print(f"      Clip {i+1}/{len(clips)}: {clip['segment']}")
        out = output_dir / f"clip_{i:02d}.mp4"
        generate_clip(client, clip["prompt"], clip.get("duration_seconds", 8), out)
        clip_paths.append({"path": str(out), "caption": clip.get("caption", ""), "segment": clip["segment"]})
    return clip_paths
