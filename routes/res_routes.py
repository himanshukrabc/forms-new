from flask import Blueprint
from flask import request, jsonify
from logs.logs_setup import log_info, log_error
import pymysql
from transactions.res import (
    add_res_transaction,
    update_res_transaction,
    del_res_transaction,
)

res_bp = Blueprint("response", __name__)


@res_bp.route("/add", methods=["POST"])
async def add_res():
    try:
        data = request.get_json()
        response=None
        status=None
        if "user_id" not in data.keys():
            response="user_id not found"
            status=400
        elif "form_id" not in data.keys():
            response="form_id not found"
            status=400
        elif "q_id" not in data.keys():
            response="q_id not found"
            status=400
        else:
            response, status = add_res_transaction(data)
        await log_info("/res/add", request.method, data, status, response)
        return jsonify({"data": response}), status
    except pymysql.Error as e:
        print(e)
        await log_error("/res/add", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/res/add", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500


@res_bp.route("/update", methods=["POST"])
async def update_res():
    try:
        data = request.get_json()
        if "user_id" not in data.keys():
            response = "data": "user_id not found"
            status=400
        elif "form_id" not in data.keys():
            response = "data": "form_id not found"
            status=400
        elif "q_id" not in data.keys():
            response = "data": "q_id not found"
            status=400
        else:
            result, status = update_res_transaction(data)
        await log_info("/res/update", request.method, data, status, response)
        return jsonify({"data": result}), status
    except pymysql.Error as e:
        print(e)
        await log_error("/res/update", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/res/update", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500


@res_bp.route("/delete", methods=["POST"])
async def del_res():
    try:
        data = request.get_json()
        if "user_id" not in data.keys():
            response = "data": "user_id not found"
            status=400
        elif "form_id" not in data.keys():
            response = "data": "form_id not found"
            status=400
        elif "q_id" not in data.keys():
            response = "data": "q_id not found"
            status=400
        else:
            result, status = del_res_transaction(data)
        await log_info("/res/delete", request.method, data, status, response)
        return jsonify({"data": result}), status
    except pymysql.Error as e:
        print(e)
        await log_error("/res/delete", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/res/delete", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500
