def compute_Jv(w):
    spacing = w[:, 1]

    Jv = 0
    for s in range(len(spacing)):
        Jv = Jv + 1 / spacing[s]

    print(
        'The volumetric joint count : Nb of joints intersecting a volume of rock mass (Nb of joints per surface unit)')
    print('Volumetric joint count : {}'.format(Jv))
