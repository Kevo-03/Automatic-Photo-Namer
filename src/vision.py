import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from PIL import Image

class ImageAnalyzer:
    def __init__(self):
        self.model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
        self.model, self.processor = load(self.model_path)
        self.config = load_config(self.model_path)
        self.prompt = """
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
    def analyze_image(self, image_path):
        img = Image.open(image_path)
        max_size = 512
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        image = [img]

        formatted_prompt = apply_chat_template(
            self.processor, self.config, self.prompt, num_images=len(image)
        )

        output = generate(self.model, self.processor, formatted_prompt, image, verbose=False)
        return output.text

