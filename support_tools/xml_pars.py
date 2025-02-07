"""
    parse_by_tags - не работает! Ошибка на этапе # Преобразуем строку в объект XML
        _xml_data = ET.fromstring(xml_array) -> print(f'_xml_data: {_xml_data.attrib}') -> {}.
        Пока не ясно почему. останавливаю работу.
    Принимает def count_product_request
"""

from xml.etree import ElementTree as ET



class ParsXML:

    @staticmethod
    def extract_namespaces_xml(xml_data, prefix_key: str = 'ns'):
        """Инициализация словаря пространств имен"""

        namespaces = {}

        # Перебор атрибутов элемента
        for attr, value in xml_data.attrib.items():
            # Проверяем, является ли атрибут пространством имен
            if attr.startswith('xmlns'):
                # Если атрибут является пространством имен без префикса
                if attr == 'xmlns':
                    # Добавляем пространство имен с заданным префиксом
                    namespaces[prefix_key] = value
                else:
                    # Если атрибут имеет префикс, мы разделяем его и добавляем в словарь
                    prefix = attr.split(':')[1]
                    namespaces[prefix] = value

        return namespaces


    def _parse_by_tags_old(self, xml_array, commands_structure: list):
        """
            Вспомогательный метод для рекурсивного разбора словаря тегов.

            Базовая структура для распознавания логикой:

                # ['url']['loc']
                * tag_structure = [{'findall': 'url'}, {'find': 'loc'}]

                ,где  management_key - ключ дает команду на вызов метода find или findall.

            Логика:
                Проходимся рекурсивно по структуре словаря и в зависимости от ключей управления "management_key"
                вызываем соответствующий метод. Результат сохраняем в список.
        """

        # Проверка на пустоту параметров
        if not xml_array or not commands_structure:
            raise ValueError(
                f'Ошибка, функция ожидает обязательные параметры: '
                f'"xml_array" - {xml_array} и "commands_structure" - {commands_structure} не могут быть пустыми.'
            )

        results = []
        temp = []

        # Преобразуем строку в объект XML
        _xml_data = ET.fromstring(xml_array)
        print(f'_xml_data: {_xml_data.attrib}')
        # Определяем пространство имен из корневого элемента
        # namespaces = {ns: v for ns, v in _xml_data.attrib.items()}
        namespaces = self.extract_namespaces_xml(_xml_data)
        print(f'namespaces: {_xml_data.attrib}')
        # Всего уровней тегов (глубина вложенности):
        count_sub_levels = len(commands_structure)

        # Добавляем объект XML в "стек" для переменных данных:
        temp.append(_xml_data)  # -> temp[0]

        # Каждый обход - это 1 уровень вложенности:
        for index, level in enumerate(commands_structure, start=1):

            # Проверка на соответствие структуры. Если это не dict, тогда:
            if not isinstance(level, dict):
                raise TypeError(
                    f'Ошибка, недопустимый тип данных элемента: {level} '
                    f'в массиве "commands_structure": {commands_structure}.'
                )

            # Распаковываем значения (метод и тег для поиска) для очередного уровня:
            for management_key, tag in level.items():

                # Перебираем все команды управления:
                # 1. ------------------------------- Если необходим поиск всех тегов в xml:
                if management_key == 'findall':

                    # Обращаемся к значению tag xml (например: 'url'):
                    # Используем findall для извлечения всех элементов:
                    elements_data = temp[0].findall(f'ns:{tag}', namespaces=namespaces)
                    print(f'elements_data: {elements_data}')
                    # ---------------------------------------- Извлечение данных по тегу:
                    # Если это конечная точка, подуровней нет, тогда:
                    if index == count_sub_levels:
                        print(f'count_sub_levels: {count_sub_levels}; index: {index}')
                        # Добавляем значение в список для результатов:
                        results.append(elements_data.text)

                    else:

                        # ------------------------- Перегружаем данные массива для последующего извлечения по тегу:
                        # Удаляем все исходные данные:
                        temp.clear()

                        # Добавляем значение в список для промежуточных результатов (без .text - повторный обход):
                        temp.append(elements_data)


                # 2. ------------------------------- Если необходим поиск только 1-го тега в xml:
                elif management_key == 'find':

                    # Обращаемся к промежуточному результату (предыдущие данные):
                    elements_data = temp[0]

                    # Перебираем. В большинстве случаем это будет массив после 'findall':
                    for element in elements_data:

                        # Обращаемся к значению elements_data xml (например: 'url'):
                        # Используем find для извлечения элемента:
                        sub_elements_data = element.find(f'ns:{tag}', namespaces=namespaces)
                        print(f'elements_data: {sub_elements_data}')

                        # ---------------------------------------- Извлечение данных по тегу:
                        # Если это конечная точка, подуровней нет, тогда:
                        if index == count_sub_levels:

                            # Добавляем значение в список для результатов:
                            results.append(sub_elements_data.text)

                            # Удаляем все исходные данные:
                            temp.clear()

                        else:

                            # ------------------------- Перегружаем данные массива для последующего извлечения по тегу:
                            # Удаляем все исходные данные:
                            temp.clear()

                            # Добавляем значение в список для промежуточных результатов (без .text - повторный обход):
                            temp.append(sub_elements_data)



                    # добавить очистку темп

                # 3. -------------------------------
                else:
                    raise ValueError(
                        f'Ошибка, недопустимое значение ключа: {management_key} '
                        f'в массиве "commands_structure": {commands_structure}.'
                    )

        return results