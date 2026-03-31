from pathlib import Path
from datetime import datetime
import exifread

def get_photo_date(image_path: Path) -> str:
  
    try:
        with open(image_path, 'rb') as f:
            # We use stop_tag to speed it up—it stops parsing once it finds the date
            tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
            
            if "EXIF DateTimeOriginal" in tags:
                date_str = str(tags["EXIF DateTimeOriginal"])
                # EXIF date format is standard: "YYYY:MM:DD HH:MM:SS"
                date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                
                # Format it to a clean string: "20260331"
                return date_obj.strftime("%Y%m%d")
                
    except Exception as e:
        print(f"Warning: Could not read EXIF date for {image_path.name}")
        
    # Fallback if the photo was downloaded from the internet and stripped of EXIF
    return "UnknownDate"


def get_safe_filepath(target_directory: Path, proposed_base_name: str, original_extension: str) -> Path:
    """
    Checks if a filename exists. If it does, appends _1, _2 safely.
    Example: NeonSign_Vibrant.JPG -> NeonSign_Vibrant_1.JPG
    """
    # Create the initial proposed path
    proposed_path = target_directory / f"{proposed_base_name}{original_extension}"
    
    # If the file doesn't exist, we are good to go!
    if not proposed_path.exists():
        return proposed_path
        
    # If it DOES exist, start the collision loop
    counter = 1
    while True:
        # Inject the counter before the extension
        new_path = target_directory / f"{proposed_base_name}_{counter}{original_extension}"
        
        if not new_path.exists():
            return new_path
            
        counter += 1