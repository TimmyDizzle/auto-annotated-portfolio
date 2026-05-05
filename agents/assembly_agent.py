from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def run(clip_paths, voiceover_path, output_dir, title):
    clips = []
    for clip_info in clip_paths:
        vc = VideoFileClip(clip_info["path"])
        if clip_info.get("caption"):
            txt = (TextClip(clip_info["caption"], fontsize=52, color="white",
                stroke_color="black", stroke_width=2, font="Arial-Bold",
                method="caption", size=(vc.w - 120, None))
                .set_position(("center", 0.85), relative=True)
                .set_duration(vc.duration))
            vc = CompositeVideoClip([vc, txt])
        clips.append(vc)
    final = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(voiceover_path)
    if final.duration > audio.duration:
        final = final.subclip(0, audio.duration)
    final = final.set_audio(audio.subclip(0, min(audio.duration, final.duration)))
    out = Path(output_dir) / f"{title[:40].replace(' ','_')}_FINAL.mp4"
    final.write_videofile(str(out), fps=24, codec="libx264", audio_codec="aac",
        temp_audiofile="temp_audio.m4a", remove_temp=True, logger=None)
    print(f"      Final video: {out}")
    return str(out)
