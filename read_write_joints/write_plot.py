import base64
import io
import os
import sys

from matplotlib import pyplot

import workflow.workflow_config as wfc


def plot_to_base64(plt: pyplot, format: str, dpi: int):
    string_IO_bytes = io.BytesIO()
    plt.savefig(string_IO_bytes, format=format, dpi=dpi)
    string_IO_bytes.seek(0)
    base64_data = "data:image/" + format + ";base64," + base64.b64encode(string_IO_bytes.getvalue()).decode(
        "utf-8").replace("\n", "")

    return base64_data


def write_plot(plt, output="", dpi=300, format="png", **kwargs):
    if wfc.template['OUTPUT_TYPE'] == "file" and not output == "":
        out_file = output + os.path.sep + "fig" + plt.gcf().number + "_" + str(
            wfc.classif_joint_set_counter) + "." + format
        plt.savefig(out_file, dpi=dpi, format=format)

        return out_file

    elif wfc.template['OUTPUT_TYPE'] == "db":
        base64_data = plot_to_base64(plt, format, 200)

    elif wfc.template['OUTPUT_TYPE'] == "plot":
        plt.show(block=False)

    else:
        pass
