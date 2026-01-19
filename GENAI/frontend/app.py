from flask import Flask, app, request, jsonify
from flask import render_template


app = Flask(__name__)
@app.route("/")
def home():
    return render_template("customer-interface.html")

if __name__ == "__main__":
    app.run(debug=True)