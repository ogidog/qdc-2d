import json
import os

from utils import template


def write_json(content: dict, output: str):
    if template.config['OUTPUT_TYPE'] == "file":

        if not os.path.exists(output):
            os.makedirs(output)

        content_json = json.dumps(content, indent=2, ensure_ascii=False)
        with open(output + os.path.sep + "brief_" + str(
                template.classif_joint_set_counter) + ".json", 'w') as f:
            f.write(content_json)
            f.close()
    elif template.config['OUTPUT_TYPE'] == "db":
        pass
    elif template.config['OUTPUT_TYPE'] == "plot":
        pass
    else:
        pass
