import asyncio
import aiofiles
import re
import lxml
import pandas as pd
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from utils import create_folder


headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


async def get_author() -> None:
    """
    Get novel authors from https://rustih.ru/stihi-russkih-poetov-klassikov/ website
    """
    author_url = 'https://rustih.ru/stihi-russkih-poetov-klassikov/'
    
    async with ClientSession() as session:
        async with session.get(url=author_url, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            author_list = {a.text:a.get('href')+'page/1/' for a  in soup.find('div', class_ = 'taxonomy-description').find_all('a')}
    return author_list
    

async def get_pages(author_link_pairs: dict):
    """
    Get max pages for each author except 1 or zero pages
    """
    tasks = []
    async with ClientSession() as session_page:
        for author, url in author_link_pairs.items():
            response = await session_page.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            navigation = soup.find('div', class_ = 'nav-links')

            try:
                max_page = navigation.find('a', text='Последняя »').get('href')
                m_page = int(re.findall(r'\d+', max_page)[0])
                if m_page > 1:
                    task = asyncio.create_task(get_poems_hrefs(url, m_page, author))
                    tasks.append(task)

            except AttributeError:
                try:
                    max_page = [el.get('href') for el in navigation.find_all('a', class_ = 'page-numbers page-numbers')][-1]
                    # Нужно больше двух страниц, так как не хватит для модели
                    m_page = int(re.findall(r'\d+', max_page)[0])
                    if m_page > 1:
                        task = asyncio.create_task(get_poems_hrefs(url, m_page, author))
                        tasks.append(task)

                except AttributeError:
                    # Нужно больше двух страниц, так как не хватит для модели
                    m_page = int(url[-2])
                    if m_page > 1:
                        task = asyncio.create_task(get_poems_hrefs(url, m_page, author))
                        tasks.append(task)
    
    await asyncio.gather(*tasks)


async def get_poems_hrefs(url: str, pages: int, author: str):
    """
    Get list-hrefs of poems for each author
    """
    for page in range(1, pages+1):
        async with ClientSession() as session_3:
            async with session_3.get(url=url.replace('page/1', f'page/{page}')) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                async with aiofiles.open(f'author_poem/{author}.txt', 'a') as file:
                    await file.write('\n'.join([href.find('a').get('href') for href in soup.find_all('div', class_ = 'entry-title')]))
                print(page, '/', pages+1)


async def get_poem_text(path_to_source: str)-> None:
    """
    Create task for each request
    """
    tasks = []
    sema = asyncio.Semaphore(8)
    for file in os.listdir(path_to_source):
        async with aiofiles.open(os.path.join(path_to_source, file), 'r') as fe:
            content = [line.strip() for line in await fe.readlines()]
            # author = file.split('.')[0]
            task = asyncio.create_task(parse_text(sema, content, file))
            tasks.append(task)

    await asyncio.gather(*tasks)


async def parse_text(semap: asyncio.Semaphore, url_list: list, author: str) -> None:
    """
    Grab authors text: poems and etc.
    """
    async with semap, ClientSession() as session:
        length = len(url_list)
        for pos, url in enumerate(url_list, start = 1):
            response = await session.get(url=url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')

            try:
                text_poem = ' '.join([el.text.replace('/\n', '') for el in soup.find('div', class_ = 'entry-content poem-text').find_all('p')])
            except Exception as _ex:
                print('Exception:', _ex)
                continue

            async with aiofiles.open(os.path.join('result', author), 'a', encoding='utf-8') as file:
                await file.write(text_poem + 'SEPARATOR\n')
            print('Работаем с файлом:', author, '\nПрогресс:', pos, '/', length)


def drop_useless_chars(path_to_file: str):
    """
    Remove unused symbols from parsed data
    """
    for file in os.listdir(path_to_file):
        with open(os.path.join(path_to_file, file), 'r', encoding='utf-8') as f:
            content = f.read()
            negative_pool = '*XIVI'
            for symbol in negative_pool:
                content = content.replace(symbol, '')
            # await f.write(content)
            
        with open(os.path.join(path_to_file, file), 'w', encoding='utf-8') as f_write:
            f_write.write(content)


def create_csv(path_to_file: str) -> None:
    """
    Convert txt data into csv
    """
    for file in os.listdir(path_to_file):
        _no_ext = file.split('.')[0]
        with open(os.path.join('result', file), 'r', encoding='utf-8') as read_f:
            content = read_f.read()
            content = content.split('SEPARATOR\n')
            table_values = zip(content, len(content)* [_no_ext])

        pd.DataFrame(table_values, columns=['Text', 'Author']).to_csv(os.path.join('res_csv', _no_ext + '.csv'), index=False)


def concat_data(path_to_file: str) -> None:
    """
    Make single file with text and authors
    """
    df = pd.DataFrame()
    for file in os.listdir(path_to_file):
        new = pd.read_csv(os.path.join(path_to_file, file))
        df = pd.concat([df, new])
    df.to_csv('test_data.csv')


if __name__ == '__main__':

    create_folder()
    loop = asyncio.get_event_loop()
    author_pair = loop.run_until_complete(get_author())
    [loop.run_until_complete(func) for func in (get_pages(author_pair), get_poem_text('author_poem'))]
    drop_useless_chars('result')
    create_csv('result')
    concat_data('res_csv')
