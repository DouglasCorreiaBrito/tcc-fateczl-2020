import db_utils as db


def readed_tweets():
    mydb = db.get_connection()
    sql = "select count(1) from tweets;"
    final_result = []
    cursor = mydb.cursor()
    cursor.execute(sql)
    for i, row in enumerate(cursor.fetchall()):
        final_result.append(row[i])
    mydb.close()
    return final_result[0]


def good_tweets():
    mydb = db.get_connection()
    sql = "select count(1)  from tweets where sentiment = 'pos';"
    final_result = []
    cursor = mydb.cursor()
    cursor.execute(sql)
    for i, row in enumerate(cursor.fetchall()):
        final_result.append(row[i])
    mydb.close()
    return final_result[0]


def bad_tweets():
    mydb = db.get_connection()
    sql = "select count(1)  from tweets where sentiment = 'neg';"
    final_result = []
    cursor = mydb.cursor()
    cursor.execute(sql)
    for i, row in enumerate(cursor.fetchall()):
        final_result.append(row[i])
    mydb.close()
    return final_result[0]


def neutral_tweets():
    mydb = db.get_connection()
    sql = "select count(1)  from tweets where sentiment = 'neu';"
    final_result = []
    cursor = mydb.cursor()
    cursor.execute(sql)
    for i, row in enumerate(cursor.fetchall()):
        final_result.append(row[i])
    mydb.close()
    return final_result[0]

def top_tweets():
    mydb = db.get_connection()
    sql = "select * from search_terms order by search_qty desc limit 3;"
    final_result = []
    cursor = mydb.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchall();
    for entry in resultset:
        final_result.append(entry)
    mydb.close()
    return final_result

def total_searchs():
    mydb = db.get_connection()
    sql = "select sum(search_qty) from search_terms;"
    final_result = 0
    cursor = mydb.cursor()
    cursor.execute(sql)
    resultset = cursor.fetchone()
    for result in resultset:
        final_result = result
    mydb.close()
    return final_result

total_searchs()