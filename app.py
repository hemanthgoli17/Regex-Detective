from flask import Flask, request, render_template, redirect, url_for, session
import re,secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if "data" in session:  
            del session["data"]
        return render_template("home.html")

    if request.method == "POST":
        match_results = []
        regex = request.form.get("regex")
        text = request.form.get("text")
        email_id = request.form.get("email_id")
        if not email_id:
            match_results.append(regex)
            match_results.append(text)
            match_results.append(re.findall(regex, text))

            session["data"] = match_results  
            return redirect(url_for("results"))
        else:
            session["data"] = email_id
            return redirect(url_for("validate_email"))

@app.route("/results", methods=["GET"])
def results():
    if "data" not in session:  
        return redirect(url_for("home"))

    match_results = session["data"]
    del session["data"]  

    return render_template("regex_result.html", match_results=match_results)

@app.route("/validate_email", methods = ["GET"])
def validate_email():
    if "data" not in session:  
        return redirect(url_for("home"))
    valid_status = False
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
    email_id = session["data"]
    del session["data"]
    if email_pattern.match(email_id):
        valid_status = True
    return render_template("email_result.html", valid_status = valid_status, email_id = email_id)
if __name__ == '__main__':
    app.run(debug=True)