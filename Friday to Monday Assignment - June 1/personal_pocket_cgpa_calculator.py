"""
COS202 Assignment - Personal Pocket CGPA Calculator (PPC)
-----------------------------------------------------------
A console-based CGPA calculator built with Python's selection control
statements (if / elif / else), so you can check your CGPA anytime
without needing to log in to AVERS.

Grading scale used (AAUA 5-point scale):
    A  = 5.0   (70 - 100)
    B  = 4.0   (60 - 69)
    C  = 3.0   (50 - 59)
    D  = 2.0   (45 - 49)
    E  = 1.0   (40 - 44)
    F  = 0.0   (0  - 39)

Author: Kayode
Course: COS202
"""


def score_to_grade_point(score):
    """Convert a numeric score (0-100) to a grade letter and grade point
    using selection control statements."""
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")

    if score >= 70:
        return "A", 5.0
    elif score >= 60:
        return "B", 4.0
    elif score >= 50:
        return "C", 3.0
    elif score >= 45:
        return "D", 2.0
    elif score >= 40:
        return "E", 1.0
    else:
        return "F", 0.0


def letter_to_grade_point(letter):
    """Convert a grade letter directly to a grade point, using selection
    control statements. Useful if the user already knows their letter grade."""
    letter = letter.strip().upper()

    if letter == "A":
        return 5.0
    elif letter == "B":
        return 4.0
    elif letter == "C":
        return 3.0
    elif letter == "D":
        return 2.0
    elif letter == "E":
        return 1.0
    elif letter == "F":
        return 0.0
    else:
        raise ValueError(f"Unknown grade letter: {letter}")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid number, please try again.")


def get_course_input(course_number):
    print(f"\n--- Course {course_number} ---")
    course_code = input("Course code (e.g. COS202): ").strip().upper()
    units = get_positive_float("Credit units: ")

    while True:
        mode = input("Enter grade as (S)core or (L)etter? [S/L]: ").strip().upper()
        if mode == "S":
            score = float(input("Score (0-100): "))
            grade, gp = score_to_grade_point(score)
            break
        elif mode == "L":
            letter = input("Letter grade (A/B/C/D/E/F): ")
            grade = letter.strip().upper()
            gp = letter_to_grade_point(grade)
            break
        else:
            print("Please type S or L.")

    quality_points = gp * units
    print(f"-> {course_code}: Grade {grade}, GP {gp}, Units {units}, "
          f"Quality Points = {gp} x {units} = {quality_points}")
    return {
        "code": course_code,
        "units": units,
        "grade": grade,
        "grade_point": gp,
        "quality_points": quality_points,
    }


def calculate_gpa(courses):
    total_units = sum(c["units"] for c in courses)
    total_quality_points = sum(c["quality_points"] for c in courses)
    if total_units == 0:
        return 0.0
    return total_quality_points / total_units


def print_report(courses, gpa):
    print("\n" + "=" * 50)
    print("PERSONAL POCKET CGPA CALCULATOR - REPORT")
    print("=" * 50)
    print(f"{'Course':<10}{'Units':<8}{'Grade':<8}{'GP':<6}{'Q.Points':<10}")
    print("-" * 50)
    total_units = 0
    total_qp = 0
    for c in courses:
        print(f"{c['code']:<10}{c['units']:<8}{c['grade']:<8}{c['grade_point']:<6}{c['quality_points']:<10}")
        total_units += c["units"]
        total_qp += c["quality_points"]
    print("-" * 50)
    print(f"Total Units: {total_units}   Total Quality Points: {total_qp}")
    print(f"\nGPA for this semester: {gpa:.2f} / 5.00")

    # Selection statements to give feedback on class of degree standing
    if gpa >= 4.50:
        remark = "First Class range"
    elif gpa >= 3.50:
        remark = "Second Class Upper range"
    elif gpa >= 2.40:
        remark = "Second Class Lower range"
    elif gpa >= 1.50:
        remark = "Third Class range"
    else:
        remark = "Below Third Class - needs improvement"
    print(f"Standing: {remark}")
    print("=" * 50)


def main():
    print("Welcome to your Personal Pocket CGPA Calculator (PPC)")
    print("Check your GPA anytime, anywhere - no need for AVERS!\n")

    courses = []
    while True:
        course = get_course_input(len(courses) + 1)
        courses.append(course)

        again = input("\nAdd another course? (Y/N): ").strip().upper()
        if again == "N":
            break
        elif again != "Y":
            print("Assuming 'No'. Ending course entry.")
            break

    gpa = calculate_gpa(courses)
    print_report(courses, gpa)

    print("\nThank you for using PPC. Stay on top of your CGPA!")


if __name__ == "__main__":
    main()
