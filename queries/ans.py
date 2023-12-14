def get_spreadsheetId(db,form_id):
    query = f"SELECT spreadsheetId FROM form WHERE form_id = {form_id}"
    result = db.execute_query(query)
    return result

def insert_ans_mcq(db,qid,response_id,user_id):
    query = f"INSERT INTO answer_mcq(q_id,res_id,user_id) VALUES {qid,response_id,user_id}"
    ans_id = db.execute_query(query,True)
    return ans_id 

def insert_ans_text(db,qid,ans_text,user_id):
    query = f"INSERT INTO answer_text(q_id,ans_text,user_id) VALUES {qid,ans_text,user_id}"
    ans_id = db.execute_query(query,True)
    return ans_id 
