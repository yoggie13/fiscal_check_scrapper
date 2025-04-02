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
            return True
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
    mycursor = mydb.cursor(dictionary=True)

    try:
        sql = f"SELECT {what} FROM {table} {where if where != None else ''}"
        mycursor.execute(sql)
        return True

    except Exception as e:
        print(e)
        return False
        
    finally:
        mycursor.close()

def selectCheckWithItems(userID, search, what="*"):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SHOW COLUMNS FROM checks")
        checkColumns = [col[0] for col in mycursor.fetchall()]
        checkColumns.remove("UserID")

        mycursor.execute("SHOW COLUMNS FROM checkitems")
        checkItemsColumns = [col[0] for col in mycursor.fetchall()]

        where_clause = " OR ".join([f"c.{col} LIKE LOWER(%s)" for col in checkColumns])
        where2_clause = " OR ".join([f"ci.{col} LIKE LOWER(%s)" for col in checkItemsColumns])

        where = where_clause + " OR " + where2_clause

        sql = f"SELECT DISTINCT c.CheckID, c.Date, c.Total, s.Name FROM checks as c JOIN checkitems as ci ON c.CheckID = ci.CheckID JOIN shops as s ON c.ShopID = s.ShopID WHERE c.UserID = {userID} AND ({where})"
        search = f"%{search}%".lower()

        mycursor.close()
        mycursor = mydb.cursor(dictionary=True)

        mycursor.execute(sql, [search] * (len(checkColumns)+len(checkItemsColumns)))

        sqlReturn = mycursor.fetchall()

        return sqlReturn
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