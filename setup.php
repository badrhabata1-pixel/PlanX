<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إعداد جدول جديد</title>
    <!-- استدعاء مكتبة Bootstrap لتجميل التصميم -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
    <!-- خط تجوال العربي -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Tajawal', sans-serif; background-color: #f8f9fa; }
        .card-header { background-color: #2c3e50; color: white; font-weight: bold; }
        .form-label { font-weight: bold; color: #34495e; }
        .btn-primary { background-color: #27ae60; border: none; padding: 10px 30px; font-size: 1.1em; }
        .btn-primary:hover { background-color: #219150; }
        .upload-area { border: 2px dashed #bdc3c7; padding: 20px; border-radius: 10px; background: #fff; text-align: center; cursor: pointer; transition: 0.3s; }
        .upload-area:hover { border-color: #3498db; background: #ebf5fb; }
    </style>
</head>
<body>

<!-- شريط التنقل العلوي -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="#">🎓 نظام الجدولة الذكي</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item"><a class="nav-link" href="index.php">عرض الجدول الحالي</a></li>
        <li class="nav-item"><a class="nav-link active" href="setup.php">إنشاء جدول جديد</a></li>
      </ul>
    </div>
  </div>
</nav>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card shadow-lg">
                <div class="card-header text-center">
                    ⚙️ إعدادات الجدول الجديد
                </div>
                <div class="card-body p-4">
                    
                    <!-- الفورم بيبدأ من هنا -->
                    <!-- action: الصفحة اللي هتعالج البيانات (هنعملها الخطوة الجاية) -->
                    <form action="process_setup.php" method="POST" enctype="multipart/form-data">
                        
                        <!-- القسم الأول: بيانات يدوية -->
                        <h4 class="mb-3 text-primary border-bottom pb-2">1️⃣ البيانات الأساسية</h4>
                        <div class="row mb-4">
                            <div class="col-md-4">
                                <label class="form-label">عدد الأيام المتاحة</label>
                                <input type="number" name="days_count" class="form-control" value="5" min="1" required>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">عدد الفترات في اليوم</label>
                                <input type="number" name="periods_per_day" class="form-control" value="3" min="1" required>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">مدة الامتحان (ساعة)</label>
                                <input type="number" name="exam_duration" class="form-control" value="2" min="1">
                            </div>
                        </div>

                        <!-- القسم الثاني: رفع الملفات -->
                        <h4 class="mb-3 text-primary border-bottom pb-2">2️⃣ ملفات البيانات (CSV)</h4>
                        
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="upload-area">
                                    <label class="form-label d-block">📂 ملف الطلاب والمواد (Schedule/Enrollments)</label>
                                    <input type="file" name="schedule_csv" class="form-control" accept=".csv" required>
                                    <small class="text-muted">يجب أن يحتوي على: student_id, course_id</small>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="upload-area">
                                    <label class="form-label d-block">📘 ملف تعريف المواد (Courses)</label>
                                    <input type="file" name="courses_csv" class="form-control" accept=".csv">
                                    <small class="text-muted">يحتوي على: course_id, course_name</small>
                                </div>
                            </div>
                            
                            <div class="col-md-6">
                                <div class="upload-area">
                                    <label class="form-label d-block">🏫 ملف القاعات (Classrooms) - اختياري</label>
                                    <input type="file" name="classrooms_csv" class="form-control" accept=".csv">
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="upload-area">
                                    <label class="form-label d-block">👨‍🏫 ملف المراقبين (Instructors) - اختياري</label>
                                    <input type="file" name="instructors_csv" class="form-control" accept=".csv">
                                </div>
                            </div>
                        </div>

                        <!-- زرار الإرسال -->
                        <div class="text-center mt-5">
                            <button type="submit" class="btn btn-primary btn-lg shadow">
                                🚀 بدء المعالجة وإنشاء الجدول
                            </button>
                        </div>

                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<footer class="text-center mt-5 mb-3 text-muted">
    &copy; 2024 Exam Scheduling System - Graduation Project
</footer>

</body>
</html>
