from flask import Blueprint
from flask import request, jsonify
import logging
import pymysql
from logs.logs_setup import log_info, log_error
from transactions.form import (
    create_form_transaction,
    display_form_transaction,
    delete_form_transaction,
)

form_bp = Blueprint("form", __name__)


@form_bp.route("/create", methods=["POST"])
async def create_form():
    try:
        data = request.get_json()

        if "questions" not in data.keys():
            response = "no questions added to form"
            status=400
        elif "user_id" not in data.keys():
            response = "user_id not added"
            status=400
        else:
            response,status = create_form_transaction(data)
        await log_info("/form/create", request.method, data, status, response)
        return jsonify({"data": response}),status

    except pymysql.Error as e:
        print(e)
        await log_error("/form/create", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/form/create", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500


@form_bp.route("/display", methods=["POST"])
async def display_form():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            response = "user_id not added"
            status=400
        elif "form_id" not in data.keys():
            response = "form_id not added"
            status=400
        else:
            response,status = display_form_transaction(data)
        await log_info("/form/display", request.method, data, status, response)
        return jsonify({"data": response}),status

    except pymysql.Error as e:
        print(e)
        await log_error("/form/display", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/form/display", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500


@form_bp.route("/delete", methods=["DELETE"])
async def delete_form():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            response = "user_id not added"
            status=400
        elif "form_id" not in data.keys():
            response = "form_id not added"
            status=400
        else:
            response,status = delete_form_transaction(data)
        await log_info("/form/delete", request.method, data, status, response)
        return jsonify({"data": response}),status

    except pymysql.Error as e:
        print(e)
        await log_error("/form/delete", request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/form/delete", request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500
