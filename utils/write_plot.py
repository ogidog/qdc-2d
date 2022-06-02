import base64
import io
import os
import matplotlib.pyplot as plt

import utils.template as template


def plot_to_base64(format: str, dpi: int):
    string_IO_bytes = io.BytesIO()
    plt.savefig(string_IO_bytes, format=format, dpi=dpi)
    string_IO_bytes.seek(0)
    base64_data = "data:image/" + format + ";base64," + base64.b64encode(string_IO_bytes.getvalue()).decode(
        "utf-8").replace("\n", "")

    return base64_data


def write_plot(output, dpi=300, format="png"):
    if template.config['OUTPUT_TYPE'] == "file":
        out_file = output + os.path.sep + "fig" + str(plt.gcf().number) + "_" + str(
            template.classif_joint_set_counter) + "." + format
        plt.savefig(out_file, dpi=dpi, format=format)
        plt.close()

        return out_file

    elif template.config['OUTPUT_TYPE'] == "db":
        base64_data = plot_to_base64(plt, format, 200)

    elif template.config['OUTPUT_TYPE'] == "plot":
        plt.show(block=False)

    else:
        pass
