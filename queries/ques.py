def validate_form_sheetId(db, form_id, user_id, get_first_qid):
    if get_first_qid:
        query = f"SELECT first_qid,spreadsheetId FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
    else:
        query = f"SELECT spreadsheetId FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
    result = db.execute_query(query)
    return result


def insert_ques_db(db, prev_qid, first_qid, form_id, ques_text, ques_type, responses):
    next_qid = None
    if prev_qid == 0:
        next_qid = first_qid
        query = f"INSERT INTO question(form_id,ques_text,ques_type,next_qid) VALUES {form_id,ques_text,ques_type,next_qid}"
        qid = db.execute_query(query, True)
        query = f"UPDATE form SET first_qid={qid} WHERE form_id={form_id}"
        db.execute_query(query)
    else:
        query = f"SELECT next_qid FROM question WHERE q_id={prev_qid}"
        next_qid = db.execute_query(query)[0][0]
        query = f"INSERT INTO question(form_id,ques_text,ques_type,next_qid,prev_qid) VALUES {form_id,ques_text,ques_type,next_qid,prev_qid}"
        qid = db.execute_query(query, True)
        query = f"UPDATE question SET next_qid={qid} WHERE q_id={prev_qid}"
        db.execute_query(query)
    if ques_type.upper() == "MCQ":
        for resp in responses:
            query = f"INSERT INTO response(q_id,res_text) VALUES {qid,resp}"
            db.execute_query(query, True)
    return qid


def update_ques_db(db, ques_text, q_id):
    query = f"UPDATE question SET ques_text='{ques_text}' WHERE q_id={q_id}"
    db.execute_query(query)


def validate_ques_prev_qid(db, form_id, q_id):
    query = f"SELECT prev_qid FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
    result = db.execute_query(query)
    return result


def get_next_qid(db, q_id):
    query = f"SELECT next_qid FROM question WHERE q_id = {q_id}"
    next_qid = db.execute_query(query)[0][0]
    return next_qid


def update_ques_on_delete(db, prev_qid, next_qid, form_id):
    if prev_qid == None:
        query = f"UPDATE form SET first_qid={next_qid} WHERE form_id={form_id}"
        db.execute_query(query)
    else:
        query = f"UPDATE question SET next_qid={next_qid} WHERE q_id={prev_qid}"
        db.execute_query(query)


def delete_ans(db, q_id):
    query = f"DELETE FROM answer_text WHERE q_id={q_id}"
    db.execute_query(query)
    query = f"DELETE FROM answer_mcq WHERE q_id={q_id}"
    db.execute_query(query)


def delete_res(db, q_id):
    query = f"DELETE FROM response WHERE q_id={q_id}"
    db.execute_query(query)


def delete_ques(db, q_id):
    query = f"DELETE FROM question WHERE q_id={q_id}"
    db.execute_query(query)
