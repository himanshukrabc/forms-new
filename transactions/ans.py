from assets.db import DatabaseTransaction
from assets.sheets import schedule_insert_answer
from queries.ans import get_spreadsheetId, insert_ans_mcq, insert_ans_text
import asyncio

async def add_ans_transaction(data):
    db = DatabaseTransaction()
    db.start_transaction()
    form_id = data.get("form_id")
    result = get_spreadsheetId(db, form_id)
    if len(result) != 1 or len(result[0])!=1:
        db.rollback_transaction("No such form exists")
        return "No such form exists",400
    spreadsheetId = result[0][0]
    ans_id_list = []
    ans_list = []
    for ans in data.get("answers"):
        qid = ans.get("qid")
        if "response_id" in ans.keys():
            ans_id = insert_ans_mcq(db, qid, ans.get("response_id"), data.get("user_id"))
            ans_list.append(ans.get("response_id"))
            ans_id_list.append(ans_id)
        else:
            ans_id = insert_ans_text(db, qid, ans.get("ans_text"), data.get("user_id"))
            ans_list.append(ans.get("ans_text"))
            ans_id_list.append(ans_id)
    db.commit_transaction()
    # calling the function for data insertion to sheet asychronously
    task = asyncio.create_task(schedule_insert_answer(spreadsheetId, data.get("user_id"), ans_list))
    return ans_id_list,200