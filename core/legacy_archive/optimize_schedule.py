import pandas as pd
import random
import math
import copy

print("⏳ جاري تحسين الجدول باستراتيجية تبديل الفترات (Slot Swapping)...")

# ==========================================
# 1. التجهيز
# ==========================================
df = pd.read_csv("schedule.csv")

# قراءة الجدول المبدئي
initial_schedule_df = pd.read_csv("final_exam_schedule.csv")
# تحويله لقاموس {course_id: slot}
current_solution = dict(zip(initial_schedule_df.course_id, initial_schedule_df.slot_number))

# معرفة عدد الفترات الكلية
num_slots = max(current_solution.values()) + 1

# تجميع المواد لكل طالب (عشان نحسب الـ Penalty بسرعة)
student_courses = df.groupby("student_id")["course_id"].apply(list)

# ==========================================
# 2. دالة حساب التكلفة (سريعة)
# ==========================================
def calculate_cost(solution):
    total_penalty = 0
    # نلف على الطلاب
    for courses in student_courses:
        # هات أوقات امتحانات الطالب ده من الحل الحالي
        slots = []
        for course in courses:
            if course in solution:
                slots.append(solution[course])
        
        if len(slots) < 2: continue
        
        slots.sort()
        # حساب الغرامة (الفرق = 1)
        for i in range(len(slots) - 1):
            if slots[i+1] - slots[i] == 1:
                total_penalty += 1
    return total_penalty

# ==========================================
# 3. الخوارزمية الذكية (تبديل الفترات)
# ==========================================
current_cost = calculate_cost(current_solution)
best_solution = current_solution.copy()
best_cost = current_cost

print(f"🔹 التكلفة الحالية: {current_cost}")

temperature = 1000.0
cooling_rate = 0.99
iterations = 3000

for i in range(iterations):
    # 🎲 حركة ذكية: نختار فترتين عشوائيتين ونبدل كل امتحاناتهم
    slot_a = random.randint(0, num_slots - 1)
    slot_b = random.randint(0, num_slots - 1)
    
    if slot_a == slot_b: continue # لو نفس الفترة، فوت المحاولة

    # نسخ الحل الحالي عشان نجرب عليه
    new_solution = current_solution.copy()

    # التبديل: أي مادة في slot_a تروح لـ slot_b والعكس
    for course, slot in new_solution.items():
        if slot == slot_a:
            new_solution[course] = slot_b
        elif slot == slot_b:
            new_solution[course] = slot_a
    
    # حساب التكلفة الجديدة
    new_cost = calculate_cost(new_solution)

    # قبول أو رفض (Simulated Annealing Logic)
    accept = False
    if new_cost < current_cost:
        accept = True
        # لو ده أفضل حل وصلناله لحد دلوقتي، احفظه
        if new_cost < best_cost:
            best_cost = new_cost
            best_solution = new_solution.copy()
            print(f"🚀 تحسين رائع! التكلفة نزلت لـ: {best_cost} (محاولة {i})")
    else:
        # معادلة الاحتمال لقبول الحل الأسوأ (عشان نهرب من التكرار)
        probability = math.exp((current_cost - new_cost) / temperature)
        if random.random() < probability:
            accept = True
    
    if accept:
        current_solution = new_solution
        current_cost = new_cost
    
    # تبريد
    temperature *= cooling_rate

# ==========================================
# 4. النتيجة والحفظ
# ==========================================
print("\n" + "="*40)
print(f"🏆 النتيجة النهائية:")
print(f"🔹 التكلفة قبل: 1092")
print(f"✅ التكلفة بعد: {best_cost}")
improvement = 1092 - best_cost
print(f"📉 مقدار التحسين: وفرنا {improvement} حالة تعب للطلاب!")
print("="*40)

# حفظ
optimized_df = pd.DataFrame(list(best_solution.items()), columns=['course_id', 'slot_number'])
optimized_df.to_csv("smart_exam_schedule.csv", index=False)
print("💾 تم الحفظ في 'smart_exam_schedule.csv'")