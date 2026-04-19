from models.course import Course
from models.exam_offering import ExamOffering
from models.student import Student
from models.enrollment import Enrollment
from ingestion.loaders import load_all_xls_sheets
from ingestion.normalizers import clean_text, clean_float_or_none


def parse_roster_excel(file_path: str):
    workbook = load_all_xls_sheets(file_path)

    courses = []
    exam_offerings = []
    students = []
    enrollments = []

    seen_courses = set()
    seen_students = set()
    seen_enrollments = set()

    for sheet_name, df in workbook.items():
        current_course_code = None
        current_course_name = None
        current_semester = None
        reading_students = False

        for _, row in df.iterrows():
            values = [clean_text(x) for x in row.tolist()]
            non_empty = [v for v in values if v != ""]

            if not non_empty:
                continue

            first_cell = non_empty[0]

            # Detect course header
            if "|" in first_cell and len(first_cell) < 120:
                parts = first_cell.split("|", 1)
                current_course_code = parts[0].strip()
                current_course_name = parts[1].strip()

                if current_course_code not in seen_courses:
                    courses.append(
                        Course(
                            course_code=current_course_code,
                            course_name=current_course_name,
                        )
                    )
                    exam_offerings.append(
                        ExamOffering(
                            course_code=current_course_code,
                            course_name=current_course_name,
                            students_no=0,
                        )
                    )
                    seen_courses.add(current_course_code)

                reading_students = False
                continue

            # Detect semester row
            if "Spring" in first_cell or "Fall" in first_cell:
                current_semester = first_cell

                for c in courses:
                    if c.course_code == current_course_code and c.academic_semester is None:
                        c.academic_semester = current_semester

                for eo in exam_offerings:
                    if eo.course_code == current_course_code and eo.academic_semester is None:
                        eo.academic_semester = current_semester
                continue

            # Detect table header
            if "Student Name" in values:
                reading_students = True
                continue

            # Read student rows
            if reading_students and current_course_code:
                student_id = clean_text(row.iloc[1]) if len(row) > 1 else ""
                student_name = clean_text(row.iloc[2]) if len(row) > 2 else ""
                level_text = clean_text(row.iloc[4]) if len(row) > 4 else ""
                cgpa = clean_float_or_none(row.iloc[5]) if len(row) > 5 else None

                if student_id == "" or student_name == "":
                    continue

                if student_id not in seen_students:
                    students.append(
                        Student(
                            student_id=student_id,
                            student_name=student_name,
                            level_text=level_text if level_text else None,
                            cgpa=cgpa,
                        )
                    )
                    seen_students.add(student_id)

                enrollment_key = (student_id, current_course_code)
                if enrollment_key not in seen_enrollments:
                    enrollments.append(
                        Enrollment(
                            student_id=student_id,
                            course_code=current_course_code,
                        )
                    )
                    seen_enrollments.add(enrollment_key)

    # Update students_no for each exam offering
    enrollment_count_by_course = {}
    for e in enrollments:
        enrollment_count_by_course[e.course_code] = enrollment_count_by_course.get(e.course_code, 0) + 1

    for eo in exam_offerings:
        eo.students_no = enrollment_count_by_course.get(eo.course_code, 0)

    return courses, exam_offerings, students, enrollments