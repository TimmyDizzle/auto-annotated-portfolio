import os
from pathlib import Path
from google import genai
from google.genai import types

def run(thumbnail_prompt, output_dir):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    output_path = Path(output_dir) / "thumbnail.png"
    result = client.models.generate_images(
        model="imagen-3.0-generate-001",
        prompt=thumbnail_prompt,
        config=types.GenerateImagesConfig(aspect_ratio="16:9", number_of_images=1))
    output_path.write_bytes(result.generated_images[0].image.image_bytes)
    print(f"      Thumbnail saved: {output_path}")
    return str(output_path)
