from flask import Blueprint
from flask import request, jsonify
import pymysql
from logs.logs_setup import log_info, log_error
from transactions.ans import add_ans_transaction

ans_bp = Blueprint("answer", __name__)


@ans_bp.route("/add", methods=["POST"])
async def add_ans():
    try:
        data = request.get_json()

        if "form_id" not in data.keys():
            response = "form_id not found"
            status = 400
        else:
            response,status = await add_ans_transaction(data)
        log_info("/ans/add", request.method, data, status, response)
        return jsonify({"data": response}),status

    except pymysql.Error as e:
        print(e)
        log_error("/ans/add", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        log_error("/ans/add", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500
