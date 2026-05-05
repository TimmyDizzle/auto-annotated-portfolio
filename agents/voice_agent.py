import os
from pathlib import Path
from elevenlabs.client import ElevenLabs

def run(script, output_dir, voice_id="21m00Tcm4TlvDq8ikWAM"):
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    parts = [script.get("hook", "")]
    for s in script.get("sections", []):
        parts.append(s.get("content", ""))
    parts.append(script.get("outro", ""))
    full_text = "\n\n".join(p for p in parts if p)
    output_path = Path(output_dir) / "voiceover.mp3"
    audio = client.text_to_speech.convert(
        voice_id=voice_id, text=full_text,
        model_id="eleven_turbo_v2_5", output_format="mp3_44100_128")
    with open(output_path, "wb") as f:
        for chunk in audio: f.write(chunk)
    print(f"      Voiceover saved: {output_path}")
    return str(output_path)
