<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanX | Processing...</title>
    
    <!-- Fonts & Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        /* CORE VARIABLES */
        :root {
            --bg-core: #0f172a;
            --bg-card: #1e293b;
            --primary: #8b5cf6;
            --accent: #06b6d4;
            --text-main: #f8fafc;
            --success: #10b981;
            --error: #ef4444;
            --font-en: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg-core);
            color: var(--text-main);
            font-family: var(--font-en);
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

       .console-card {
    width: 100%;
    max-width: 800px;
    background: var(--bg-card);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 15px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    margin-bottom: 50px; /* إضافة مساحة تحت */
}

        .console-header {
            background: #0f172a;
            padding: 15px 25px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .red { background: #ef4444; }
        .yellow { background: #f59e0b; }
        .green { background: #10b981; }

        .console-body {
            padding: 25px;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            height: 400px; /* Fixed height with scroll */
            overflow-y: auto;
            color: #ccc;
        }

        .log-line { margin-bottom: 10px; padding-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .log-success { color: var(--success); font-weight: bold; }
        .log-error { color: var(--error); font-weight: bold; }
        .log-info { color: var(--accent); }

        /* ACTION BAR (The Button Area) */
        .action-bar {
            padding: 30px;
            text-align: center;
            background: rgba(139, 92, 246, 0.1);
            border-top: 1px solid rgba(139, 92, 246, 0.3);
            display: none; /* Hidden by default */
            animation: slideUp 0.5s ease-out;
        }

        .btn-result {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.2rem;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: 0.3s;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
        }
        .btn-result:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 0 40px rgba(6, 182, 212, 0.6);
        }

        /* Loader */
        .loader-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; }
        .ai-pulse { 
            width: 80px; height: 80px; background: rgba(139, 92, 246, 0.2); 
            border: 3px solid var(--primary); border-radius: 50%; position: relative; 
            animation: pulse 2s infinite; 
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(139, 92, 246, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
        }
        .loading-text { margin-top: 20px; font-weight: bold; color: var(--accent); animation: blink 1.5s infinite; }
        @keyframes blink { 50% { opacity: 0.5; } }
        
        #successCard { display: none; text-align: center; padding: 20px; }
        .file-tag { display: inline-block; padding: 5px 12px; background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 8px; font-size: 0.8rem; margin: 4px; color: #10b981; }
        .path-box { background: #000; padding: 15px; border-radius: 12px; font-family: monospace; font-size: 0.85rem; color: var(--accent); border-left: 4px solid var(--accent); margin: 20px 0; word-break: break-all; text-align: left; }

        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <div class="console-card">
        <div class="console-header">
            <div class="dot red"></div>
            <div class="dot yellow"></div>
            <div class="dot green"></div>
            <span style="margin-left: 10px; font-weight: bold; font-size: 0.9rem;">PlanX Processor</span>
        </div>

       <div class="console-body" id="consoleOutput" style="background: #111827; position: relative; display: block; overflow-y: auto;">
    
            <!-- 1. شاشة اللودينج -->
            <div id="loadingUI" style="text-align: center; z-index: 10;">
                <div id="liveStatus" style="color: #4af626; font-family: monospace; font-size: 0.8rem; margin-top: 15px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px; max-height: 100px; overflow-y: auto; text-align: left; width: 300px; margin-left: auto; margin-right: auto;">
                    ➜ Waiting for Engine response...
                </div>

                <style>
                    .ai-pulse-ring { 
                        width: 100px; height: 100px; background: rgba(139, 92, 246, 0.1); 
                        border: 2px solid var(--primary); border-radius: 50%; margin: 0 auto; 
                        position: relative; animation: pulse-ring 2s infinite; 
                    }
                    .ai-pulse-ring::after { 
                        content: ''; position: absolute; width: 50px; height: 50px; 
                        top: 23px; left: 23px; background: var(--accent); border-radius: 50%; 
                        box-shadow: 0 0 30px var(--accent); animation: core-glow 2s infinite;
                    }
                    @keyframes pulse-ring { 0% { transform: scale(0.8); opacity: 0.5; } 50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 40px var(--primary); } 100% { transform: scale(0.8); opacity: 0.5; } }
                    @keyframes core-glow { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
                </style>
                
                <div class="ai-pulse-ring"></div>
                <h3 style="margin-top: 25px; color: #fff; font-family: 'Outfit'; letter-spacing: 1px;">AI Engine Calculating...</h3>
                <p style="color: #64748b; font-size: 0.85rem;">Optimizing exams within student constraints</p>
            </div>

            <!-- 2. كارت تفاصيل النجاح -->
            <div id="successDetails" style="display: none; width: 100%; text-align: center; padding: 10px; font-family: 'Outfit'; animation: fadeIn 0.8s;">
                <div style="margin-bottom: 25px;">
                    <i class="fa-solid fa-circle-check" style="color: #10b981; font-size: 4.5rem; text-shadow: 0 0 20px rgba(16, 185, 129, 0.4);"></i>
                    <h2 style="color: #fff; margin-top: 15px; font-size: 2.2rem;">Sequence Stabilized!</h2>
                    <p style="color: #94a3b8; margin-top: 5px;">AI Engine has successfully generated the optimized schedule.</p>
                </div>
                
                <div style="text-align: left; margin-bottom: 20px;">
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 10px;"><i class="fa-solid fa-cloud-check"></i> Ingested Streams:</p>
                    <div id="displayUploadedFiles"></div>
                </div>
            </div>

            <?php
            // --- المنطق البرمجي ---
            $db_host = "localhost:3307"; $db_user = "root"; $db_pass = ""; $db_name = "exam_system_db";
            $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
            $python_path = "C:/Users/badr habata/AppData/Local/Programs/Python/Python313/python.exe";
            $engine_folder = __DIR__ . "/planx_ai_engine";
            $uploadDir = $engine_folder . '/data/raw/';
            $uploadedFileList = [];

            if ($_SERVER['REQUEST_METHOD'] == 'POST') {
                
                // 1. تنظيف الفولدر قبل الرفع
                if (is_dir($uploadDir)) {
                    $files = glob($uploadDir . '*');
                    foreach ($files as $file) { if (is_file($file)) unlink($file); }
                } else {
                    mkdir($uploadDir, 0777, true);
                }

                // 2. معالجة الرفع الذكي (Smart Ingestion - Content Based)
                $uploadedSuccessfully = false;
                if (isset($_FILES['engine_files'])) {
                    foreach ($_FILES['engine_files']['name'] as $i => $name) {
                        if ($_FILES['engine_files']['error'][$i] == 0) {
                            $tmp_name = $_FILES['engine_files']['tmp_name'][$i];
                            $lower_name = strtolower($name);
                            
                            $target_name = $name; // الاسم الافتراضي

                            // التعرف على ملف الطلاب من الامتداد
                           // التعرف على ملف الطلاب من الامتداد والحفاظ عليه
if (strpos($lower_name, '.xlsx') !== false) {
    $target_name = "student_roster.xlsx";
} elseif (strpos($lower_name, '.xls') !== false) {
    $target_name = "student_roster.xls";
} else {
                                // قراءة أول 1000 حرف من الملف للتعرف على محتواه
                                $file_content = strtolower(file_get_contents($tmp_name, false, null, 0, 1000));
                                
                                // المطابقة الذكية بناءً على العناوين
                                if (strpos($file_content, 'source_or_reason') !== false) {
                                    $target_name = "planx_system_assumptions.csv";
                                } elseif (strpos($file_content, 'is_available') !== false) {
                                    $target_name = "room_availability_template.csv";
                                } elseif (strpos($file_content, 'coordinates') !== false || strpos($file_content, 'size,alt') !== false) {
                                    $target_name = "rooms_capacities.csv";
                                } elseif (strpos($file_content, 'constraint_type') !== false) {
                                    $target_name = "exam_rules.csv";
                                } elseif (strpos($file_content, 'penalty') !== false && strpos($file_content, 'time') !== false) {
                                    $target_name = "periods_from_rules.csv";
                                } elseif (strpos($file_content, 'is_holiday') !== false) {
                                    $target_name = "planx_academic_calendar.csv";
                                } elseif (strpos($file_content, 'is_schedulable_by_default') !== false) {
                                    $target_name = "planx_date_period_slots.csv";
                                } elseif (strpos($file_content, 'min_gap_days_between_exams') !== false) {
                                    $target_name = "planx_level_exam_policy.csv";
                                } elseif (strpos($file_content, 'student_id') !== false && strpos($file_content, 'exam_id') !== false) {
                                    $target_name = "student_roster.xls";
                                }
                            }

                            // نقل الملف وتسجيله (هذا هو السطر الذي كان به المشكلة وتم إصلاحه)
                            if (move_uploaded_file($tmp_name, $uploadDir . $target_name)) {
                                $uploadedFileList[] = $name;
                                if ($target_name == "student_roster.xls") {
                                    $uploadedSuccessfully = true;
                                }
                            }
                        }
                    }
                }

                // 3. تشغيل المحرك
                if ($uploadedSuccessfully) {
                    chdir($engine_folder);
                    $command = "set PYTHONIOENCODING=utf-8 && \"$python_path\" \"main.py\" 2>&1";
                    
                    $handle = popen($command, 'r');
                    $full_output = "";
                    while (!feof($handle)) {
                        $line = fgets($handle);
                        if ($line) {
                            $full_output .= $line;
                            echo "<script>
                                var statusBox = document.getElementById('liveStatus');
                                if(statusBox) statusBox.innerHTML += '" . addslashes(trim($line)) . "<br>';
                                statusBox.scrollTop = statusBox.scrollHeight;
                            </script>";
                            if(ob_get_level() > 0) ob_flush();
                            flush();
                        }
                    }
                    pclose($handle);

                    // 4. فحص النجاح النهائي
                    if (strpos($full_output, "exported successfully") !== false) {
                        $finalFile = "";
                        if (preg_match('/GENERATED_FILENAME:(.*)/', $full_output, $matches)) { $finalFile = trim($matches[1]); }
                        
                        $localMsg = "Default Storage (Engine Folder)";
                        if (!empty($_POST['local_destination'])) {
                            $userP = $_POST['local_destination'];
                            if (is_dir($userP)) {
                                $dest = rtrim($userP, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . $finalFile;
                                if (copy($engine_folder . DIRECTORY_SEPARATOR . $finalFile, $dest)) $localMsg = $dest;
                            }
                        }
echo "<script>
                            // 1. إخفاء اللودينج وإظهار النجاح
                            document.getElementById('loadingUI').style.display = 'none';
                            var successDiv = document.getElementById('successDetails');
                            successDiv.style.display = 'block';

                            // 2. تجهيز البيانات
                            var finalFileName = '" . $finalFile . "';
                            if (!finalFileName) finalFileName = 'Optimized_Schedule.xlsx';
                            var downloadLink = 'planx_ai_engine/' + finalFileName;

                            // 3. عرض الملفات
                            const fileNames = " . json_encode($uploadedFileList, JSON_UNESCAPED_UNICODE) . ";
                            var displayBox = document.getElementById('displayUploadedFiles');
                            if(displayBox) {
                                displayBox.innerHTML = ''; 
                                fileNames.forEach(f => { 
                                    displayBox.innerHTML += `<span class='file-tag'><i class='fa-solid fa-check'></i> \${f}</span>`; 
                                });
                            }

                            // 4. إضافة الزرار الشيك في الآخر تحت الملفات
                            var finalActionHtml = `
                                <div style='margin-top: 40px; padding: 25px; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;'>
                                    <a href='\${downloadLink}' download='\${finalFileName}' class='btn-result' style='text-decoration: none;'>
                                        <i class='fa-solid fa-file-excel'></i> تحميل الجدول النهائي (Excel)
                                    </a>
                                    <p style='color: #64748b; font-size: 0.85rem; margin-top: 15px;'>تمت المعالجة بنجاح بواسطة PlanX AI</p>
                                </div>
                            `;
                            successDiv.insertAdjacentHTML('beforeend', finalActionHtml);

                            // 5. سكرول لأسفل عشان تشوف الزرار
                            var consoleBody = document.getElementById('consoleOutput');
                            consoleBody.style.overflowY = 'auto';
                            setTimeout(() => {
                                consoleBody.scrollTo({ top: consoleBody.scrollHeight, behavior: 'smooth' });
                            }, 500);
                        </script>";
                        // الكود الجديد انتهى هنا

                    } else {
                        echo "<script>
                            document.getElementById('loadingUI').style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
                            document.getElementById('liveStatus').style.color = '#ef4444';
                            document.querySelector('.loading-text').innerText = 'Engine Halted (Logic Error)';
                        </script>";
                    }
                } else {
                    echo "<script>
                        document.getElementById('loadingUI').style.display = 'none';
                        alert('Error: Student Roster file (.xls) is missing or was not identified properly!');
                    </script>";
                }
            }
            if(isset($conn)) $conn->close();
            ?>
        </div>

        <!-- THIS IS THE BUTTON AREA -->
        <div class="action-bar" id="actionBar">
            <h3 style="color: #fff; margin-bottom: 20px;">🎉 Schedule Generation Complete!</h3>
            <a href="#" class="btn-result">
                <i class="fa-solid fa-file-excel"></i> 
                Download Optimized Excel
            </a>
            <p style="margin-top: 15px; font-size: 0.8rem; color: #64748b;">The AI has successfully balanced your dataset.</p>
        </div>
    </div>

    <script>
        window.addEventListener('DOMContentLoaded', (event) => {
            const loadingUI = document.getElementById('loadingUI');
            const successDetails = document.getElementById('successDetails');
            const actionBar = document.getElementById('actionBar');

            // Set up download button properly if finalFile is found
            const downloadBtn = document.querySelector('.btn-result');
            const fileName = "<?php echo isset($finalFile) ? $finalFile : ''; ?>";
            if (downloadBtn && fileName !== "") {
                downloadBtn.href = "planx_ai_engine/" + fileName;
                downloadBtn.setAttribute("download", fileName);
            }
        });
    </script>
</body>
</html>