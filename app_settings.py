"""User-editable identity and sharing preferences, independent of conversion."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

DEFAULTS = {
    'developer_name': 'Progress Ajayi',
    'developer_bio': 'Developer of Excel to Prism Studio.',
    'professional_url': '',
    'share_url': 'https://github.com/ajayiprogress04-ctrl/excel-to-prism-studio/releases',
    'theme': 'Light',
}

def validate_url(value):
    value = value.strip()
    if not value:
        return ''
    try:
        parsed = urlsplit(value)
        valid = (parsed.scheme in {'http', 'https'} and parsed.hostname
                 and not parsed.username and not parsed.password
                 and not any(c.isspace() for c in value))
        if not valid:
            raise ValueError()
        _ = parsed.port
    except ValueError:
        raise ValueError('Use a complete http:// or https:// web address without credentials.') from None
    return value

def settings_path():
    base = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.local' / 'share'))
    return base / 'ExcelToPrismStudio' / 'settings.json'

def load_settings():
    result = DEFAULTS.copy()
    try:
        data = json.loads(settings_path().read_text(encoding='utf-8'))
        if isinstance(data, dict):
            result.update({k:v for k,v in data.items() if k in result and isinstance(v,str)})
    except (OSError, ValueError):
        pass
    return result

def save_settings(values):
    data = {key: str(values.get(key, default)) for key,default in DEFAULTS.items()}
    data['share_url'] = validate_url(data['share_url'])
    data['professional_url'] = validate_url(data['professional_url'])
    if not data['developer_name'].strip():
        raise ValueError('Enter a developer name.')
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(path)
    return data
