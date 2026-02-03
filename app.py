from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os, json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheet connect
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1D856b4YOda1eeFAGcOVXSNgRq6vAw_KS6XwAytESS7E").sheet1

@app.route("/")
def home():
    return render_template("index.html")   # ✅ index.html open karega

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
    else:
        query = request.args.get("query", "").strip().lower()

    records = sheet.get_all_records()

    # Clean headers
    cleaned_records = []
    for row in records:
        cleaned_row = {k.strip(): str(v).strip() for k, v in row.items()}
        cleaned_records.append(cleaned_row)

    # Search
    results = [
        row for row in cleaned_records
        if query in row.get("Name", "").lower()
    ]

    # ✅ JSON ke jagah HTML render karo
    return render_template("index.html", results=results, query=query)


if __name__ == "__main__":
    app.run(debug=True)

