import mysql.connector
import Result
import os

database_host = os.environ['MYSQL_TCC_HOST']
database_name = os.environ['MYSQL_TCC_NAME']
database_user = os.environ['MYSQL_TCC_USER']
database_pass = os.environ['MYSQL_TCC_PASS']

def get_connection():
    mydb = mysql.connector.connect(
        host=database_host,
        user=database_user,
        password=database_pass,
        database=database_name
    )

    return mydb

def batch_tweet_insertion(list_of_tweets):
    mydb = get_connection()

    mycursor = mydb.cursor()

    sql = "INSERT INTO tweets (id, username, text, sentiment, fav_count, retweet_count, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = []

    for tweet in list_of_tweets:
        val.append(tweet.split_values())

    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()

    print(mycursor.rowcount, "was inserted.")

    return

def execute(sql, values=None):
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    mydb.commit()
    mydb.close()
    return

def execute_many(sql, values=None):
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.executemany(sql, values)
    mydb.commit()
    mydb.close()
    return

def create_database():
    mydb = mysql.connector.connect(
        host=database_host,
        user=database_user,
        password=database_pass
    )

    mycursor = mydb.cursor()

    sql = "CREATE DATABASE IF NOT EXISTS " + database_name
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    return

def create_table_tweets():

    mydb = get_connection()
    mycursor = mydb.cursor()
    
    sql = """CREATE TABLE IF NOT EXISTS tweets(
        id              varchar(50)
        ,username       varchar(50)
        ,text           text
        ,sentiment      varchar(50)
        ,fav_count      varchar(50)
        ,retweet_count  varchar(50)
        ,created_at     varchar(50)
    )"""

    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    return

def create_table_search_terms():
    mydb = get_connection()
    mycursor = mydb.cursor()
    
    sql = """CREATE TABLE IF NOT EXISTS search_terms(
        term            varchar(100) primary key,
        search_qty      int
    )"""

    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    return

def initialize_database():
    create_database()
    create_table_tweets()
    create_table_search_terms()

