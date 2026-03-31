import json

def clean_json_string(raw_text: str) -> str:
    """Strips markdown and conversational filler from LLM outputs."""
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


def parse_ai_output(raw_text: str) -> dict:
    """Safely converts the AI text into a dictionary, with fail-safes."""
    cleaned_text = clean_json_string(raw_text)
    
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        print(f"\nWarning: AI hallucinated invalid JSON. Skipping advanced tags.\nRaw text: {cleaned_text}")
        return {
            "subject": "UnknownSubject",
            "mood": "UnknownMood",
            "lighting": "UnknownLighting",
            "photography_principle": "None"
        }


def format_filename(tags: dict, date_str: str, template: str, casing: str = "pascal") -> str:
    """
    Injects the parsed tags into the user's template using their preferred casing.
    Example template: "{date}_{subject}_{mood}_{principle}"
    """
    
    def apply_casing(val: str, style: str) -> str:
        if not val or val.lower() == "none": 
            return ""
            
        clean_val = "".join(c for c in val if c.isalnum() or c.isspace())
        
        if style == "pascal":
            return clean_val.title().replace(" ", "")        # -> RuleOfThirds
        elif style == "snake":
            return clean_val.lower().replace(" ", "_")       # -> rule_of_thirds
        elif style == "upper":
            return clean_val.upper().replace(" ", "")        # -> RULEOFTHIRDS
        elif style == "lower":
            return clean_val.lower().replace(" ", "")        # -> ruleofthirds
        else:
            return clean_val.replace(" ", "")                # Default fallback

    formatted_tags = {
        "date": date_str,
        "subject": apply_casing(tags.get("subject", "Unknown"), casing),
        "mood": apply_casing(tags.get("mood", "Neutral"), casing),
        "lighting": apply_casing(tags.get("lighting", "Unknown"), casing),
        "principle": apply_casing(tags.get("photography_principle", "None"), casing)
    }

    try:
        base_name = template.format(**formatted_tags)
        
        base_name = base_name.replace("__", "_").replace("--", "-").strip("_-")
        
        return base_name
        
    except KeyError as e:
        print(f"\nWarning: Invalid template key {e}. Using default format.")
        return f"{formatted_tags['date']}_{formatted_tags['subject']}"