def validate_user(db,user_id):
    query = f"SELECT COUNT(user_id) FROM user WHERE user_id = '{user_id}'"
    result = db.execute_query(query)[0][0]
    return result==1

def create_form_db(db,user_id):
    query = f"INSERT INTO form(user_id) VALUES ({user_id})"
    form_id = db.execute_query(query, True)
    return form_id

def insert_ques_to_form(db,questions,form_id):
    prev_qid = None
    qid_list = []
    q_text_list = []
    first_qid = None
    for ques in questions:
        if prev_qid == None:
            query = f"INSERT INTO question(form_id, ques_text, ques_type, prev_qid) VALUES ({form_id}, '{ques.get('ques_text')}', '{ques.get('ques_type')}', NULL)"
        else:
            query = f"INSERT INTO question(form_id,ques_text,ques_type,prev_qid) VALUES {form_id,ques.get('ques_text'),ques.get('ques_type'),prev_qid}"
        print(query)
        qid = db.execute_query(query, True)
        qid_list.append(qid)
        q_text_list.append(ques.get('ques_text'))
        prev_qid = qid
        if(first_qid==None):
            first_qid = qid
        if ques.get("ques_type") == "MCQ":
            for resp in ques.get("responses"):
                query = f"INSERT INTO response(q_id,res_text) VALUES {qid,resp}"
                db.execute_query(query, True)
    for i in range(len(qid_list)-1):
        query = f"UPDATE question SET next_qid={qid_list[i+1]} WHERE q_id={qid_list[i]}"
        db.execute_query(query)
    query = f"UPDATE form SET first_qid = {first_qid} WHERE form_id = {form_id}"
    db.execute_query(query)
    return {"qid_list":qid_list,"q_text_list":q_text_list}

def set_spreadsheet_id(db,spreadsheetId,form_id):
    query = f"UPDATE form SET spreadsheetId = '{spreadsheetId}' WHERE form_id = {form_id}"
    db.execute_query(query)

def validate_user_first_qid(db,form_id,user_id):
    query = f"SELECT first_qid FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
    result = db.execute_query(query)
    return result

def get_ques(db,form_id):
    query = f"SELECT * FROM question WHERE form_id = {form_id}"
    q_list = db.execute_query(query)
    return q_list

def get_responses(db,cur_qid):
    query = f"SELECT res_id,res_text FROM response WHERE q_id={cur_qid}"
    result = db.execute_query(query)
    return result


def validate_form(db,form_id,user_id):
    query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
    result = db.execute_query(query)[0][0]
    return result == 1

def get_qids(db,form_id):
    query = f"SELECT q_id FROM question WHERE form_id = {form_id} AND ques_type = 'MCQ'"
    qid_list = db.execute_query(query)[0]
    return qid_list

def delete_responses(db,qid):
    query = f"DELETE FROM response WHERE q_id = {qid}"
    db.execute_query(query)

def delete_questions(db,form_id):
    query = f"DELETE FROM question WHERE form_id = {form_id}"
    db.execute_query(query)

def delete_form(db,form_id):
    query = f"DELETE FROM form WHERE form_id = {form_id}"
    db.execute_query(query)

