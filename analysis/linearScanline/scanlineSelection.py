from analysis.linearScanline.find_best_scanline import find_best_scanline


def scanlineSelection(selectNB, nodes, nbScan):

    # Scanline-PROCESSING
    if selectNB == 0:
        print("-- Scanline AUTO --")
        scanline = find_best_scanline(nodes, nbScan) #automatic scanline selection

    return scanline