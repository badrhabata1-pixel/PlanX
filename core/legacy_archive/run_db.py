import pandas as pd
import random
import os
import sys

# ==========================================
# 1. استقبال المدخلات من PHP
# ==========================================
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# القيم الافتراضية (لو مفيش حاجة اتبعتت)
USER_DAYS = 5
PERIODS_PER_DAY = 3

# استقبال القيم من سطر الأوامر (PHP)
if len(sys.argv) > 2:
    try:
        USER_DAYS = int(sys.argv[1])      # المتغير الأول: عدد الأيام
        PERIODS_PER_DAY = int(sys.argv[2]) # المتغير الثاني: عدد الفترات
        print(f">> Configuration Received: {USER_DAYS} Days | {PERIODS_PER_DAY} Slots/Day")
    except ValueError:
        print(">> Warning: Invalid inputs, using defaults.")

# ==========================================
# 2. تجهيز البيئة والمسارات
# ==========================================
BASE_DIR = os.getcwd() 
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'input', 'schedule.csv')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'exports', 'final_schedule.csv')

print(">> Python Engine Started (Dynamic Mode)...")

# قراءة الملف
try:
    df = pd.read_csv(INPUT_FILE)
    print(f">> Loaded {len(df)} records.")
except FileNotFoundError:
    print(f"[ERROR] Input file not found at {INPUT_FILE}")
    exit()

# ==========================================
# 3. بداية الخوارزمية
# ==========================================

all_courses = list(df['course_id'].unique())
student_groups = df.groupby("student_id")["course_id"].apply(list)

# --- بناء الجراف ---
print(">> Building Conflict Graph...")
graph = {c: set() for c in all_courses}
degree = {c: 0 for c in all_courses}

for courses in student_groups:
    if len(courses) < 2:
        continue
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            u, v = courses[i], courses[j]
            if v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                degree[u] += 1
                degree[v] += 1

# --- حساب الأوزان ---
student_counts = df.groupby("course_id")["student_id"].count()
score = {}

for course in all_courses:
    score[course] = degree[course] * 20 + student_counts.get(course, 0)

sorted_courses = sorted(all_courses, key=lambda x: score[x], reverse=True)

# --- البناء (Greedy Coloring) ---
solution = {}

for course in sorted_courses:
    used_slots = {solution[n] for n in graph[course] if n in solution}
    slot = 0
    while slot in used_slots:
        slot += 1
    solution[course] = slot

# هنا بنحسب الحد الأقصى للفترات بناءً على المدخلات
# لو الخوارزمية احتاجت فترات أكتر من المسموح بيه (الأيام * الفترات)، بنكمل عادي بس ممكن نعمل تحذير
calculated_max_slots = max(solution.values()) + 1
print(f">> Total Slots Used: {calculated_max_slots}")

# --- دالة حساب التكلفة ---
def calculate_cost(sol):
    penalty = 0
    for courses in student_groups:
        slots = sorted([sol[c] for c in courses if c in sol])
        for i in range(len(slots) - 1):
            if slots[i+1] - slots[i] == 1:
                penalty += 1
    return penalty

# --- التحسين (Local Search) ---
current_cost = calculate_cost(solution)
print(f"-> Initial Penalty: {current_cost}")

ITERATIONS = 2000 
num_slots = calculated_max_slots # نستخدم الفترات الفعلية للتبديل

for _ in range(ITERATIONS):
    a = random.randint(0, num_slots - 1)
    b = random.randint(0, num_slots - 1)
    if a == b: continue

    new_solution = solution.copy()
    for course in new_solution:
        if new_solution[course] == a:
            new_solution[course] = b
        elif new_solution[course] == b:
            new_solution[course] = a

    new_cost = calculate_cost(new_solution)
    
    if new_cost < current_cost:
        solution = new_solution
        current_cost = new_cost

print(f"[OK] Final Penalty: {current_cost}")

# ==========================================
# 4. تجهيز المخرجات (الحساب الديناميكي لليوم والفترة)
# ==========================================
# هنا السحر كله: بنستخدم المتغير اللي استلمناه من PHP
# PERIODS_PER_DAY

# ==========================================
# 4. تجهيز المخرجات (التصحيح: التوزيع بناءً على الأيام المحددة)
# ==========================================

# 1. بنشوف الخوارزمية احتاجت كام مكان فعلياً
actual_total_slots = max(solution.values()) + 1

# 2. بنحسب "الفترات المطلوبة في اليوم الواحد" عشان نكفي الأيام اللي أنت حددتها
# لو أنت قايل 5 أيام، واحتاجنا 24 مكان -> يبقى لازم اليوم يشيل 5 فترات (مش 3 زي ما دخلت)
import math
required_periods_per_day = math.ceil(actual_total_slots / USER_DAYS)

# 3. بنستخدم الرقم الجديد ده في التقسيم عشان نضمن إن الأيام متزدش عن USER_DAYS
calc_periods = max(PERIODS_PER_DAY, required_periods_per_day)

rows = []
for course, slot in solution.items():
    # المعادلة المعدلة
    calculated_day = (slot // calc_periods) + 1
    calculated_period = (slot % calc_periods) + 1
    
    rows.append({ 
        "course_id": course,
        "slot_number": slot,
        "exam_day": calculated_day,
        "exam_period": calculated_period,
        "total_students": student_counts.get(course, 0),
        "conflicts_count": degree.get(course, 0)
    })

final_table = pd.DataFrame(rows).sort_values(["exam_day", "exam_period"])
# ==========================================
# 5. الحفظ
# ==========================================
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
try:
    final_table.to_csv(OUTPUT_FILE, index=False)
    print(f"[SUCCESS] Schedule exported to: {OUTPUT_FILE}")
except Exception as e:
    print(f"[ERROR] Could not write file: {e}")