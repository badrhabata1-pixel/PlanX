import pandas as pd

print("⏳ جاري حساب جودة الجدول (Penalty)...")

# ==========================================
# Step 1: نربط كل طالب بجدوله
# ==========================================
# قراءة ملف الجدول الأصلي (مين بياخد إيه)
original_schedule = pd.read_csv("schedule.csv")

# قراءة ملف الجدول النهائي (إمتى الامتحان)
final_schedule = pd.read_csv("final_exam_schedule.csv")

# دمج الجدولين عشان يبقى عندنا (الطالب -> المادة -> وقت الامتحان)
# بنقوله: ضيف عمود 'slot_number' لكل مادة بناءً على 'course_id'
full_data = original_schedule.merge(final_schedule, on="course_id")

# ==========================================
# Step 2: نجمع امتحانات كل طالب مع الفترات
# ==========================================
# لكل طالب، هات قائمة أرقام الفترات (Slots) اللي عنده فيها امتحان
# النتيجة: الطالب X عنده امتحانات في الأوقات [0, 5, 1, 20]
student_slots = full_data.groupby("student_id")["slot_number"].apply(list)

# ==========================================
# Step 3: نحسب الـ Penalty
# ==========================================
total_penalty = 0           # إجمالي الغرامات لكل الطلاب
students_affected = 0       # عدد الطلاب المتضررين

# نلف على طالب طالب
for slots in student_slots:
    # 1. ترتيب الأوقات (مهم جداً!)
    # لازم نرتب عشان نعرف نقارن الامتحان باللي بعده (مثلاً: 0, 1, 5)
    slots.sort()
    
    current_student_penalty = 0
    
    # 2. نقارن كل امتحان باللي بعده
    for i in range(len(slots) - 1):
        # الوقت الحالي
        current_exam = slots[i]
        # الوقت اللي بعده
        next_exam = slots[i+1]
        
        # 3. حساب الفرق
        diff = next_exam - current_exam
        
        # لو الفرق = 1 (يعني ورا بعض مباشرة) -> زود غرامة
        if diff == 1:
            current_student_penalty += 1
            
    # تجميع الغرامات
    if current_student_penalty > 0:
        total_penalty += current_student_penalty
        students_affected += 1

# ==========================================
# Step 4: طباعة النتيجة
# ==========================================
print("\n" + "="*40)
print("📊 تقرير جودة الجدول (Penalty Report)")
print("="*40)
print(f"🔹 إجمالي عدد الطلاب: {len(student_slots)}")
print(f"🔹 عدد الطلاب المتضررين (امتحانات متتالية): {students_affected}")
print(f"🔴 إجمالي نقاط الـ Penalty (كلما قل الرقم كان أفضل): {total_penalty}")

avg_penalty = total_penalty / len(student_slots)
print(f"📈 متوسط الـ Penalty لكل طالب: {avg_penalty:.4f}")
print("="*40)