# PhotoNamer: Autonomous AI Image File Renamer for Apple Silicon Macs

PhotoNamer is a fast, privacy-first CLI tool that uses local a Vision-Language Model (specifically Qwen2.5-VL) to analyze your photos and automatically rename them based on their visual composition, lighting, and mood. 

Built specifically for Apple Silicon using the MLX framework, it processes heavy RAW and JPEG files entirely offline—meaning your personal photos never leave your Mac.

## Features
* **True Visual Understanding:** Powered by Qwen2.5-VL, it looks at the image and extracts the subject, mood, lighting, and photographic principles.
* **100% Local & Private:** No API keys, no cloud uploads, no subscriptions. Everything runs on your own hardware.
* **Apple Silicon Optimized:** Uses Apple's native MLX framework for unified memory processing, keeping RAM usage perfectly stable even when processing thousands of photos.
* **Fail-Safe Dry Runs:** By default, the app runs in "Preview Mode" so you can see exactly how files will be renamed before altering your file system.
* **Highly Customizable:** Interactive wizard lets you build your naming template on the fly and choose your preferred casing (PascalCase, snake_case, UPPERCASE, lowercase).

---

## Installation

### Prerequisites
* A Mac with an Apple Silicon chip (M1/M2/M3/M4), at least 16GB of RAM is recommended.
* Python 3.10 or newer.

### For Photographers & End-Users (Recommended)
The safest and easiest way to install PhotoNamer globally is using `pipx`. This ensures the heavy AI dependencies don't conflict with your Mac's system files.

1. Install `pipx` via Homebrew (if you haven't already):
   ```bash
   brew install pipx
   pipx ensurepath
   ```
2. Clone this repository and install the app:
   ```bash
   git clone https://github.com/Kevo-03/Automatic-Photo-Namer.git
   cd Automatic-Photo-Namer
   pipx install .
   ```
   (You can safely delete the cloned folder after installation!)

### For Developers

If you want to modify the source code or contribute, install it in editable mode:

```bash
git clone https://github.com/Kevo-03/Automatic-Photo-Namer.git
cd Automatic-Photo-Namer
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

Navigate to any folder containing your photos (.jpg, .jpeg, .png, .nef) and simply run the command:

```bash
photonamer
```
The interactive wizard will guide you through the process:

1. **Fields:** Choose what information you want in the filename (Options: date, subject, mood, lighting, principle).
2. **Separator:** Choose how fields are connected (e.g., _ or -).
3. **Casing Style:** Format the text (pascal, snake, upper, lower).
4. **Execution:** Confirm if you want a safe dry-run (Preview) or a live execution.

### Architecture Under the Hood

- **Engine:** Apple mlx-vlm for hardware-accelerated inference.
-**Model:**  Qwen/Qwen2.5-VL-3B-Instruct for optimal speed-to-accuracy ratio.
-**Memory Management:** Implements isolated sequential processing. The 5GB AI model loads into unified memory exactly once, and Python's garbage collector destroys individual image tensors post-inference, preventing thermal throttling or RAM overflow during massive batch jobs.
**CLI Framework:** Built with Typer and Rich for a beautiful, type-safe terminal experience. 