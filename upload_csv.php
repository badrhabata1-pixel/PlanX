<?php
// إعدادات الاتصال
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "exam_system_db";

// إنشاء الاتصال
$conn = new mysqli($servername, $username, $password, $dbname);

// التأكد من الاتصال
if ($conn->connect_error) {
    die("فشل الاتصال: " . $conn->connect_error);
}

// اسم ملف الجدول النهائي (تأكد إنه موجود جنبك)
$csvFile = "day5_final_schedule.csv";

if (!file_exists($csvFile)) {
    die("❌ الملف $csvFile مش موجود! اتأكد إنك نسخته للفولدر.");
}

// فتح الملف
if (($handle = fopen($csvFile, "r")) !== FALSE) {
    
    // تخطي أول سطر (العناوين)
    fgetcsv($handle); 

    echo "<h3>⏳ جاري رفع البيانات لقاعدة البيانات...</h3>";

    // تفريغ الجدول القديم عشان ميكررش البيانات
    $conn->query("TRUNCATE TABLE final_exam_schedule");

    // قراءة البيانات سطر سطر
    $count = 0;
    $stmt = $conn->prepare("INSERT INTO final_exam_schedule (course_id, slot_number, exam_day, exam_period, total_students, conflicts_count) VALUES (?, ?, ?, ?, ?, ?)");

    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        // البيانات جاية من CSV: [course_id, slot_number]
        // هنحسب اليوم والفترة بعملية حسابية بسيطة هنا
        $c_id = $data[0];
        $slot = $data[1];
        
        // افتراض: 3 فترات في اليوم
        $day = floor($slot / 3) + 1;
        $period = ($slot % 3) + 1;
        
        // قيم افتراضية للإحصائيات (لأن الـ CSV القديم مفهوش العدد)
        $students = 0; 
        $conflicts = 0;

        $stmt->bind_param("iiiiii", $c_id, $slot, $day, $period, $students, $conflicts);
        $stmt->execute();
        $count++;
    }
    
    fclose($handle);
    $stmt->close();

    echo "<h2 style='color:green;'>✅ مبروك! تم رفع $count امتحان لقاعدة البيانات بنجاح.</h2>";
    echo "<a href='index.php'>اضغط هنا عشان تشوف الجدول</a>";

} else {
    echo "مش قادر أفتح الملف.";
}

$conn->close();
?>