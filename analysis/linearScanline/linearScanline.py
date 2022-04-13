from analysis.linearScanline.scanlineSelection import scanlineSelection
from read_write_joints.nodes2vector import nodes2vector


def linearScanline(nodes, info_scanline):
    vector = nodes2vector(nodes)

    # prompt = 'Automatic scanline estimation? \n -- 0:automatic \n -- 1:click 2 points  \n -- 2:1point and 1 orientation \n'
    # autoScanline_bool = input(prompt)
    autoScanline_bool = 0

    best_scanline = scanlineSelection(autoScanline_bool, nodes, info_scanline['nbScan'])

    # return [frequency, spacing_real, THETA]
