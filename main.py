import csv

ROOM_CAPACITY = 20  # 10 benches × 2 students


# ------------------ STEP 1: LOAD STUDENTS ------------------
def load_students():
    students = []

    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append({
                "name": row["Name"],
                "usn": row["USN"],
                "branch": row["Branch"]
            })

    return students


# ------------------ STEP 2: BRANCH SEGREGATION ------------------
def segregate_by_branch(students):
    branches = {}

    for student in students:
        branch = student["branch"]
        if branch not in branches:
            branches[branch] = []
        branches[branch].append(student)

    return branches


# ------------------ STEP 3: SEATING LOGIC ------------------
def generate_seating(branches, num_rooms):
    student_pool = []
    for b in branches.values():
        student_pool.extend(b)

    total_students = len(student_pool)
    total_capacity = num_rooms * ROOM_CAPACITY

    if total_capacity < total_students:
        return None

    seat_map = {}
    student_index = 0

    for room_no in range(1, num_rooms + 1):
        for bench_no in range(1, 11):

            if student_index >= len(student_pool):
                break

            student1 = student_pool[student_index]
            student_index += 1

            student2 = None
            for i in range(student_index, len(student_pool)):
                if student_pool[i]["branch"] != student1["branch"]:
                    student2 = student_pool.pop(i)
                    break

            seat_map[student1["usn"]] = {
                "room": room_no,
                "bench": bench_no,
                "seat": "Left"
            }

            if student2:
                seat_map[student2["usn"]] = {
                    "room": room_no,
                    "bench": bench_no,
                    "seat": "Right"
                }

    return seat_map


# ------------------ STEP 4: TERMINAL DASHBOARD ------------------
def student_dashboard(seat_map):
    print("\n--- STUDENT DASHBOARD ---")

    while True:
        usn = input("\nEnter USN (or EXIT): ").strip()
        if usn.upper() == "EXIT":
            break

        if usn in seat_map:
            s = seat_map[usn]
            print(f"Exam   : {exam_name}")
            print(f"Subject: {subject}")
            print(f"Date   : {exam_date}")

        else:
            print("Invalid USN")


# ------------------ MAIN EXECUTION ------------------
if __name__ == "__main__":

    students = load_students()
    branches = segregate_by_branch(students)
    exam_name = input("Enter Exam Name: ")
    subject = input("Enter Subject: ")
    exam_date = input("Enter Exam Date (DD-MM-YYYY): ")
    num_rooms = int(input("Enter number of rooms: "))


    seat_map = generate_seating(branches, num_rooms)

    if seat_map is None:
        print("Not enough rooms.")
    else:
        student_dashboard(seat_map)
