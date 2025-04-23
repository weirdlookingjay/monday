import requests
import dateparser
from django.conf import settings

API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
HF_API_KEY = getattr(settings, "HF_API_KEY", None)

def extract_entities(text):
    import logging
    if not HF_API_KEY:
        raise RuntimeError("Hugging Face API key not configured in Django settings (HF_API_KEY)")
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
        response.raise_for_status()
        raw_entities = response.json()
        logging.warning(f"[HF NER] Raw response: {raw_entities}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 503:
            logging.error(f"Hugging Face model is temporarily unavailable: {e}")
            return {"entities": [], "parsed_date": None, "error": "Hugging Face model temporarily unavailable (503)"}
        else:
            logging.error(f"Hugging Face API error: {e}")
            return {"entities": [], "parsed_date": None, "error": str(e)}
    except Exception as e:
        logging.error(f"Unknown error with Hugging Face API: {e}")
        return {"entities": [], "parsed_date": None, "error": str(e)}
    # Parse entities into {type, value} pairs, merging consecutive tokens for the same entity
    parsed_entities = []
    # Flatten if response is a list of lists
    entities_to_parse = raw_entities
    if isinstance(raw_entities, list) and len(raw_entities) == 1 and isinstance(raw_entities[0], list):
        entities_to_parse = raw_entities[0]
    if isinstance(entities_to_parse, list):
        current_entity = None
        current_type = None
        for ent in entities_to_parse:
            ent_type = ent.get('entity_group') or ent.get('entity')
            word = ent.get('word')
            if ent_type and word:
                if ent_type == current_type:
                    current_entity += word.replace('##', '')
                else:
                    if current_entity and current_type:
                        parsed_entities.append({'type': current_type, 'value': current_entity.strip()})
                    current_entity = word.replace('##', '')
                    current_type = ent_type
        if current_entity and current_type:
            parsed_entities.append({'type': current_type, 'value': current_entity.strip()})
    # Use dateparser to extract a date from the text
    parsed_date = dateparser.parse(text)
    # Detect board or task creation intent
    text_lower = text.lower()
    action = None
    if any(word in text_lower for word in ["create board", "new board", "add board"]):
        action = "create_board"
    elif any(word in text_lower for word in ["add task", "create task", "new task", "add", "task"]):
        action = "create_task"
    elif any(word in text_lower for word in ["remind", "review", "check", "look at", "monitor"]) and board_name:
        action = "review_board"
    else:
        # Heuristic: if there's a PERSON and a DATE, likely a task
        if parsed_entities and any(e['type'] == 'PER' for e in parsed_entities) and parsed_date:
            action = "create_task"
        else:
            action = "unknown"

    # Extract likely board name (ORG entity), assignee (PER), and task name (rest of text minus entities)
    board_name = next((e['value'] for e in parsed_entities if e['type'] in ["ORG", "MISC"]), None)
    assignee = next((e['value'] for e in parsed_entities if e['type'] == "PER"), None)

    # Remove entity words from text to guess task name
    task_name = text
    for ent in parsed_entities:
        task_name = task_name.replace(ent['value'], "")
    if parsed_date:
        task_name = task_name.replace(parsed_date.strftime('%B %d, %Y'), "")
    task_name = task_name.strip()

    return {
        "entities": parsed_entities,
        "parsed_date": parsed_date.isoformat() if parsed_date else None,
        "action": action,
        "board_name": board_name,
        "task_name": task_name if action == "create_task" else None,
        "assignee": assignee
    }
