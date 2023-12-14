from flask import Blueprint
from flask import request, jsonify
from logs.logs_setup import log_info, log_error
import pymysql
from transactions.ques import (
    add_ques_transaction,
    update_ques_transaction,
    delete_ques_transaction,
)

ques_bp = Blueprint("ques", __name__)


@ques_bp.route("/add", methods=["POST"])
async def add_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            response = "user_id/username not added"
            status=400
        elif "form_id" not in data.keys():
            response = "form_id not added"
            status=400
        else:
            response, status = add_ques_transaction(data)
        await log_info("/ques/add", request.method, data, status, response)
        return jsonify({"data": response}), status

    except pymysql.Error as e:
        print(e)
        await log_error("/ques/add", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/ques/add", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500


@ques_bp.route("/update", methods=["POST"])
async def update_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            response = "user_id/username not added"
            status=400
        elif "form_id" not in data.keys():
            response = "form_id not added"
            status=400
        else:
            response, status = update_ques_transaction(data)
        await log_info("/ques/update", request.method, data, status, response)
        return jsonify({"data": response}), status

    except pymysql.Error as e:
        print(e)
        await log_error("/ques/update", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/ques/update", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500


@ques_bp.route("/delete", methods=["DELETE"])
async def delete_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            response = "user_id/username not added"
            status=400
        elif "form_id" not in data.keys():
            response = "form_id not added"
            status=400
        else:
            response, status = delete_ques_transaction(data)
        await log_info("/ques/delete", request.method, data, status, response)
        return jsonify({"data": response}), status

    except pymysql.Error as e:
        print(e)
        await log_error("/ques/delete", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}), 500
    except Exception as e:
        await log_error("/ques/delete", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}), 500
