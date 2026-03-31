from pathlib import Path
from datetime import datetime
import exifread

def get_photo_date(image_path: Path) -> str:
  
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
            
            if "EXIF DateTimeOriginal" in tags:
                date_str = str(tags["EXIF DateTimeOriginal"])
                date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                
                return date_obj.strftime("%Y%m%d")
                
    except Exception as e:
        print(f"Warning: Could not read EXIF date for {image_path.name}")
        
    return "UnknownDate"


def get_safe_filepath(target_directory: Path, proposed_base_name: str, original_extension: str) -> Path:
    """
    Checks if a filename exists. If it does, appends _1, _2 safely.
    Example: NeonSign_Vibrant.JPG -> NeonSign_Vibrant_1.JPG
    """
    proposed_path = target_directory / f"{proposed_base_name}{original_extension}"
    
    if not proposed_path.exists():
        return proposed_path
        
    counter = 1
    while True:
        new_path = target_directory / f"{proposed_base_name}_{counter}{original_extension}"
        
        if not new_path.exists():
            return new_path
            
        counter += 1