from assets.db import DatabaseTransaction
from queries.res import (
    validate_form,
    validate_ques,
    validate_res,
    insert_res,
    update_res,
    delete_res,
)


def add_res_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_form(db, form_id, user_id)
    if not result:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    q_id = data.get("q_id")
    result = validate_ques(db, form_id, q_id)
    if not result:
        db.rollback_transaction("No such question exists")
        return "No such question exists",400
    result = insert_res(db, q_id, data.get("res_text"))

    db.commit_transaction()
    return result,200


def update_res_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_form(db, form_id, user_id)
    if not result:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    q_id = data.get("q_id")
    result = validate_ques(db, form_id, q_id)
    if not result:
        db.rollback_transaction("No such question exists")
        return "No such question exists",400

    res_id = data.get("res_id")
    result = validate_res(db, form_id, q_id)
    if not result:
        db.rollback_transaction("No such response exists")
        return "No such response exists",400

    update_res(db, res_id, data.get("res_text"))

    db.commit_transaction()
    return "Resp updated",200


def del_res_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_form(db, form_id, user_id)
    if not result:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    q_id = data.get("q_id")
    result = validate_ques(db, form_id, q_id)
    if not result:
        db.rollback_transaction("No such question exists")
        return "No such question exists",400

    res_id = data.get("res_id")
    result = validate_res(db, form_id, q_id)
    if not result:
        db.rollback_transaction("No such response exists")
        return "No such response exists",400

    delete_res(db, res_id)
    db.commit_transaction()
    return "Response deleted",200