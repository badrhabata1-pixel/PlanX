import pandas as pd

print("⏳ جاري تحميل البيانات وحساب التعارضات...")

df = pd.read_csv("schedule.csv")

grouped = df.groupby("student_id")["course_id"].apply(list)

conflicts = set()
for courses_list in grouped:
    if len(courses_list) < 2:
        continue
    for i in range(len(courses_list)):
        for j in range(i + 1, len(courses_list)):
           
            pair = tuple(sorted((courses_list[i], courses_list[j])))
            conflicts.add(pair)

conflict_df = pd.DataFrame(list(conflicts), columns=['exam1', 'exam2'])


conflict_df.to_csv("conflict_list.csv", index=False)
print("✅ تم حفظ ملف 'conflict_list.csv' بنجاح!")


total_exams = df['course_id'].nunique()     
total_students = df['student_id'].nunique()  
total_conflicts = len(conflicts)           

print("\n" + "="*30)
print("📄 تقرير Day 2 (جاهز للنسخ)")
print("="*30)

print(f"1. عدد الامتحانات (Courses): {total_exams}")
print(f"2. عدد الطلاب: {total_students}")
print(f"3. عدد التعارضات: {total_conflicts}")
print("\n4. شرح يعني إيه Conflict:")
print("   الـ Conflict (التعارض) يحدث عندما يكون هناك طالب واحد مسجل في مادتين مختلفتين.")
print("   وهذا يعني أنه لا يمكن جدولة امتحان المادتين في نفس الفترة الزمنية (Timeslot)،")
print("   لأن الطالب لا يستطيع حضور امتحانين في نفس الوقت.")
print("="*30)