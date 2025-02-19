<a id="readme-top"></a>
<!-- PROJECT MAIN LOGO | ГЛАВНОЕ ЛОГО ПРОЕКТА С КРАТКИМ ОПИСАНИЕМ -->
<div style="text-align: center;">

[![Product main_logo][main_logo]](https://github.com/ArtemXYZ/mv_pars)

</div> 
<!-- PROJECT SHIELDS | ШИЛЬДИКИ-ССЫЛКИ -->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


</div>

<!-- ABOUT THE PROJECT -->
## About The Project

    This is a custom library designed for parsing (via API) 
    the range of goods by branches and categories of the household retail chain 
    techniques of M.Video.

  #### Верхнеуровневая логика: 

  1. Collecting and processing categories from sitemap:
     - https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml.
     

  2. Collecting data on current branches.


  3. Bypassing branches.


  4. Category traversal for each branch:
     - (collection and processing of product availability data (SKU) for a category).
  

  5. Processing the results and saving them to the database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

```python
from parser_04_vers import MvPars

# Initializing a class does not require explicitly passing arguments.
pars = MvPars()
```
```python
"""
    MvPars() имеет интуитивно понятный интерфейс реализованный по принципу функционального разделения: 
                                                ***
        * Существует всего три основных "менеджера", каждый из которых, отвечает за свою область функционала
        и содержит соответствующие методы. Данная концепция реализована через цепочки вызовов для удобства.
"""

pars = MvPars()

# Менеджер "info" содержит все методы предоставляющие данны о текущем состоянии параметров парсера:
pars.info 

# Менеджер "set" содержит все методы позволяющие устанавливать новые значения параметров парсера:
pars.set

# Менеджер "activate" содержит все основные методы управления и запуска парсером:
pars.activate
```
## _Manager "info"_

```python
"""
    Большинство методов в менеджере "info" реализовано как @property и являются гетторами.
"""

pars = MvPars()


# Возвращает заданное количество попыток для повторного подключения, в случае сбоев (обрыв соединения и тд.).
result = pars.info.get_retries

# Возвращает заданный промежуток времени между повторными подключениями, в случае сбоев (обрыв соединения и тд.).
result = pars.info.get_timeout

# Возвращает экземпляр подключения к базе данных.
result = pars.info.get_connect

# Возвращает имя таблицы в базе данных определенную по умолчанию для сохранения результатов парсинга. 
# :param: params_for_table_tag = 'history' or 'catalog'.
result = pars.info.get_name_table(self, table_tag)

# Возвращает имя схемы, где хранится таблица, определенная по умолчанию для сохранения результатов парсинга.
# :param: params_for_table_tag = 'history' or 'catalog'.
result = pars.info.get_schem(self, table_tag)

# Возвращает текущие значения переменной CITY_DATA (набор исходных данных, необходимый для работы методов парсера.
result = pars.info.get_city_data

# Возвращает текущие значения имени папки для сохранения результатов работы парсера
result = pars.info.get_base_folder

# Возвращает текущие значения заголовков (предназнаячены для корректной работы запросов через requests,  
# сайт определяет запрос, как отпользователя в браузере, а не скрипт).
result = pars.info.get_headers

# Возвращает текущие значения имен для итоговых выходных файлов метода получения филиалов.
result = pars.info.get_unified_names_files_for_branches

# Возвращает текущее значения имен итоговых выходных файлов метода получения категорий.
result = pars.info.get_unified_names_files_for_category

# Возвращает текущие значение пути для сохранения дампа данных по филиалам.
result = pars.info.get_path_file_branch_dump

# Возвращает текущее значение пути для сохранения дампа данных по категориям.
result = pars.info.get_path_file_category_dump

# Возвращает текущие значения имитации задержки (минимальные и максимальные границы).
result = pars.info.get_ping_limits

# Возвращает рандомную задержку.
result = pars.info.get_time_sleep_random
```

## _Manager "set"_  

```python
"""
    Методы в менеджере "set" имеют противоположную логику методов в "info" 
    и позволяют устанавливать новые значения не прибегая к изменению кода. 
    Это позволяет гибко осуществлять работу, если вдруг не требуется стандартный цикл парсинга.
"""

pass

```

## _Manager "activate"_

```python
"""
    Менеджер "activate" являются основным и предназначен для предоставления методов управления различными вариантами
    запуска парсинга, в том числе и низкоуровневых для частных случаев (например, таких, как работа с результатами 
    для каждой из целевых таблиц, управлением запуска по рассписанию или запуск в ручную и др.
"""

from parser_04_vers import MvPars

# Если необходимо в ручном режиме запустить полный цикл парсинга pars.activate.run_one_cycle_pars(load_damp=True)
# Параметр load_damp=True указывает на то, что необходимо будет загрузить дамп предыдущего парсинга филиалов,
# а не парсить заново и наоборот, для обновления данных, можно не указывать данный флаг,по умолчанию load_damp=False.
pars.activate.run_one_cycle_pars(load_damp=True)

# Парсинг кодов магазинов и адресов, необходимых для основго запроса на получение информации о товарах.
result = pars.activate.get_branches_dat()

pass
```




<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Libraries used
  
    This tool uses both auxiliary libraries:

   * ```SQLAlchemy```
   * ```APScheduler```
   * ```requests```
   * ```urllib```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

* Distributed under the MIT License. See [`LICENSE`][license-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

  - Telegram - [ArtemP_khv](https://t.me/ArtemP_khv)

<!-- back to top | На верх -->
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES |  Ссылки на ресурсы (переменные для вставки в шаблоне документа) -->

[contributors-shield]:  https://img.shields.io/github/contributors/ArtemXYZ/mv_pars.svg?style
[contributors-url]: https://github.com/ArtemXYZ/mv_pars/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ArtemXYZ/mv_pars.svg?style
[forks-url]: https://github.com/ArtemXYZ/mv_pars/network/members
[stars-shield]: https://img.shields.io/github/stars/ArtemXYZ/mv_pars.svg?style
[stars-url]: https://github.com/ArtemXYZ/mv_pars/stargazers
[issues-shield]: https://img.shields.io/github/issues/ArtemXYZ/mv_pars.svg?style
[issues-url]: https://github.com/ArtemXYZ/mv_pars/issues

<!-- License | Лицензия -->
[license-shield]: https://img.shields.io/github/license/ArtemXYZ/mv_pars.svg?style
[license-url]: https://github.com/ArtemXYZ/mv_pars/blob/master/LICENSE.txt

<!-- Logo | Лого  + [product-screenshot]: -->
[main_logo]: docs/images_project/logo.png
[logo_mini]: docs/images_project/lg.png

[//]: # (    Ссылка на репозиторий https://github.com/ArtemXYZ/mv_pars.git )
[//]: # (_For more examples, please refer to the [Documentation]&#40;https://example.com&#41;_)