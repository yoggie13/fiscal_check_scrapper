import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host = "localhost",
  user = os.getenv('DATABASE_USER'),
  password = os.getenv('DATABASE_PASS'),
  database = "fiscal_check"
)

transactionCheck = True

def start_transaction():
    try:
        mydb.start_transaction()
        return mydb.cursor()
    except Exception as e:
        return False

def commit():
    global transactionCheck
    
    if transactionCheck:
        try:
            mydb.commit()
        except Exception as e:
            return False
    else:
        mydb.rollback()
        transactionCheck =  True

def insertInTransaction (table, propNames, propTypes, props, mycursor):

    sql = f"INSERT INTO {table} ({propNames}) VALUES ({propTypes})" 

    try:
        if type(props) == tuple:
            mycursor.execute(sql, props)
        else:
            mycursor.executemany(sql, props)
        return mycursor.lastrowid
    except Exception as e:
        print(e)
        transactionCheck = False


def insert (table, propNames, propTypes, props):
    mycursor = mydb.cursor()

    sql = f"INSERT INTO {table} ({propNames}) VALUES ({propTypes})" 

    try:
        if type(props) == tuple:
            mycursor.execute(sql, props)
        else:
            mycursor.executemany(sql, props)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        mycursor.close()


def select (table, what="*", where = None):
    mycursor = mydb.cursor()

    try:
        sql = f"SELECT {what} FROM {table} {where if where != None else ''}"
        mycursor.execute(sql)
        return True

    except Exception as e:
        print(e)
        return False
        
    finally:
        mycursor.close()

def update (table, what, value, where, type):
    mycursor = mydb.cursor()

    sql = f"UPDATE {table} SET {what} = {value} WHERE {type} = {where}"
    
    try:
        mycursor.execute(sql)
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        mycursor.close()