import pandas as pd

print("⏳ جاري تحميل البيانات وبناء الجدول...")

# 1️⃣ قراءة البيانات وحساب التعارضات (زي ما عملنا قبل كده)
df = pd.read_csv("schedule.csv")
all_courses = df['course_id'].unique()

# بناء قائمة المواد لكل طالب
student_courses = df.groupby("student_id")["course_id"].apply(list)

# بناء "رسم بياني للتعارضات" (Graph)
# كل مادة هتعرف مين المواد اللي بتتعارض معاها
graph = {course: set() for course in all_courses}

for courses in student_courses:
    if len(courses) < 2: continue
    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            u, v = courses[i], courses[j]
            graph[u].add(v)
            graph[v].add(u)

# ==========================================
# 🧠 الخوارزمية الجشعة (Greedy Algorithm)
# ==========================================
print("🤖 تشغيل خوارزمية الجدول (Greedy Coloring)...")

# ترتيب المواد: نبدأ بالمواد اللي عندها تعارضات أكتر (الأصعب)
# ده بيخلي الجدول مضغوط وأحسن
sorted_courses = sorted(all_courses, key=lambda x: len(graph[x]), reverse=True)

solution = {}  # قاموس لتخزين النتيجة: {course_id: time_slot}

for course in sorted_courses:
    # 1. شوف جيران المادة دي (المواد المتعارضة معاها) أخدوا أوقات إيه؟
    neighbor_slots = {solution[neighbor] for neighbor in graph[course] if neighbor in solution}
    
    # 2. اختار أول وقت (Slot) متاح مش موجود عند الجيران
    slot = 0
    while slot in neighbor_slots:
        slot += 1
        
    # 3. سجل الوقت للمادة
    solution[course] = slot

# ==========================================
# 🕵️‍♂️ التحقق من الحل (Testing)
# ==========================================
print(f"✅ تم إنشاء الجدول! عدد الفترات المطلوبة: {max(solution.values()) + 1}")

print("\n🔍 جاري التحقق من صحة الجدول (Conflict Check)...")
has_error = False

# نلف على كل طالب ونشوف هل عنده امتحانين في نفس الـ Slot؟
for student, courses in student_courses.items():
    slots_taken = [solution[c] for c in courses if c in solution]
    
    # لو عدد الأوقات أقل من عدد المواد، يبقى فيه تكرار (تعارض)
    if len(slots_taken) != len(set(slots_taken)):
        print(f"❌ مصيبة! الطالب {student} عنده تعارض في المواد {courses}")
        has_error = True
        break

if not has_error:
    print("🎉 النتيجة: الجدول سليم 100% (لا يوجد أي تعارض في نفس الفترة).")

# ==========================================
# 💾 حفظ الجدول النهائي
# ==========================================
# تحويل القاموس لجدول وحفظه
final_schedule = pd.DataFrame(list(solution.items()), columns=['course_id', 'slot_number'])
final_schedule.to_csv("final_exam_schedule.csv", index=False)
print("💾 تم حفظ الجدول في ملف 'final_exam_schedule.csv'")