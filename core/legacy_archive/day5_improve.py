import pandas as pd
import matplotlib.pyplot as plt
import random

df = pd.read_csv("schedule.csv")
all_courses = list(df['course_id'].unique())
student_groups = df.groupby("student_id")["course_id"].apply(list)

graph = {c: set() for c in all_courses}
degree = {c: 0 for c in all_courses}

for courses in student_groups:
    if len(courses) < 2: continue
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            u, v = courses[i], courses[j]
            if v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                degree[u] += 1
                degree[v] += 1

student_counts = df.groupby("course_id")["student_id"].count()
score = {}

for course in all_courses:
    count = student_counts.get(course, 0)
    score[course] = (degree[course] * 20) + count     
sorted_courses = sorted(all_courses, key=lambda x: score[x], reverse=True)

solution = {}
for course in sorted_courses:
    neighbor_slots = {solution[neighbor] for neighbor in graph[course] if neighbor in solution}
    slot = 0
    while slot in neighbor_slots:
        slot += 1
    solution[course] = slot

num_slots = max(solution.values()) + 1

def calculate_detailed_cost(sol):
    penalty = 0
    problematic_slots = []
    
    for courses in student_groups:
        exam_slots = sorted([sol[c] for c in courses if c in sol])
        if len(exam_slots) < 2: continue
        
        for i in range(len(exam_slots) - 1):
            if exam_slots[i+1] - exam_slots[i] == 1:
                penalty += 1
                problematic_slots.append(exam_slots[i+1])
                
    return penalty, problematic_slots

current_cost, problems = calculate_detailed_cost(solution)
print(f"🔹 Initial Penalty: {current_cost}")

# زودنا الرقم هنا لـ 20000 لضمان نتيجة أفضل
for i in range(20000):
    if not problems:
        slot_a = random.randint(0, num_slots - 1)
    else:
        slot_a = random.choice(problems)
        
    slot_b = random.randint(0, num_slots - 1)
    
    if slot_a == slot_b: continue

    new_solution = solution.copy()
    for course, slot in new_solution.items():
        if slot == slot_a: new_solution[course] = slot_b
        elif slot == slot_b: new_solution[course] = slot_a
    
    new_cost, new_problems = calculate_detailed_cost(new_solution)
    
    if new_cost < current_cost:
        solution = new_solution
        current_cost = new_cost
        problems = new_problems

old_penalty = 1092 
final_penalty = current_cost

print("\n" + "="*40)
print(f"Old Penalty (Basic): {old_penalty}")
print(f"New Penalty (Targeted Hybrid): {final_penalty}")
print("="*40)

methods = ["Basic Greedy", "Targeted Hybrid"]
values = [old_penalty, final_penalty]

plt.figure(figsize=(8, 6))
bars = plt.bar(methods, values, color=['gray', '#e74c3c']) 
plt.title("Exam Schedule Optimization (Targeted Swapping)")
plt.ylabel("Total Student Penalty")
plt.ylim(0, max(values) * 1.2)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.savefig("final_targeted_comparison.png")
plt.show()

final_df = pd.DataFrame(list(solution.items()), columns=['course_id', 'slot_number'])
final_df.to_csv("day5_final_schedule.csv", index=False)