import pandas as pd
import matplotlib.pyplot as plt
import random

# ========================
# 1️⃣ قراءة البيانات
# ========================
df = pd.read_csv("schedule.csv")

all_courses = list(df['course_id'].unique())
student_groups = df.groupby("student_id")["course_id"].apply(list)

# ========================
# 2️⃣ بناء جراف التعارض
# ========================
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

# ========================
# 3️⃣ حساب وزن كل مادة
# ========================
student_counts = df.groupby("course_id")["student_id"].count()
score = {}

for course in all_courses:
    score[course] = degree[course] * 20 + student_counts.get(course, 0)

sorted_courses = sorted(all_courses, key=lambda x: score[x], reverse=True)

# ========================
# 4️⃣ Greedy Coloring
# ========================
solution = {}

for course in sorted_courses:
    used_slots = {solution[n] for n in graph[course] if n in solution}
    slot = 0
    while slot in used_slots:
        slot += 1
    solution[course] = slot

num_slots = max(solution.values()) + 1

# ========================
# 5️⃣ دالة حساب العقوبة
# ========================
def calculate_cost(sol):
    penalty = 0
    for courses in student_groups:
        slots = sorted(sol[c] for c in courses if c in sol)
        for i in range(len(slots) - 1):
            if slots[i+1] - slots[i] == 1:
                penalty += 1
    return penalty

# ========================
# 6️⃣ تحسين Local Search
# ========================
current_cost = calculate_cost(solution)

for _ in range(1000):
    a = random.randint(0, num_slots - 1)
    b = random.randint(0, num_slots - 1)
    if a == b:
        continue

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

print("✅ Final Penalty:", current_cost)

# ========================
# 7️⃣ تحويل الحل لجدول مفهوم
# ========================

PERIODS_PER_DAY = 10

rows = []
for course, slot in solution.items():
    rows.append({ 
        "Course": course,
        "Slot": slot,
        "Day": (slot // PERIODS_PER_DAY) + 1,
        "Period": (slot % PERIODS_PER_DAY) + 1,
        "Students": student_counts.get(course, 0),
        "Conflicts": degree.get(course, 0)
    })

final_table = pd.DataFrame(rows).sort_values(["Day", "Period"])

# ========================
# 8️⃣ حفظ الجدول النهائي
# ========================
final_table.to_csv("FINAL_EXAM_SCHEDULE.csv", index=False)
print("📁 تم حفظ الجدول في FINAL_EXAM_SCHEDULE.csv")

# ========================
# 9️⃣ عرض الجدول
# ========================
print("\n📋 جدول الامتحانات النهائي:\n")
print(final_table)
