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

def insertInTransaction (table, propNames, props, mycursor):
    
    ss = ", ".join(["%s"] * len(propNames.split(", ")))
    sql = f"INSERT INTO {table} ({propNames}) VALUES ({ss})"

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

def select (table,  where = None, what="*", groupBy=None):
    mycursor = mydb.cursor(dictionary=True)

    try:
        sql = f"SELECT {what} FROM {table} {f'WHERE {where}' if where != None else ''} {f'GROUP BY {groupBy}' if groupBy != None else ''}"
        mycursor.execute(sql)
        return mycursor.fetchall()

    except Exception as e:
        print(e)
        return []
        
    finally:
        mycursor.close()

def searchChecksWithItems(userID, search, what="*"):
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

        sql = f"SELECT DISTINCT c.CheckID, c.Date, c.UserPaid, c.Total, s.Name FROM checks as c JOIN checkitems as ci ON c.CheckID = ci.CheckID JOIN shops as s ON c.ShopID = s.ShopID AND c.PIB = s.PIB WHERE c.UserID = {userID} AND ({where})"
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

def update (table, what, value, where):
    mycursor = mydb.cursor()

    sql = f"UPDATE {table} SET {what} = {value} WHERE {where}"
    print(sql)
    
    try:
        mycursor.execute(sql)
        mydb.commit()

        return True
    except Exception as e:
        print(e)
        return False
    finally:
        mycursor.close()
