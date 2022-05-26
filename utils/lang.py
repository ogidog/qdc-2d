import utils.template as template


def select_locale(en_txt: str, ru_txt: str):
    if template.config['LANG'] == 'ru':
        return ru_txt
    elif template.config['LANG'] == 'en':
        return en_txt
    else:
        return ''
