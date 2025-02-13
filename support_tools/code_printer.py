"""
    Модуль настройки вывода на печать сообщений с кодом (пайтон структуры (картежи, словари, списки и тд.).
    + изменение цвета и яркости служебных сообщений в консоли.


    # Примеры вывода текста с цветом и стилем (colorama):
    Создаем экземпляр класса init() один раз в одном месте, далее, все настройки будут доступны во всех модулях.

    print(Fore.RED + "This is red text" + Style.RESET_ALL)
    print(Fore.GREEN + "This is green text" + Style.RESET_ALL)
    print(Back.YELLOW + "Text with yellow background" + Style.RESET_ALL)
    print(Style.BRIGHT + "Bright text" + Style.RESET_ALL)
    print(Style.DIM + Fore.CYAN + "Dim cyan text" + Style.RESET_ALL)

    Автоматический сброс: autoreset=True (Чтобы не писать RESET_ALL после каждой строки) - \
    print(Fore.RED + "Red text without manual reset").

    В colorama эффект Style.DIM применяется только к тексту, а не к фону.
    Это значит, что, если вы комбинируете Style.DIM с Fore.GREEN и Back.BLACK,
    DIM будет влиять только на цвет текста, а фон останется неизменным.
"""

import pprint
from colorama import Fore, Back, Style, init

# ----------------------------------------------------------------------------------------------------------------------
# Настройки вывода кода в консоль (отступы и переносы):
beauty_code = pprint.PrettyPrinter(indent=8, width=118, compact=True)
# compact=True каждую элемент списка, кортежа или контейнера на новой строке,

# Инициализация colorama
init(autoreset=True)  #

RESET = Style.RESET_ALL  # c autoreset=True  - не нужно
# Подготовленные переменные для импорта в другие модули (чтобы их можно было использовать в других модулях):

# Текст:

# Обычные цвета:
RED = Fore.RED  # Используется для выделения важных или предупреждающих сообщений.
GREEN = Fore.GREEN  # Часто используется для успешных операций или позитивных уведомлений.
YELLOW = Fore.YELLOW  # Обычно применяется для предупреждений или информации, требующей внимания.
BLUE = Fore.BLUE
BLACK = Fore.BLACK

# Светлые версии:
LIGHTRED = Fore.LIGHTRED_EX  # Мягкая версия красного, подходит для менее агрессивных предупреждений.
LIGHTGREEN = Fore.LIGHTGREEN_EX  # Более мягкий и спокойный оттенок зеленого.
LIGHTYELLOW = Fore.LIGHTYELLOW_EX  # Пастельный оттенок желтого, подходит для менее ярких предупреждений.
LIGHTBLUE = Fore.LIGHTBLUE_EX
LIGHTBLACK = Fore.LIGHTBLACK_EX
LIGHTCYAN = Fore.LIGHTCYAN_EX
LIGHTGREEN = Fore.LIGHTGREEN_EX

# Фон:

# Обычные фоны:
BACK_BLACK = Back.BLACK  # "Черный фон"
BACK_RED = Back.RED  # "Красный фон"
BACK_GREEN = Back.GREEN  # "Зеленый фон"
BACK_YELLOW = Back.YELLOW  # "Желтый фон"
BACK_BLUE = Back.BLUE  # "Синий фон"
BACK_MAGENTA = Back.MAGENTA  # "Магента (пурпурный) фон"
BACK_CYAN = Back.CYAN  # "Голубой фон"
BACK_WHITE = Back.WHITE  # "Белый фон"

# Светлые фоны:
BACK_LIGHTBLACK = Back.LIGHTBLACK_EX  # "Светлый черный фон (теневой)"
BACK_LIGHTRED = Back.LIGHTRED_EX  # "Светлый красный фон"
BACK_LIGHTGREEN = Back.LIGHTGREEN_EX  # "Светлый зеленый фон"
BACK_LIGHTYELLOW = Back.LIGHTYELLOW_EX  # "Светлый желтый фон"
BACK_LIGHTBLUE = Back.LIGHTBLUE_EX  # "Светлый синий фон"
BACK_LIGHTMAGENTA = Back.LIGHTMAGENTA_EX  # "Светлый пурпурный фон"
BACK_LIGHTCYAN = Back.LIGHTCYAN_EX  # "Светлый голубой фон"
BACK_LIGHTWHITE = Back.LIGHTWHITE_EX  # "Светлый белый фон"

# Темные фоны:
BACK_DARKRED = Back.RED  # "Темный красный фон (эффект темной насыщенности)"
BACK_DARKGREEN = Back.GREEN  # "Темный зеленый фон"
BACK_DARKYELLOW = Back.YELLOW  # "Темный желтый фон"

# Яркость (для текста):
DIM_STYLE = Style.DIM  # Ууменьшает яркость текста.
BRIGHT_STYLE = Style.BRIGHT  # Увеличивает яркость текста (на практике текст становится жирнее,
# появляется едва заметная аура подсветки).


# Наборы тематических шаблонов:
ERROR_STYLE = RED + LIGHTYELLOW
WARNING_STYLE = YELLOW + BACK_DARKRED


def valid_type(check_key_type: any, inspect_value):
    if isinstance(check_key_type, bool):
        return check_key_type is inspect_value  # 'bool_type'

    elif isinstance(check_key_type, (int, str)):
        return check_key_type == inspect_value  # 'int_type'

    # elif isinstance(check_key_type, str):
    #     return check_key_type == inspect_value      # 'str_type'

    elif check_key_type is None:
        return check_key_type is inspect_value  # 'none_type'

    elif not isinstance(value, (bool, str, int,)) or value is not None:
        raise TypeError(f'Неверный тип данных переданного аргумента {value}')


# Функция вариации цвета по условию:
def coller(colored_text: str, inspect_value: bool | str | int | None, criterion: dict):
    """
        Красим текст если выполняется условие.
        inspect_value - проверяемая переменная.
        key - значение для проверки по условию.
        value - значение цвета для key.

        ***

        Пример:
        # Меняем цвет сообщения в консоли по условию:
        inspect_pattern = {True: GREEN, False: YELLOW, None: RED}
        new_color_text = coller(
            f'{check_is_deleted_employee}', check_is_deleted_employee, inspect_pattern
        )
        print(YELLOW + f'Результат проверки регистрации пользователя (tg_id: ' +
              BLUE + f'{user_tg_id}' + YELLOW + f'): ' + f'{new_color_text}')
    """
    new_color_text = colored_text  # Инициализируем переменную значением без изменений.

    for key, value in criterion.items():
        # if key == inspect_value:
        if valid_type(key, inspect_value):
            new_color_text = value + colored_text

    return new_color_text

#     # Выполняем если соответствует (color_text: str =):
#     return value + colored_text
#  например: строку с суммой красителей: авв = 'BRIGHT_STYLE + BACK_DARKRED', же в коде применять этот шаблон.
