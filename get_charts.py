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
