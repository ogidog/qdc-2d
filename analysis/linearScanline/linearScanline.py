from analysis.linearScanline.scanlineSelection import scanlineSelection
from read_write_joints.nodes2vector import nodes2vector
from read_write_joints.plot_nodes import plot_nodes


def linearScanline(nodes, info_scanline):
    vector = nodes2vector(nodes)

    # TODO: uncomment
    # prompt = 'Automatic scanline estimation? \n -- 0:automatic \n -- 1:click 2 points  \n -- 2:1point and 1 orientation \n'
    # autoScanline_bool = input(prompt)
    autoScanline_bool = 0

    best_scanline = scanlineSelection(autoScanline_bool, nodes, info_scanline['nbScan'])
    Xsl = best_scanline['Xsl']
    Ysl = best_scanline['Ysl']
    Xb  = best_scanline['Xb']
    Yb  = best_scanline['Yb']

    plot_nodes(nodes)

    # return [frequency, spacing_real, THETA]
