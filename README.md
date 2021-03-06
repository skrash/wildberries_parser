# О проекте
Данный проект реализован с использованием web-скрапера Scrapy, для удобства поиска внутри html использован BeautifulSoup и конечно для работы с javascript - selenium webdriver. Как источник прокси используется tor browser. Парсит wildberries по конкретным данным(цены, название товара, дата актуальности данных). Итог работы парсера - 2 таблицы:
* products содержащая название товара, цену, категорию, дату актуальности.
* urls содержащая url, по которому парсер прошёл для сбора информации, хэш md5 (идея добавления хэша была добавлена в перспективе для сравнения хэша из таблицы и при повторном запуске парсера, при совпадении хэшей не парсить страницу переходя далее по списку, но данная функциональность реализована не была), булевое значение того, была ли удачно обработана страница или необходимые теги не были найдены на странице, дата актуальности.
<br>
проект был заброшен, из-за низкой эффективности ввиду использования selenium и использования ожиданий догрузки контента.
<hr>

# Установка
1. Первым делом, конечно, необходимо установить Python 3.10 >= и пакетный менеджер pip, обновить pip до последней актуальной версии ```pip install --upgrade pip```
1. скачать подходящий geckodriver для работы selenium можно [здесь](https://github.com/mozilla/geckodriver/releases "mozilla geckodriver") и поместить его в папке /текущий_путь_до_папки_с_проектом/wildberries/
1. для настройки прокси соединениия используется tor browser [сслыка на оф сайт для скачивания](https://www.torproject.org/ru/download/), который также необходимо поместить в ту же директорию что и в предыдущем пункте. **Можно также в ручную отредактировать файл /wildberries/wildberries/piplines.py строки 29-31 содержащие пути к необходимым файлам на актуальные для вашей системы. Также для ОС linux возможно придется указать в 32 строке executable_path="./ваш_путь_к_geckodriver"**
1. перед использованием необходимо запустить хотя бы 1 раз tor browser и соединиться с сервером для создания необходимых профилей.
1. установить виртуальное окружение. ```python -m venv venv``` или ```python3 -m venv venv``` взависимости от ОС и окружения.
1. (необязательный пункт) обновить активировать виртуальное окружение ```./venv/Scripts/activate``` для windows или source ```./venv/bin/activate```
1. установить необходимые пакеты ```pip install -r req.txt```
1. если возникают проблемы при установке на linux подобных ОС, например (ERROR: Failed building wheel for twisted-iocpsupport), необходимо в ручную удалить в req.txt строчку twisted-iocpsupport==1.0.2
<hr>

# Запуск
1. ```cd wildberries```
1. ```scrapy crawl wb```
<hr>

# Проблемы с запуском.
Если вы используется ОС linux проверьте следующие
* права доступа к файлам корректны, необходимые файлы как например geckodriver имеют права на запуск.
* пути к файлам в файле /wildberries/wildberries/piplines.py строки 29-31 корректны. двойной обратный слэш заменен на одинарный /.
* пути к исполняемым файлам указаны со знаком .
