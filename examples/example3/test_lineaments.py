import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def main():
    lines_coord = {"lx1": [], "lx2": [], "ly1": [], "ly2": []}
    lines_file = "D:\\intellij-idea-workspace\\qdc-2d\\TEMPLATES\\examples2\\C1M.txt"
    img_file = "D:\\intellij-idea-workspace\\qdc-2d\\TEMPLATES\\examples2\\02-11-2019_cut_pwr_ql.png"

    f = open(lines_file)
    while True:
        line = f.readline().strip()
        if line == "":
            f.close()
            break
        [lx1, ly1, lx2, ly2] = np.array(line.split(";"), dtype="int")
        lines_coord['lx1'].append(lx1)
        lines_coord['lx2'].append(lx2)
        lines_coord['ly1'].append(ly1)
        lines_coord['ly2'].append(ly2)
    f.close()

    plt.figure(1)
    for i in range(len(lines_coord['lx1'])):
        plt.plot([lines_coord['lx1'][i], lines_coord['lx2'][i]], [lines_coord['ly1'][i], lines_coord['ly2'][i]], "b-",
                 linewidth=0.3)

    im = Image.open(img_file)
    im_size = im.size
    im_data = np.array(im.getdata(0)).reshape(tuple(reversed(im_size)))
    plt.imshow(im_data, aspect="auto", cmap="gray")

    plt.show()


if __name__ == "__main__":
    main()
