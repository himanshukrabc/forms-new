from assets.db import DatabaseTransaction
from assets.sheets import del_ques, upd_ques, insert_ques
from queries.ques import (
    validate_form_sheetId,
    insert_ques_db,
    update_ques_db,
    validate_ques_prev_qid,
    get_next_qid,
    update_ques_on_delete,
    delete_ans,
    delete_ques,
    delete_res,
)

def add_ques_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_form_sheetId(db, form_id, user_id, True)
    if len(result[0]) != 2:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    first_qid = result[0][0]
    spreadsheet_id = result[0][1]
    prev_qid = data.get("prev_qid")
    qid = insert_ques_db(
        db,
        prev_qid,
        first_qid,
        form_id,
        data.get("ques_text"),
        data.get("ques_type"),
        data.get("responses"),
    )

    db.commit_transaction()
    insert_ques(spreadsheet_id, prev_qid, qid, data.get("ques_text"))

    return qid,200

def update_ques_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    form_id = data.get("form_id")
    user_id = data.get("user_id")
    q_id = data.get("q_id")
    result = validate_form_sheetId(db, form_id, user_id, False)
    if len(result[0]) != 1:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    spreadsheet_id = result[0][0]

    update_ques_db(db, data.get("ques_text"), q_id)
    db.commit_transaction()

    upd_ques(spreadsheet_id, q_id, data.get("ques_text"))
    return "Question Updated",400
        

def delete_ques_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    form_id = data.get("form_id")
    user_id = data.get("user_id")
    q_id = data.get("q_id")

    result = validate_form_sheetId(db, form_id, user_id, False)
    if len(result[0]) != 1:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    spreadsheet_id = result[0][0]

    result = validate_ques_prev_qid(db, form_id, q_id)
    if len(result[0]) != 1:
        db.rollback_transaction("No such question exists")
        return "No such question exists",400
    prev_qid = result[0][0]
    next_qid = get_next_qid(db, q_id)
    update_ques_on_delete(db, prev_qid, next_qid, form_id)
    delete_ans(db, q_id)
    delete_res(db, q_id)
    delete_ques(db, q_id)

    db.commit_transaction()

    del_ques(spreadsheet_id, q_id)
    return "Question deleted successfully",200
