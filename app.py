from flask import Flask
from flask import request, jsonify
from routes.user_routes import user_bp
from routes.form_routes import form_bp
from routes.ques_routes import ques_bp
from routes.ans_routes import ans_bp
from logs.logs_setup import get_ratios

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(form_bp, url_prefix="/form")
app.register_blueprint(ques_bp, url_prefix="/ques")
app.register_blueprint(ans_bp, url_prefix="/ans")

@app.route("/syshealth", methods=["GET"])
def syshealth():
    return jsonify(get_ratios()),200


if __name__ == "__main__":
    app.run(debug=True)
