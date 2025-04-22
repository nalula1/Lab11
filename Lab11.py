import os
import matplotlib.pyplot as plt


def read_students(filename):
    students = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            student_id = line[:3]
            student_name = line[3:]
            students[student_id] = student_name
    return students


def read_assignments(filename):
    assignments = {}
    assignment_names = {}
    total_points = 0

    with open(filename, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            name = lines[i].strip()
            assignment_id = lines[i + 1].strip()
            points = int(lines[i + 2].strip())
            assignments[assignment_id] = (name, points)
            assignment_names[name] = (assignment_id, points)
            total_points += points
            i += 3

    return assignments, assignment_names, total_points


def read_submissions(directory):
    submissions = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename not in ['students.txt', 'assignments.txt']:
            with open(filepath, 'r') as file:
                content = file.read().strip()
                if '|' in content:
                    parts = content.split('|')
                    if len(parts) == 3:
                        student_id = parts[0]
                        assignment_id = parts[1]
                        percentage = int(parts[2])

                        if student_id not in submissions:
                            submissions[student_id] = {}

                        submissions[student_id][assignment_id] = percentage

    return submissions

def calculate_student_grade(student_id, submissions, assignments, total_points):
    if student_id not in submissions:
        return 0

    student_submissions = submissions[student_id]
    earned_points = 0

    for assignment_id, percentage in student_submissions.items():
        if assignment_id in assignments:
            _, points = assignments[assignment_id]
            earned_points += (percentage / 100) * points

    return (earned_points / total_points) * 100


def get_assignment_stats(assignment_id, submissions, students):
    scores = []

    for student_id, student_submissions in submissions.items():
        if assignment_id in student_submissions:
            scores.append(student_submissions[assignment_id])

    if not scores:
        return None

    min_score = min(scores)
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)

    return min_score, avg_score, max_score, scores


def main():

    data_dir = 'data'
    students = read_students(os.path.join(data_dir, 'students.txt'))
    assignments, assignment_names, total_points = read_assignments(os.path.join(data_dir, 'assignments.txt'))
    submissions = read_submissions(data_dir)

    # Display menu
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("Enter your selection: ")

    if selection == '1':
        student_name = input("What is the student's name: ")
        student_id = None

        for sid, name in students.items():
            if name == student_name:
                student_id = sid
                break

        if student_id is None:
            print("Student not found")
        else:
            grade = calculate_student_grade(student_id, submissions, assignments, total_points)
            print(f"{round(grade)}%")

    elif selection == '2':
        assignment_name = input("What is the assignment name: ")

        if assignment_name not in assignment_names:
            print("Assignment not found")
        else:
            assignment_id, _ = assignment_names[assignment_name]
            stats = get_assignment_stats(assignment_id, submissions, students)

            if stats is None:
                print("No submissions found for this assignment")
            else:
                min_score, avg_score, max_score, _ = stats
                print(f"Min: {min_score}%")
                print(f"Avg: {round(avg_score)}%")
                print(f"Max: {max_score}%")

    elif selection == '3':
        assignment_name = input("What is the assignment name: ")

        if assignment_name not in assignment_names:
            print("Assignment not found")
        else:
            assignment_id, _ = assignment_names[assignment_name]
            stats = get_assignment_stats(assignment_id, submissions, students)

            if stats is None:
                print("No submissions found for this assignment")
            else:
                _, _, _, scores = stats
                plt.hist(scores, bins=[0, 25, 50, 75, 100])
                plt.title(f"{assignment_name} Scores")
                plt.xlabel("Score (%)")
                plt.ylabel("Number of Students")
                plt.show()


if __name__ == "__main__":
    main()