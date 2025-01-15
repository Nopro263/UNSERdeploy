from .models import Configuration

import yaml

def parse_text(data: str) -> Configuration:
    raw = yaml.safe_load(data)

    root = Configuration.model_validate(raw)
    return root