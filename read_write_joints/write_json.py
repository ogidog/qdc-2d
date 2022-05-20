import json


def write_json(content: dict, file_path: str):
    content_json = json.dumps(content, ensure_ascii=False, indent=4)
    with open(file_path, 'w') as f:
        f.write(content_json)
        f.close()
