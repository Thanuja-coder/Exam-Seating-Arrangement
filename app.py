from flask import Flask, render_template, request
from main import load_students, segregate_by_branch, generate_seating

app = Flask(__name__)

seat_map = {}
exam_details = {}


@app.route("/", methods=["GET", "POST"])
def admin():
    global seat_map, exam_details
    seating_generated = False

    if request.method == "POST":
        exam_details["exam"] = request.form["exam"]
        exam_details["subject"] = request.form["subject"]
        exam_details["date"] = request.form["date"]
        rooms = int(request.form["rooms"])

        students = load_students()
        branches = segregate_by_branch(students)
        seat_map = generate_seating(branches, rooms)
        seating_generated = True
        return render_template("student.html")

    if seating_generated:
        return render_template("student.html")
    return render_template("admin.html")



@app.route("/dashboard", methods=["POST"])
def dashboard():
    usn = request.form["usn"]

    if usn in seat_map:
        return render_template(
            "dashboard.html",
            usn=usn,
            seat=seat_map[usn],
            exam=exam_details
        )

    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
