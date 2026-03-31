import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from PIL import Image
import json
from pathlib import Path

def clean_json_string(raw_text):
    text = raw_text.strip()
    
    if text.startswith("```json"):
        text = text[7:] 
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3] 
        
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        return text[start_idx:end_idx+1]
        
    return text.strip()

model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
model, processor = load(model_path)
config = load_config(model_path)

image_path = "/Users/kivanc/Desktop/Reflection/DSC_1008.JPG"
og_extension = Path(image_path).suffix
img = Image.open(image_path)
max_size = 512
img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
image = [img]
prompt = """
Analyze this image and extract its core visual characteristics. 
You must output your response ONLY as a valid, parsable JSON object. 
Do not include any conversational text, explanations, or markdown formatting (like ```json).

Use the following exact JSON schema:
{
  "subject": "A 1-3 word description of the main subject (e.g., Galata Tower, Neon Sign, Golden Retriever)",
  "mood": "A 1-2 word description of the emotional vibe or atmosphere (e.g., Vibrant, Moody, Melancholic, Uplifting)",
  "lighting": "A 1-2 word description of the lighting condition (e.g., Golden Hour, Neon, Harsh, Soft, Low Key)",
  "photography_principle": "The dominant photographic technique or composition rule used (e.g., Rule of Thirds, Reflection, Motion Blur, Bokeh, Symmetry, Leading Lines)"
}
"""

formatted_prompt = apply_chat_template(
    processor, config, prompt, num_images=len(image)
)

output = generate(model, processor, formatted_prompt, image, verbose=False)

raw_text = output.text

cleaned_text = clean_json_string(raw_text)

try:
    tags = json.loads(cleaned_text)
    
    subject = tags.get("subject", "Unknown").title().replace(" ", "")
    mood = tags.get("mood", "Neutral").title().replace(" ", "")
    principle = tags.get("photography_principle", "None").title().replace(" ", "")
    
    new_filename = f"{subject}_{mood}_{principle}{og_extension}"
    print(f"\nSuccessfully parsed! Proposed filename: {new_filename}")

except json.JSONDecodeError:
    print(f"\nError: Failed to parse JSON even after cleaning.\nCleaned Text: {cleaned_text}")
