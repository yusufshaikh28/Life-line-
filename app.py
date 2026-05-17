from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallbackkey")

client = MongoClient(os.getenv("MONGO_URI"))
db = client["blooddb"]
collection = db["donors"]

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")
client = MongoClient(os.getenv("MONGO_URI"))
db = client["blooddb"]
collection = db["donors"]

# ---------------- HOME ----------------
@app.route("/")
def home():
    total = collection.count_documents({})
    return render_template("home.html", total=total)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        collection.insert_one({
            "name": request.form["name"],
            "blood": request.form["blood"],
            "city": request.form["city"],
            "mobile": request.form["mobile"]
        })
        return redirect("/register")
    return render_template("register.html")

# ---------------- SEARCH ----------------
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        results = collection.find({
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"blood": {"$regex": keyword, "$options": "i"}},
                {"city": {"$regex": keyword, "$options": "i"}}
            ]
        })
    return render_template("search.html", results=results)

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
    return render_template("admin_login.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin/login")

    donors = list(collection.find().sort("_id", -1))
    total = collection.count_documents({})
    return render_template("admin.html", donors=donors, total=total)

# ---------------- DELETE ----------------
@app.route("/admin/delete/<id>")
def delete_donor(id):
    if not session.get("admin"):
        return redirect("/admin/login")

    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/admin")

# ---------------- EDIT ----------------
@app.route("/admin/edit/<id>", methods=["GET", "POST"])
def edit_donor(id):
    if not session.get("admin"):
        return redirect("/admin/login")

    donor = collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "blood": request.form["blood"],
                "city": request.form["city"],
                "mobile": request.form["mobile"]
            }}
        )
        return redirect("/admin")

    return render_template("edit.html", donor=donor)

# ---------------- LOGOUT ----------------
@app.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)