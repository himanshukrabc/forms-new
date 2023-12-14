from assets.db import DatabaseTransaction
from assets.sheets import create_sheet
from queries.form import (
    validate_user,
    create_form_db,
    insert_ques_to_form,
    set_spreadsheet_id,
    validate_user_first_qid,
    validate_user_first_qid,
    get_ques,
    get_responses,
    validate_form,
    get_qids,
    delete_responses,
    delete_questions,
    delete_form,
)


def create_form_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    user_id = data.get("user_id")
    result = validate_user(db, user_id)
    if not result:
        db.rollback_transaction("user not found")
        return "user not found",400
    form_id = create_form_db(db, user_id)
    result = insert_ques_to_form(db, data.get("questions"),form_id)
    qid_list = result.get("qid_list")
    q_text_list = result.get("q_text_list")

    spreadsheetId = create_sheet(data.get("user_id"), qid_list, q_text_list)
    set_spreadsheet_id(db, spreadsheetId, form_id)
    db.commit_transaction()
    return {"form_id": form_id, "qid_list": qid_list, "spreadsheet_id": spreadsheetId},200


def display_form_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()

    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_user_first_qid(db, form_id, user_id)
    if len(result)!=1 or len(result[0]) != 1:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400

    q_list = get_ques(db, form_id)

    mp = {}
    print(q_list)
    for q in q_list:
        mp[q[0]] = {"text": q[2], "type": q[3], "next_qid": q[4]}
    resp = []
    cur_qid = result[0][0]
    while cur_qid != None:
        if mp[cur_qid].get("type").upper() == "MCQ":
            result = get_responses(db, cur_qid)
            responses = []
            for item in result:
                responses.append({"resp_id": item[0], "resp_text": item[1]})
            resp.append(
                {
                    "q_id": cur_qid,
                    "q_text": mp[cur_qid].get("text"),
                    "q_type": mp[cur_qid].get("type"),
                    "response": responses,
                }
            )
        else:
            resp.append(
                {
                    "q_id": cur_qid,
                    "q_text": mp[cur_qid].get("text"),
                    "q_type": mp[cur_qid].get("type"),
                }
            )
        cur_qid = mp[cur_qid].get("next_qid")
    db.commit_transaction()
    return resp,200


def delete_form_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    form_id = data.get("form_id")
    user_id = data.get("user_id")
    result = validate_form(db, form_id, user_id)
    if not result:
        db.rollback_transaction("unexpected Error")
        return "unexpected Error",400
    qid_list = get_qids(db, form_id)
    for qid in qid_list:
        delete_responses(db, qid)
    delete_questions(db, form_id)
    delete_form(db, form_id)
    db.commit_transaction()
    return "Form deleted",200
