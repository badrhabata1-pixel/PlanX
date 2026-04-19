import pandas as pd

print("⏳ جاري تجهيز الجدول النهائي للطباعة...")

# 1. قراءة الملفات
# لاحظ: هنقرأ الجدول الذكي اللي لسة طالع
schedule = pd.read_csv("smart_exam_schedule.csv") 
courses = pd.read_csv("courses.csv")
timeslots = pd.read_csv("timeslots.csv")

# 2. ربط الجدول بأسماء المواد
final_df = schedule.merge(courses[['course_id', 'course_name']], on="course_id")

# 3. ربط الـ Slots بالأيام والساعات
# بنرتب الـ timeslots ونديهم أرقام (0, 1, 2...) عشان نربطهم بالجدول
timeslots['slot_number'] = range(len(timeslots)) 

final_df = final_df.merge(timeslots[['slot_number', 'day', 'start_time', 'end_time']], on="slot_number", how="left")

# 4. الترتيب النهائي (حسب اليوم والوقت)
final_df = final_df.sort_values("slot_number")

# 5. تنظيف الجدول (اختيار الأعمدة المهمة بس)
export_df = final_df[['course_id', 'course_name', 'day', 'start_time', 'end_time']]

# 6. الحفظ
export_df.to_csv("FINAL_SMART_SCHEDULE.csv", index=False)

print("\n" + "="*40)
print("🎉 مبروووك! تم استخراج الجدول النهائي.")
print("📄 اسم الملف: FINAL_SMART_SCHEDULE.csv")
print("="*40)
print(export_df.head(10).to_string(index=False)) # عرض أول 10 أسطر