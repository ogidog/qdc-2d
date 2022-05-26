import workflow.workflow_config as wfc


def select_locale(en_txt: str, ru_txt: str):
    if wfc.template['LANG'] == 'ru':
        return ru_txt
    elif wfc.template['LANG'] == 'en':
        return en_txt
    else:
        return ''
