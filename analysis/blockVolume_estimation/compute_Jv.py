import workflow.lang as lang
import workflow.workflow_config as wfc


def compute_Jv(w):
    spacing = w[:, 1]

    Jv = 0
    for s in range(len(spacing)):
        Jv = Jv + 1 / spacing[s]

    print(lang.select_locale(
        'The volumetric joint count : Nb of joints intersecting a volume of rock mass (Nb of joints per surface unit)',
        'Кол-во линий по объему - количество линий на единицу поверхности'))

    print(lang.select_locale('Volumetric joint count : {}', 'Количество линий на единицу поверхности : {}').format(Jv))
    wfc.volume_brief[lang.select_locale('Volumetric joint count', 'Количество линий на единицу поверхности')] = Jv
