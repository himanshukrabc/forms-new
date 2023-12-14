def validate_username(db,username):
    query = f"SELECT COUNT(*) FROM user WHERE username = '{username}'"
    result = db.execute_query(query)[0][0]
    return (result==0)

def get_user(db,user_id):
    query = f"SELECT * FROM user WHERE user_id = '{user_id}'"
    result = db.execute_query(query)
    print("qweqwe")
    return result

def delete_user(db,user_id):
    query = f"DELETE FROM user WHERE user_id = '{user_id}'"
    result = db.execute_query(query)
    return result
        
def create_user(db,username):
    query = f"INSERT INTO user(username) VALUES ('{username}')"
    result = db.execute_query(query,True)
    return result