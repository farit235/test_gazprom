import psycopg2
from flask import jsonify, request


def find_data_by_name(title):
    """Функция поиска текста по названию"""
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='password',
        host='localhost'
    )
    pretty = request.args.get('pretty')
    query = f"""
            SELECT * \
            FROM wikitable \
            WHERE title LIKE '%{title}%' \
            """

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    all = []
    for row in rows:
        record = {"id": row[0], "create_timestamp": row[1], "timestamp": row[2],
                 "language": row[3], "wiki": row[4], "category_id": row[5], "title": row[6], "auxiliary_text": row[7]}
        print(record)
        all.append(record)
    conn.close()
    if pretty:
        return jsonify(all)
    else:
        return all


# def find_data_by_name_form(title):
#     """Функция поиска текста по названию"""
#     pretty = request.args.get('pretty')
#     query = f"""
#             SELECT * \
#             FROM wikitable \
#             WHERE title LIKE '%{title}%' \
#             """
#
#     cursor = conn.cursor()
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     all = []
#     for row in rows:
#         record = {"id": row[0], "create_timestamp": row[1], "timestamp": row[2],
#                  "language": row[3], "wiki": row[4], "category_id": row[5], "title": row[6], "auxiliary_text": row[7]}
#         print(record)
#         all.append(record)
#     conn.close()
#     return jsonify(all)


