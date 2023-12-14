from flask import Blueprint
from flask import request, jsonify
from logs.logs_setup import log_info,log_error
import pymysql
from transactions.user import (
    reg_user_transaction,
    get_user_transaction,
    delete_user_transaction,
)

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
async def reg_user():
    try:
        data = request.get_json()
        response,status = reg_user_transaction(data)
        await log_info("/user/register", request.method, data, status, response)
        return jsonify({"data": response}),status
    except pymysql.Error as e:
        print(e)
        await log_error("/user/register",request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/user/register",request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500


@user_bp.route("/get", methods=["POST"])
async def get_user():
    try:
        data = request.get_json()
        response,status = get_user_transaction(data)
        await log_info("/user/get", request.method, data, status, response)
        return jsonify({"data": response}),status
    except pymysql.Error as e:
        print(e)
        await log_error("/user/get",request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/user/get",request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500


@user_bp.route("/delete", methods=["DELETE"])
async def del_user():
    try:
        data = request.get_json()
        response,status = delete_user_transaction(data)
        await log_info("/user/delete", request.method, data, status, response)
        return jsonify({"data": response}),status
    except pymysql.Error as e:
        print(e)
        await log_error("/user/delete",request.method, data, e, 500)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message}),500
    except Exception as e:
        await log_error("/user/delete",request.method, data, e, 500)
        return jsonify({"data": "internal server error"}),500
