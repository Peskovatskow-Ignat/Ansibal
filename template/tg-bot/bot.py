from telethon import TelegramClient
import asyncio
import json
import subprocess
import os
from  datetime import datetime
from dotenv import load_dotenv 

load_dotenv() # Загрузка переменных окружения из .env файла

api_id = os.getenv('api_id')  # Получение API ID и Hash из переменных окружения
api_hash = os.getenv('api_hash')

with open('configs/users.conf', 'r') as file:  # Загрузка ID целевых пользователей из файла 'users.conf'
    target_user_ids = [int(line.strip()) for line in file.readlines()]

client = TelegramClient('session_name', api_id, api_hash)  # Инициализация TelegramClient

with open('configs/chats.conf', 'r', encoding='UTF-8') as file:  # Загрузка списка каналов из файла 'chats.conf'
    chanelist = [line.strip() for line in file.readlines()]
chanel_send = {channel: set() for channel in chanelist}

def load_keywords():  # Функция загрузки ключевых слов из файла 'keywords.conf'
    with open('configs/keywords.conf', 'r', encoding='UTF-8') as file:
        return [line.strip() for line in file.readlines()]

keywords = load_keywords()  # Загрузка ключевых слов

async def collect_posts(channel):  # Асинхронная функция для сбора сообщений из указанного канала
    with open(f"{channel}.txt") as file:
        file = file.readlines()
    posts = []
    chanel_dict = {}
    post_send = set()
    ids = set()
    for n, _ in enumerate(file):  # Обработка сообщений из файла
        file[n] = json.loads(file[n])
        if str(file[n]['content']):
            pass
        links = [link for link in file[n]['outlinks'] if channel not in link]
        url = file[n]['url']
        last_slash_index = url.rfind('/')
        if last_slash_index != -1:
            post_id = url[last_slash_index + 1:]
        for word in keywords:  # Поиск ключевых слов в сообщениях
            if file[n]['content'] and str(word).lower() in file[n]['content'].lower():
                if not chanel_send[channel] or post_id not in chanel_send[channel]:
                    try:
                        await send_messages(f'Новый пост на канале {channel}\n' + str(file[n]['content']) + "\n\n" + str("\n".join(links)) + '\n' 'Перейти к посту:' + url)
                    except Exception as e:
                        print("Не удалось отправить сообщение:", e)
                post_send.add(post_id)
                break
        ids.add(post_id)
    chanel_send[channel] = sorted(post_send)
    chanel_dict[channel] = sorted(ids)
    return posts

async def upload_posts(num_posts, channel):  # Асинхронная функция для загрузки сообщений из указанного канала
    command = f'snscrape --max-result {num_posts} --jsonl telegram-channel {channel} > /opt/tg-bot/{channel}.txt'
    subprocess.run(command, shell=True)

async def delete_txt_files():  # Асинхронная функция для удаления файлов с расширением .txt
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            os.remove(filename)

async def send_messages(message):  # Асинхронная функция для отправки сообщений целевым пользователям
    for user in target_user_ids:
        try:
            await client.send_message(user, message)
            print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Сообщение отправлено пользователю, {user}')
        except Exception as e:
            print(f'Ошибка отправки сообщения пользователю {user}', e)

async def main():  # Асинхронная основная логика бота
    await client.start(bot_token=os.getenv('bot_token'))
    print('Бот запущен!!!')
    while True:
        await delete_txt_files()
        for channel in chanelist:
            await upload_posts(3, channel)
            for _ in await collect_posts(channel):
                pass
        print(f'{datetime.now().strftime("%dd %mm %Yy %H:%M:%S")}: Парсинг прошёл успешно')
        await delete_txt_files()
        await asyncio.sleep(60)

async def run_bot():  # Асинхронная функция для запуска бота
    await main()

if __name__ == "__main__":  # Запуск основного цикла
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
