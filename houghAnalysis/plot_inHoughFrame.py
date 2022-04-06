from read_write_joints.polylines_to_lines import polylines_to_lines
def plot_inHoughFrame(nodes):

    #Create Hough matrix from nodes
    nodes = polylines_to_lines(nodes)
