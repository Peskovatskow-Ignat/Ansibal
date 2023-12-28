<!DOCTYPE html>
<html>
  <body>
    <img align="right" alt="Coding" width="350" src="https://user-images.githubusercontent.com/113009998/233772381-b051a566-85af-4f28-a6e1-5aa209f37318.png">
    <h1>Parser Folder</h1>
    <p>Данный микросервис предназначен для сбора и анализ информации. Уставка и запуска процессов происходит с помощью Ancible . В каждой папке хранится своё приложение</p>
    <h2>Содержание</h2>
    <ul>
      <li><a href="#ansible">Ansible</a></li>
      <li><a href="#ddos">Folder ddos-log-parser</a></li>
      <li><a href="#mail">Folder mail-ban-parser</a></li>
      <li><a href="#web_server">Folder web_server</a></li>
      <li><a href="#data_files">Folder data_files </a></li>
      <li><a href="#bot">Folder data_files </a></li>
      <li><a href="#end">Заключение</a></li>
    </ul>
    <h1 id="ansible">Ansible</h1>
    <p>Этот проект содержит набор задач <a href="https://habr.com/ru/articles/305400/">Ansible</a> для быстрой настройки окружения на удаленной машине. Он автоматизирует создание необходимых директорий, установку Python и драйверов, создание виртуальных сред для приложений, копирование файлов и служб, назначение прав доступа и запуск сервисов. При запуске потребуется <a href="https://t.me/IgnatPesk">пароль</a>.</p>
    <h3>Состав</h3>
    <ul>
      <li><code>/template:</code> Директория которая хранит все необходимые файлы и директории</li>
      <li><code>secrets.yml:</code> Файл в  котором храняться зашифорванные данные для дальнейшего создания .env</li>
      <li><code>main.yaml</code> Файл который содержит необходимы playbook для установки</li>
    </ul>
    <h3>Команда установки Ansibal<h3>
    <ul>
    <pre><code>sudo apt update && sudo apt install ansible</code></pre>
    </ul>  
    <h3>Пример заполенине файла secrets.yml до того как его зашифровать</h3>
    <pre><code>api_hash: "api_hash" --> str
bot_token: "bot_token" --> str
ip: "0.0.0.0" --> str
port: port --> int
server: "resource FTP link" --> str
user: "username" --> str
password: "passwd" --> str</code></pre>
    </ul>
    <h3>Команда запуска<h3>
    <ul>
    <pre><code>ansible-playbook --ask-vault-pass main.yaml</code></pre>
    </ul>
    <h1 id="ddos">ddos-log-parser</h1>
    <p>Данное приложение скачивает и сохраняет архивы за отределённое число ( можно указать любой день в самом скрипте но щас он работает на числа данного дня) с <a href="https://ru.wikipedia.org/wiki/FTP">FTP</a> сервера и далее по регулярным выражениям происходит выборка возможных инцидентов. Сохранение данных происхоить в директорию <a href="#data_files" >data_file</a>. Запуск данного скрипта происходит каждый час в 30 минут (Пример: 13:30)</p>
    <h3>Состав</h3>
    <ul>
      <li><code>start.sh:</code> Отвечает за запуск программы с активацией venv</li>
      <li><code>/arcive:</code> Директория которая содержит предназначена для хранения архивов за день</li>
      <li><code>/logs:</code> Директория которая содержит логи исполняемой программы </li>
      <ul>
       <li><code>cron.log:</code> Файл котоырй содержит данные о аыполнение программы</li>
       </ul>
<li><code>/new_parser:</code> Директория в которой находятся файлы конфигурации и сама программа
      <ul>
        <li><code>unpacket_arcive.py</code> Скрипт которые выполянет основную логику программы </li>
        <li><code>.env:</code> Файл конфигурации в которм хранятся чувствительные данные</li>
        <li><code>whitelist.conf:</code> Файл конфигурации в котором хрантся ip адреса или подсети которые считаются доверенными </li>
      </ul>
      <li><code>requirements.txt:</code> Файл который содержит необходиме библиотеки для запуска скрипта</li>
</li>
    </ul>
    <h3>Пример заполнения .env</h3>
    <ul>
    <li>server = Ссылка на ресурс</li> 
    <li>user = Имя пользователя</li> 
    <li>password = Пароль </li>
    </ul>
    <h1 id="mail">Mail-ban-parser</h1>
    <p>Данное приложение обращается на web сервис <a href="https://mxtoolbox.com/">Mxtoolbox</a> для проверки доменов почт, котрые попали в чёрные листы определённых сервисов. Сохранение данных происхоить в директорию <a href="#data_files" >data_file</a>. Запуск данного скрипта происходит в периуд с 7:45 до 17:45 каждый час в 45 минут (Пример: 13:45)</p>
    <h3>Состав</h3>
    <ul>
      <li><code>start.sh:</code> Отвечает за запуск программы с активацией venv</li>
       <li><code>cron.log:</code> Файл котоырй содержит данные о выполнение программы</li>
       <li><code>main.py:</code> Скрипт которые выполянет основную логику программы</li>
<li><code>doamin.conf:</code> Файл конфигрурации который содержит доменные имена для проверки</li>
      <li><code>requirements.txt:</code> Файл который содержит необходиме библиотеки для запуска скрипта</li>
</li>
    </ul>
    <h1 id="web_server">Web_server</h1>
    <p>Данный web сервер является <a href="https://habr.com/ru/articles/464261/">API</a> на основе <a href="https://flask.palletsprojects.com/en/latest/">Flask</a> служит анализатором журналов, а так же возвращает список ip адресов котоые находятся в списках спам сервисах. Сам сервер запускается и перезагружается автоматически c помощью менеджера служб <a href="https://habr.com/ru/companies/slurm/articles/255845/">systemd</a>. Данные берутся из директории <a href="#data_files" >data_file</a>. Вызвать документацию по данному сервису можно обратившит на данный URL - <a href="http://10.25.150.42:9200/dock">10.25.150.42:9200/dock</a></p>
    <h3>Состав</h3>
    <ul>
       <li><code>server.py:</code> Скрипт которые выполянет основную логику программы</li>
       <li><code>/logs:</code> Директория которая содержит логи обращений с сервису</li>
       <ul>
      <li><code>parser_serser.log</code> Содержит все обращения к сервису</li>
       <li><code>parser_serser_error.log</code> Содержит предупреждения или ошибки сервиса</li>
       </ul>
      <li><code>.env</code> Файл конфигурации в которм хранятся чувствительные данные</li>
      <li><code>requirements.txt:</code> Файл который содержит необходиме библиотеки для запуска скрипта</li>
    </ul>
    <h3>Пример заполнения .env</h3>
    <ul>
    <li>ip = Ip адресс для запуска</li> 
    <li>port = Порт по которому будут обращаться</li> 
    </ul>
    <h1 id="bot">Tg-bot</h1>
    <p>Данный телеграмм бот предназначен для сбора информации и отправки сотрудникам или группе сотрудников. Для отпалвки сообщений используется библиотека <a href='https://docs.telethon.dev/en/stable/'>telethon</a>. Бот запускается и перезагружается автоматически c помощью менеджера служб <a href="https://habr.com/ru/companies/slurm/articles/255845/">systemd</a>.</p>
    <h3>Состав</h3>
    <ul>
      <li><code>start.sh:</code> Отвечает за запуск программы с активацией venv</li>
      <li><code>bot.py</code> Скрипт который содержит оснвновную логику программы</li>
      <li><code>.env</code> Файл конфигурации в которм хранятся чувствительные данные </li>
      <li><code>/configs:</code> Директория в которой находятся файлы конфигурации
      <ul>
        <li><code>chats.conf</code> Файл конфигурации в которм хранятся 'usernames' телеграмм каналов. Пример: (сслыка: <a href='https://t.me/xakep_ru'>https://t.me/xakep_ru</a>, запись в файл: xakep_ru) </li>
        <li><code>keywords.conf</code> Файл конфигурации в которм хранятся ключевые слова по которым в дальнейшем будут фильроваться посты</li>
        <li><code>users.conf:</code> Файл конфигурации в котором хрантся ID пользователей или групп куда идёт расслка постов</li>
      </ul>
      <li><code>/logs:</code> Директория которая содержит логи обращений с сервису</li>
       <ul>
      <li><code>parser_bot.log</code> Содержит все логи отправки сообщений</li>
       <li><code>parser_serser_error.log</code> Содержит предупреждения или ошибки бота</li>
       </ul>
      <li><code>requirements.txt:</code> Файл который содержит необходиме библиотеки для запуска скрипта</li>
</li>
    </ul>
    <h3>Пример заполнения .env</h3>
    <ul>
    <li>api_id= <a href='https://core.telegram.org/'>Ваш API ID</a></li> 
    <li>api_hash= <a href='https://core.telegram.org/'>Ваш API HASH</a></li> 
    <li>bot_token= Токен бота, который можно получуть у <a href='https://t.me/BotFather'>BotFather</a></li>
    </ul>
    <h1 id="data_files">Data_files</h1>
    <p>Директория для хранения данных</p>
    <h3>Состав</h3>
    <ul>
    <li><code>mail_ban.json:</code> Файл в котором находятся данные о почтах которые попали в спам сервисы</li>
    <li><code>ftp_logs.json</code> Файл в котором содержатся данные о возможных инцедентах</li>
    </ul>
  </body>
</html>