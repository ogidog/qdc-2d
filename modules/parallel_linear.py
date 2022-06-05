from utils import lang, template


def parallel_linear(joints_source: str = None):

    print(lang.select_locale('Analyse with parallel linear','Анализ - Метод параллельных сканирующих линий'))
    template.parallel_linear_brief[lang.select_locale('Method', 'Модуль')] = lang.select_locale('Analyse with parallel linear','Анализ - Метод параллельных сканирующих линий')

    pass