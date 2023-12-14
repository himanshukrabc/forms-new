from assets.db import DatabaseTransaction
from queries.user import validate_username, get_user, delete_user, create_user

def reg_user_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    if "username" in data.keys():
        result = validate_username(db, data.get("username"))
        if result:
            result = create_user(db, data.get("username"))
            db.commit_transaction()
            return result,200
        else:
            db.rollback_transaction("username not unique")
            return "username not unique",400
    else:
        db.rollback_transaction("username not added")
        return "username not added",400

        

def get_user_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    if "user_id" in data.keys():
        result = get_user(db, data.get("user_id"))
        db.commit_transaction()
        return result,200
    else:
        db.rollback_transaction("user_id not added")
        return "user_id not added",400

def delete_user_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    if "user_id" in data.keys():
        delete_user(db,data.get("user_id"))
        db.commit_transaction()
        return "user deleted",200
    else:
        db.rollback_transaction("user_id/username not added")
        return "user_id/username not added",400
