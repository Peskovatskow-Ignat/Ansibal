import os
import gzip
import shutil
from datetime import datetime
from ftplib import FTP
import ipaddress
from dotenv import load_dotenv
import json
import subprocess

load_dotenv()

white_list = []  # Список IP-адресов, которые будут исключены из анализа
pull_ip = []  # Временный список для обработки IP-адресов из сетей

if 'whitelist.conf' in os.listdir():
    with open('whitelist.conf', 'r+') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Пропускаем пустые строки
            if '/' not in line:
                # Проверяем, является ли это одиночным IP-адресом
                try:
                    ipaddress.ip_address(line)  # Проверяем корректность IP-адреса
                    white_list.append(line)
                except ValueError:
                    print(f'Неверный IP-адрес: {line}')
            else:
                # Проверяем, является ли это подсетью
                try:
                    подсеть = ipaddress.ip_network(line, strict=False)
                    for ip in подсеть.hosts():
                        white_list.append(str(ip))
                except ValueError:
                    print(f'Неверная подсеть: {line}')
                except Exception as e:
                    print(f'Ошибка при обработке подсети {line}: {e}')



def delete_empty_files(directory_path: str):
    """
    Удаляет пустые файлы из указанной директории.

    Args:
    - directory_path (str): Путь к директории, в которой нужно удалить пустые файлы.
    """

    os.chdir(directory_path)  # Переходим в указанную директорию

    files = os.listdir(directory_path)  # Получаем список файлов в директории

    for file in files:
        file_path = os.path.join(directory_path, file)  # Полный путь к файлу

        # Проверяем, является ли элемент файлом и пуст ли он
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)  # Удаляем пустой файл



def clear():
    """
    Очищает временные файлы и каталоги.

    Очищает временные файлы и каталоги, созданные в процессе работы скрипта.
    """
    # Переходим на уровень выше от текущей директории
    os.chdir(os.path.join(os.getcwd(), '..'))

    # Удаляем временные каталоги
    shutil.rmtree('unpacked_files')  # Удаляем каталог с распакованными файлами
    shutil.rmtree('owasp')  # Удаляем другой временный каталог

    # Получаем файлы и директории внутри каталога 'arcive'
    files_and_directories_parent = os.listdir(os.path.join(os.getcwd(), 'arcive'))

    # Фильтруем .gz файлы для удаления
    gz_files = [f for f in files_and_directories_parent if (f.endswith('.gz') or ('.gz.' in f)) and not datetime.now().strftime("%Y%m%d") in f[f.find('_') + 1:f.find('_') + 9]]

    os.chdir('arcive')  # Переходим в каталог 'arcive'

    # Удаляем файлы, не соответствующие текущей дате
    for gz in gz_files:
        os.remove(gz)  # Удаляем файлы, не соответствующие заданной дате



def unpack():
    """
    Распаковывает файлы формата .gz.

    Распаковывает все архивированные файлы в формате .gz, находящиеся в указанной директории.
    """
    # Определение директорий и файлов
    current_directory = os.path.join(os.getcwd(), '..')  # Текущая директория скрипта
    parent_directory = os.path.join(current_directory, 'arcive')  # Родительская директория для архивов
    gz_files = [f for f in os.listdir(parent_directory) if f.endswith('.gz') or ('.gz.' in f)]  # Список .gz файлов

    # Подготовка каталога для распакованных файлов
    output_folder = os.path.join(current_directory, 'unpacked_files')  # Каталог для распакованных файлов
    if not os.path.exists(output_folder):  # Создание каталога, если он не существует
        os.makedirs(output_folder)

    # Распаковка файлов
    for gz_file in gz_files:
        gz_file_path = os.path.join(parent_directory, gz_file)  # Полный путь к .gz файлу
        unpacked_file_path = os.path.join(output_folder, os.path.splitext(gz_file)[0])  # Полный путь для распакованных файлов

        with gzip.open(gz_file_path, 'rb') as f_in, open(unpacked_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)  # Распаковка .gz файла и сохранение распакованных данных



def create_files():
    """
    Создает файлы для поиска ключевых слов в логах.

    Создает файлы на основе списка ключевых слов для последующего поиска и анализа в лог-файлах.
    """
    try:
        # Получение путей и создание каталога для результатов поиска
        current_directory = os.getcwd()
        default_path_dir = os.path.join(current_directory, '..')
        output_folder = os.path.join(default_path_dir, 'owasp')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        TARGET_DIR = os.path.join(default_path_dir, 'owasp')
        os.chdir(TARGET_DIR)

        # Списки ключевых слов и их названий для файлов
        keys = ['passwd', 'union\>', 'ldap', 'alert', 'select\>', 'cmd\>', 'xss\>', '\<script\>', 'etc\>', '\.\.\/',
                '\-\-\%', '\-\-', 'cookie', 'onload', 'onmouseover', 'whoami', 'net\%20user', 'metascan']

        names = ['passwd', 'union', 'ldap', 'alert', 'select', 'cmd', 'xss', 'script', 'etc', 'pp', 'dash%', 'dash',
                 'cookie', 'onload', 'onmouseover', 'whoami', 'net20user', 'metascan']

        logs = (os.path.join(default_path_dir, 'unpacked_files'))
        # Команды для поиска и записи результатов в файлы
        commands = [
            f'grep -E -i "{i}" {logs}/*.log | sed "s|{logs}/||" > {r}.txt' for i, r in zip(keys, names)
        ]

        for cmd in commands:
            print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: {cmd}')  # Для отладки выводим текущую команду
            subprocess.run(cmd, shell=True, check=True)  # Выполняем команду через subprocess
    except Exception as e:
        print(f"Произошла ошибка: {e}")



def write_files_data():
    """
    Записывает данные из файлов, исключая доверенные IP-адреса.

    Записывает данные из обработанных файлов в новые файлы, исключая информацию по доверенным IP-адресам.
    """
    ip_list = []  # Список для хранения IP-адресов
    list_file = os.listdir()  # Получаем список файлов в текущей директории

    for file in list_file:
        with open(file, 'r') as files:
            lines = files.readlines()  # Считываем строки из файла

        with open(file, 'w+') as f:
            for line in lines:
                key_word = '.log:'
                positions = line.find(key_word)  # Поиск позиции ключевого слова
                ip_list.append(line.split()[0][positions + len(key_word):])  # Добавляем IP в список

                # Проверка на наличие IP-адреса в списке доверенных IP-адресов
                if positions != -1 and line.split()[0][positions + len(key_word):] not in white_list:
                    f.writelines(line[positions + len(key_word):])  # Запись строки в файл без IP, если он не доверенный



def create_json():
    """
    Создает JSON-файл на основе обработанных данных.

    Формирует JSON-файл на основе собранных и обработанных данных из лог-файлов.
    """
    # Переходим к директории с обработанными файлами
    os.chdir(os.path.join(os.getcwd(), '..'))
    os.chdir(os.path.join(os.getcwd(), 'owasp'))

    owasp_dict = {}  # Словарь для хранения данных, которые будут преобразованы в JSON

    # Чтение данных из файлов и создание словаря
    for file in os.listdir():
        with open(file, 'r') as f:
            filename, file_extension = os.path.splitext(file)
            risk = filename

            if file_extension != '.txt':
                continue 

            if risk not in owasp_dict:
                owasp_dict[risk] = {}

            for line in f.readlines():
                split_line = line.split()  # Разбиение строки на части

                if len(split_line) < 9:
                    continue 

                if split_line[1] not in owasp_dict[risk]:
                    owasp_dict[risk][split_line[1]] = []

                # Заполнение списка событий данными из файла
                owasp_dict[risk][split_line[1]].append({
                    'ip_address': split_line[0],
                    'date': split_line[2][1:split_line[2].find(':')],
                    'time': split_line[2][split_line[2].find(':') + 1:],
                    'method': split_line[4][1:],
                    'port': split_line[-1],
                    'url': split_line[5] if not ('.png' or 'img')  in split_line[5] else None,
                    'version_protocol': split_line[6][:split_line[6].find('"')],
                    'status_code': split_line[7],
                    'use_cache': split_line[8] if split_line[8] != '-' else 'use_cache',
                    'country': split_line[-3] if not '"' in split_line[-3] else '-'
                })

    # Проверка и удаление пустых значений
    keys_to_delete = [key for key in owasp_dict if not owasp_dict[key]]
    for key in keys_to_delete:
        del owasp_dict[key]

    # Возврат к исходной директории и сохранение данных в JSON-файл
    os.chdir(os.path.join(os.getcwd(), '..'))
    os.chdir(os.path.join(os.getcwd(), 'new_parser'))
    with open('/opt/data_files/metascan_logs.json', 'w') as f:
        json.dump(owasp_dict, f, indent=5)  # Запись словаря в файл в формате JSON с отступами


def check_rar() -> list:
    """
    Проверяет наличие файлов в директории.

    Проверяет текущую директорию на наличие определенных файлов.
    """

    return os.listdir()  # Возвращает список файлов в текущей директории



def download_log(data: str):
    """
    Загружает журналы (логи) с FTP-сервера.

    Args:
    - data (str): Дата, для которой необходимо загрузить журналы в формате YYYYMMDD.
    """

    os.chdir(os.path.join(os.getcwd(), '..'))  # Переход на уровень выше в иерархии папок
    archive_directory = os.path.join(os.getcwd(), 'arcive')

    if not os.path.exists(archive_directory):
        os.makedirs(archive_directory)

    os.chdir(archive_directory)

    # Установка соединения с FTP-сервером и аутентификация
    ftp = FTP(os.getenv('server'))
    ftp.login(user=os.getenv('user'), passwd=os.getenv('password'))
    ftp.cwd('/logs')  # Переход на сервере в директорию с логами

    ready_rar = check_rar()  # Получение списка файлов в текущей директории

    # Цикл по директориям на FTP-сервере
    for dirs in ftp.nlst():
        ftp.cwd(dirs)  # Переход в текущую директорию
        # Цикл по файлам в текущей директории на FTP-сервере
        for file in ftp.nlst():
            # Проверка соответствия даты в имени файла и его отсутствия в локальной директории
            if data in file[file.find('_') + 1:file.find('_') + 9] and file not in ready_rar:
                try:
                    with open(file, 'wb') as local_file:
                        ftp.retrbinary('RETR ' + file, local_file.write)
                    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: download -', file)  # Вывод информации о загрузке файла
                    # Загрузка файла с FTP-сервера и сохранение локально
                except:
                    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Не удалось загурузть файл {file}')

        ftp.cwd('..')  # Переход на уровень выше в директории на FTP-сервере

    ftp.quit()  # Закрытие соединения с FTP-сервером

    # Возврат в исходную директорию скрипта
    os.chdir(os.path.join(os.getcwd(), '..'))
    os.chdir(os.path.join(os.getcwd(), 'new_parser'))



if __name__ == '__main__':
    print("=" * 50, f'START {datetime.now().strftime("%dd %mm %Yy %H:%M:%S")} (GMT+03:00)', "=" * 50)
    download_log(datetime.now().strftime("%Y%m%d"))
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Installation of files was successful')
    unpack()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: All files are unpacked')
    create_files()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Configuration files created successfully')
    delete_empty_files(os.getcwd())
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Removal of unnecessary files completed successfully')
    write_files_data()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: All trusted IP addresses are excluded')
    create_json()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: json generation completed successfully')
    clear()
    print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Removing unnecessary files')
    print("=" * 50, f'PARSE {datetime.now().strftime("%dd %mm %Yy %H:%M:%S")} (GMT+03:00)', "=" * 50)
