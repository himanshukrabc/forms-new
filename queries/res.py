def validate_form(db, form_id, user_id):
    query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
    result = db.execute_query(query)[0][0]
    return result == 1


def validate_ques(db, form_id, q_id):
    query = f"SELECT COUNT(*) FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
    result = db.execute_query(query)[0][0]
    return result == 1


def validate_res(db, res_id, q_id):
    query = f"SELECT COUNT(*) FROM response WHERE res_id = {res_id} AND q_id = {q_id}"
    result = db.execute_query(query)[0][0]
    return result == 1


def insert_res(db, q_id, res_text):
    query = f"INSERT into response(qid,res_text) VALUES({q_id,res_text})"
    result = db.execute_query(query)
    return result == 1


def update_res(db, res_id, res_text):
    query = f"UPDATE response SET res_text={res_text} WHERE res_id = {res_id}"
    db.execute_query(query)


def delete_res(db, res_id):
    query = f"DELETE FROM response WHERE res_id = {res_id}"
    db.execute_query(query)
