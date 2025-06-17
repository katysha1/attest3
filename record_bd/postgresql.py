import asyncpg


async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='1234',
                                 database='postgres',
                                 host='127.0.0.1')
    query = '''select user_id, chat_id, message_id, text from tg_task
                where text is not Null
                '''
    res = await conn.fetch(query)
    return res