import os.path
import asyncio
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "./assets/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

with open("token.json", "w") as token:
    token.write(creds.to_json())

def create_sheet(user_id,qid,q_text):
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': f'Sheet_{user_id}'  # Specify the title for the new spreadsheet
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'AnswerSheet'
                    }
                },
                {
                    'properties': {
                        'title': 'QuestionSheet'
                    }
                }
            ]
        }

        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        print(f"Created new spreadsheet with ID: {spreadsheet['spreadsheetId']}")
        spreadsheetId = spreadsheet['spreadsheetId']

        values = [["question_id","question_text"]]
        for i in range(len(qid)):
            values.append([qid[i],q_text[i]])

        range_ = 'QuestionSheet!A1:B' + str(len(values))

        value_input_option = 'RAW'
        value_range_body = {
            'values': values
        }

        # Execute the request to update the sheet
        request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=range_,
            valueInputOption=value_input_option,
            body=value_range_body
        )
        response = request.execute()
        print("Pairs added to the sheet successfully!")

        qid.insert(0,"user_id")
        values = [qid,]
        range_ = 'AnswerSheet!1:1'
        body = {
            'values': values
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId,
            range=range_,
            valueInputOption='RAW',
            body=body
        ).execute()
        print('Question Ids inserted successfully.')
        return spreadsheetId
    except Exception as e:
        print(e)
        print(f"Error creating spreadsheet: {str(e)}")

def get_col_num(service, spreadsheetId, sheet_properties, qid):
    sheet_title = sheet_properties['title']
    range_to_search = f"{sheet_title}!1:1"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_to_search).execute()
    values = result.get('values', [])
    print(values)
    if not values:
        print('No data found.')
    else:
        col_num=1
        if qid !=0 :
            col_num=0
            for col in values[0]:
                print(col)
                col_num+=1
                if col == str(qid):
                    break;
    print(col_num)
    return col_num

def get_row_num(service, spreadsheetId, sheet_properties, qid):
    sheet_title = sheet_properties['title']
    range_to_search = f"{sheet_title}!A:B"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_to_search).execute()
    values = result.get('values', [])
    print(values)
    if not values:
        print('No data found.')
    else:
        row_num=1
        if qid!=0:
            row_num=0
            for row in values:
                print(row[0])
                row_num+=1
                if row[0] == str(qid):
                    break;
    print(row_num)
    return row_num 

def add_row_col(service, spreadsheetId, ans_sheet_id, ques_sheet_id, row_num, col_num):
    request_body = {
        "requests": [
            {
                "insertDimension": {
                    "range": {
                        "sheetId": ques_sheet_id,
                        "dimension": "ROWS",
                        "startIndex": row_num,
                        "endIndex": row_num + 1
                    },
                    "inheritFromBefore": False
                }
            },
            {
                "insertDimension": {
                    "range": {
                        "sheetId": ans_sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": col_num,
                        "endIndex": col_num + 1
                    },
                    "inheritFromBefore": False
                }
            }
        ]
    }

    # Execute the request to insert a new row
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=request_body).execute()
    print("New Row,Column created")

def update_question_sheet(service, spreadsheetId, sheet_title, qid, q_text, row_num):
    new_row_values = [qid,q_text]  
    update_range = f"{sheet_title}!A{row_num+1}"  # Specify the range for the new row
    update_body = {
        'values': [new_row_values]
    }

    # Execute the request to update values in the newly inserted row
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=update_range,
        valueInputOption='RAW',
        body=update_body
    )
    response = request.execute()

def update_answer_sheet(service, spreadsheetId,sheet_title, qid, col_num):
    new_col_value = [qid]  
    update_range = f"{sheet_title}!{chr(65+col_num)}1"  # Specify the range for the new row
    update_body = {
        'values': [new_col_value]
    }

    # Execute the request to update values in the newly inserted row
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=update_range,
        valueInputOption='RAW',
        body=update_body
    )
    response = request.execute()

def insert_ques(spreadsheetId, prev_qid, qid, q_text):
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    col_num = get_col_num(service, spreadsheetId, spreadsheet['sheets'][0]['properties'], prev_qid)
    row_num = get_row_num(service, spreadsheetId, spreadsheet['sheets'][1]['properties'], prev_qid)
    add_row_col(service, spreadsheetId, spreadsheet['sheets'][0]['properties']['sheetId'], spreadsheet['sheets'][1]['properties']['sheetId'], row_num, col_num)
    update_answer_sheet(service,spreadsheetId,spreadsheet['sheets'][0]['properties']['title'],qid,col_num)
    update_question_sheet(service,spreadsheetId,spreadsheet['sheets'][1]['properties']['title'],qid,q_text,row_num)

def upd_ques(spreadsheetId, qid, q_text):
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheet_properties = spreadsheet['sheets'][1]['properties']
    sheet_id = sheet_properties['sheetId']
    sheet_title = sheet_properties['title']
    range_to_search = f"{sheet_title}!A:B"

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_to_search).execute()
    values = result.get('values', [])
    print(values)
    if not values:
        print('No data found.')
    else:
        updated_values = []
        for row in values:
            if row and len(row) >= 2 and row[0] == str(qid):
                row[1] = q_text
            updated_values.append(row)
        
        print(updated_values)

        update_range = f"{sheet_title}!B1:B" + str(len(updated_values))
        update_body = {
            'values': [[row[1]] for row in updated_values]
        }


        request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=update_range,
            valueInputOption='RAW',
            body=update_body
        )
        response = request.execute()

        print("Values updated successfully!")

def del_row_col(service, spreadsheetId, ans_sheet_id, ques_sheet_id, row_num, col_num):
    request_body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": ques_sheet_id,
                        "dimension": "ROWS",
                        "startIndex": row_num-1,
                        "endIndex": row_num
                    }
                }
            },
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": ans_sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": col_num-1,
                        "endIndex": col_num
                    }
                }
            }
        ]
    }

    # Execute the request to insert a new row
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=request_body).execute()
    print("New Row,Column created")

def del_ques(spreadsheetId,qid):
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    col_num = get_col_num(service, spreadsheetId, spreadsheet['sheets'][0]['properties'], qid)
    row_num = get_row_num(service, spreadsheetId, spreadsheet['sheets'][1]['properties'], qid)
    del_row_col(service, spreadsheetId, spreadsheet['sheets'][0]['properties']['sheetId'], spreadsheet['sheets'][1]['properties']['sheetId'], row_num, col_num)

async def insert_answer(spreadsheetId, user_id, answers):
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    answers.insert(0,user_id)  
    sheet_title = spreadsheet['sheets'][0]['properties']['title']
    update_range = f"{sheet_title}!A1:{chr(64+len(answers))}1"
    update_body = {
        'values': [answers]
    }

    # Execute the request to update values in the newly inserted row
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId,
        range=update_range,
        valueInputOption='RAW',
        body=update_body
    )
    response = request.execute()
    print(response)

async def schedule_insert_answer(spreadsheetId, user_id, answers, retry_count=0):
    try:
        await insert_answer(spreadsheetId, user_id, answers)
    except HttpError as e:
        if e.resp.status == 429:
            # This error code is generated when there are too many requests.
            # Google sheets only supports 300 requests per minute, so we implement exponential backoff.
            # This will make calls in exponentially increasing time when the call fails.
            # This helps in load reduction. At retry_count = 5, total wait time exceeds 60s, 
            # which should start the new limit of 60 seconds.
            # This approach can also be used to deal with other errors where the sheet api is unavailable. 
            if(retry_count < 6):
                random_time = random.randint(0, 1000)/1000
                asyncio.sleep(2**retry_count+random_time)
                schedule_insert_answer(spreadsheetId, user_id, answers, retry_count+1)
            else:
                print("insert operation timed out")
        else:
            print("HTTP error:", e)