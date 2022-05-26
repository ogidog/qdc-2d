import json


def write_json(content: dict, file_path: str):
    content_json = json.dumps(content, indent=2, ensure_ascii=False)
    with open(file_path, 'w') as f:
        f.write(content_json)
        f.close()
