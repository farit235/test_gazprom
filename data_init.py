import json
import psycopg2


def init_db():
    """Инициализация БД"""
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='password',
        host='localhost'
    )


    with open("data/data.json") as file:
        data = file.readlines()

    clear_data = []
    categories = []

    for i in range(1, len(data), 2):
        item = json.loads(data[i])
        for itm in item.get('category', None):
            categories.append(itm)

    set_cat = set(categories)
    categories = list(set_cat)

    for i in range(1, len(data), 2):
        item = json.loads(data[i])
        category_id = 1
        for itm in item.get('category', None):
            if itm in set_cat:
                category_id = categories.index(itm)
                if category_id == 0:
                    category_id = 1
            else:
                category_id = 1

        clear_item = {
        "create_timestamp": item.get('create_timestamp', None),
        "timestamp": item.get('timestamp', None),
        "language": item.get('language', None),
        "wiki": item.get('wiki', None),
        "category_id": category_id,
        "title": item.get('title', None),
        "auxiliary_text": item.get('auxiliary_text', None)
        }
        clear_data.append(clear_item)

    conn.autocommit = True

    cursor = conn.cursor()
    # q_drop = """DROP TABLE wikitable, categories;"""

    # cursor.execute(q_drop)
    query = '''
            CREATE TABLE categories(
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
            );
            '''
    cursor.execute(query)

    for i in set_cat:
        query_2 = f'''INSERT INTO categories (name) VALUES ('{i}')'''
        cursor.execute(query_2)

    query_3 = '''
            CREATE TABLE wikitable(
            wiki_id SERIAL PRIMARY KEY,
            create_timestamp TIMESTAMPTZ,
            timestamp TIMESTAMPTZ,
            language VARCHAR,
            wiki VARCHAR,
            title VARCHAR,
            auxiliary_text VARCHAR,
            category_id INT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
            );
            '''
    cursor.execute(query_3)

    for i in clear_data:
        query_4 = f'''INSERT INTO wikitable (create_timestamp, timestamp, language, wiki, title, auxiliary_text, category_id)
                        VALUES ('{i['create_timestamp']}', '{i['timestamp']}', '{i['language']}', '{i['wiki']}',
                                '{i['title'].replace("'", "")}', '{str(i['auxiliary_text']).replace("'", "")}', '{i['category_id']}')'''
        cursor.execute(query_4)

    conn.close()
