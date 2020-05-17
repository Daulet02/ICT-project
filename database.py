import sqlite3
conn = sqlite3.connect('db.db')
cur = conn.cursor()


def count_message(user_id: int):
    c = conn.cursor()
    c.execute('SELECT text FROM user_message WHERE id = ?  LIMIT 1', (user_id,))
    (result,) = c.fetchone()
    return result


welcome = count_message(1)
conn.close()