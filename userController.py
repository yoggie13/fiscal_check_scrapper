import databaseController

def loginUser(user):
    userData = databaseController.select("users", f"Email = '{user['email']}'")

    if(len(userData) == 0):
        if(databaseController.insert("users", 
                                     "Email, FirstName, LastName", 
                                     (user['email'], user['given_name'], user['family_name']))):
            userData = databaseController.select("users", f"Email = '{user['email']}'")
        else:
            return {}

    return userData[0]
