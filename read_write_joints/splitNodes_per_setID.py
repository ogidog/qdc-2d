def splitNodes_per_setID(nodes, setID):
    n = 1
    split_nodes = {'iD': [], 'x': [], 'y': [], 'nseg': [], 'norm': [], 'theta': [], 'wi': [], 'ori_w': [],
                   'ori_mean_deg': [], 'setiD': []}

    if 'setiD' in nodes.keys():
        for j in range(len(nodes['iD'])):
            if nodes['setiD'][j] == setID:
                split_nodes['iD'].append(n)
                split_nodes['x'].append(nodes['x'][j])
                split_nodes['y'].append(nodes['y'][j])
                split_nodes['nseg'].append(nodes['nseg'][j])
                split_nodes['norm'].append(nodes['norm'][j])
                split_nodes['theta'].append(nodes['theta'][j])
                split_nodes['wi'].append(nodes['wi'][j])
                split_nodes['ori_w'].append(nodes['ori_w'][j])
                split_nodes['ori_mean'].append(nodes['ori_mean'][j])
                split_nodes['ori_mean_deg'].append(nodes['ori_mean_deg'][j])
                split_nodes['setiD'].append(nodes['setiD'][j])
                n = n + 1

    return split_nodes
