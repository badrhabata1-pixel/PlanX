<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanX | Workspace</title>

    <!-- Google Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        /* CORE VARIABLES (Purple & Cyan Theme) */
        :root {
            --bg-core: #0f172a;
            --bg-secondary: #1e293b;
            --bg-glass: rgba(15, 23, 42, 0.85);
            --bg-card: rgba(30, 41, 59, 0.6);
            --primary: #8b5cf6;
            --primary-glow: rgba(139, 92, 246, 0.5);
            --primary-dark: #7c3aed;
            --accent: #06b6d4;
            --accent-glow: rgba(6, 182, 212, 0.5);
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --border-light: rgba(139, 92, 246, 0.3);
            --font-en: 'Outfit', sans-serif;
            --font-ar: 'Tajawal', sans-serif;
            --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; outline: none; }
        
        body {
            background-color: var(--bg-core);
            color: var(--text-main);
            font-family: var(--font-en);
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.05) 0%, transparent 40%);
        }

        /* Particles Background */
        .particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
        .particle { position: absolute; background: rgba(255, 255, 255, 0.1); border-radius: 50%; animation: float linear infinite; }
        @keyframes float { 0% { transform: translateY(0); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(-100vh); opacity: 0; } }

        /* NAVBAR */
        .navbar {
            padding: 15px 5%; display: flex; justify-content: space-between; align-items: center;
            background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-light); position: sticky; top: 0; z-index: 100;
        }
        
        .brand { 
            font-size: 1.5rem; font-weight: 900; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 10px; 
            transition: var(--transition);
        }
        .brand:hover { transform: scale(1.05); }
        .brand i { color: var(--primary); text-shadow: 0 0 10px var(--primary-glow); }

        /* NAV CONTROLS (Right Side Group) */
        .nav-controls {
            display: flex;
            align-items: center;
            gap: 25px;
        }

        /* BACK BUTTON STYLE */
        .nav-back {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: inherit;
        }

        .nav-back:hover {
            color: var(--accent);
            text-shadow: 0 0 10px var(--accent-glow);
            transform: translateX(-3px); /* حركة خفيفة لليسار */
        }
        
        /* LANGUAGE TOGGLE BUTTON */
        .lang-toggle {
            background: rgba(139, 92, 246, 0.1); 
            border: 1px solid var(--primary); 
            color: var(--primary);
            padding: 8px 20px; 
            border-radius: 50px; 
            cursor: pointer; 
            font-weight: 700;
            font-family: inherit;
            transition: var(--transition); 
            display: flex; gap: 8px; align-items: center;
        }
        .lang-toggle:hover { 
            background: var(--primary); 
            color: #fff; 
            box-shadow: 0 0 15px var(--primary-glow); 
        }

        /* WORKSPACE CONTAINER */
        .workspace-container {
            max-width: 1200px; margin: 50px auto; padding: 0 20px;
        }

        .page-header { text-align: center; margin-bottom: 50px; animation: fadeUp 0.8s ease-out; }
        .page-header h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 10px; }
        .page-header h1 span { background: linear-gradient(to right, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .page-header p { color: var(--text-muted); font-size: 1.1rem; }

        /* CARDS */
        .glass-card {
            background: var(--bg-card); backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.05); border-radius: 20px;
            padding: 30px; margin-bottom: 30px; position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: fadeUp 1s ease-out backwards;
        }
        
        .card-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; color: var(--text-main); }
        .card-title i { color: var(--accent); }
        .card-title::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.1); margin-left: 20px; }

        /* FORM ELEMENTS */
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 8px; color: var(--text-muted); font-size: 0.9rem; font-weight: 500; }
        
        .form-control {
            width: 100%; padding: 12px 15px; background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 10px;
            color: #fff; font-family: inherit; font-size: 1rem;
            transition: var(--transition);
        }
        .form-control:focus {
            border-color: var(--primary); box-shadow: 0 0 15px var(--primary-glow);
        }

        /* FILE UPLOAD STYLING */
        .file-upload-box {
            position: relative; height: 120px; border: 2px dashed rgba(255,255,255,0.1);
            border-radius: 15px; display: flex; flex-direction: column;
            align-items: center; justify-content: center; text-align: center;
            transition: var(--transition); cursor: pointer; background: rgba(0,0,0,0.2);
        }
        
        .file-upload-box:hover { border-color: var(--accent); background: rgba(6, 182, 212, 0.05); }
        
        .file-upload-box input[type="file"] {
            position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer;
        }
        
        .icon-upload { font-size: 1.8rem; color: var(--text-muted); margin-bottom: 10px; transition: var(--transition); }
        .file-upload-box:hover .icon-upload { color: var(--accent); transform: scale(1.1); }
        
        .file-name { font-size: 0.85rem; color: var(--text-muted); margin-top: 5px; }
        .file-uploaded .icon-upload { color: #10b981; } /* Green on success */
        .file-uploaded { border-color: #10b981; border-style: solid; }

        /* ACTION BUTTON */
        .action-area { text-align: center; margin-top: 40px; }
        
        .btn-glow {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white; border: none; padding: 18px 60px; font-size: 1.2rem;
            font-weight: 700; border-radius: 50px; cursor: pointer;
            box-shadow: 0 0 20px var(--primary-glow); transition: var(--transition);
            display: inline-flex; align-items: center; gap: 12px; font-family: inherit;
        }
        
        .btn-glow:hover { transform: translateY(-5px) scale(1.05); box-shadow: 0 0 40px var(--primary-glow); }
        .btn-glow i { transition: 0.3s; }
        .btn-glow:hover i { transform: rotate(90deg); }

        /* ALERTS */
        .alert { padding: 15px; border-radius: 10px; margin-bottom: 20px; font-size: 0.95rem; display: flex; align-items: center; gap: 10px; }
        .alert-info { background: rgba(6, 182, 212, 0.1); border: 1px solid var(--accent); color: var(--accent); }

        /* ANIMATIONS */
        @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr; }
            .page-header h1 { font-size: 2rem; }
        }
    </style>
</head>

<body>

    <!-- BACKGROUND ANIMATION -->
    <div class="particles" id="particles"></div>

    <!-- NAVBAR -->
    <nav class="navbar">
        <!-- Logo -->
        <a href="index.php" class="brand">
            <i class="fa-solid fa-layer-group"></i> PlanX
        </a>

        <!-- Controls (Back + Lang) -->
        <div class="nav-controls">
            <!-- RESTORED BACK BUTTON -->
            <a href="index.php" class="nav-back" data-en="Back to Home" data-ar="العودة للرئيسية">
                <i class="fa-solid fa-arrow-left"></i> 
                <span>Back to Home</span>
            </a>

            <!-- LANG BUTTON -->
            <button class="lang-toggle" id="langBtn">
                <i class="fa-solid fa-language"></i>
                <span>AR / EN</span>
            </button>
        </div>
    </nav>

    <!-- MAIN CONTAINER -->
    <div class="workspace-container">
        
        <div class="page-header">
            <h1 data-en="Initialize" data-ar="تهيئة">Initialize <span data-en="Scheduling Protocol" data-ar="بروتوكول الجدولة">Scheduling Protocol</span></h1>
            <p data-en="Configure parameters and ingest data streams for AI processing." 
               data-ar="قم بضبط المعاملات وإدخال البيانات للمعالجة بالذكاء الاصطناعي.">
               Configure parameters and ingest data streams for AI processing.
            </p>
        </div>

        <!-- FORM START -->
        <form action="process.php" method="POST" enctype="multipart/form-data" id="scheduleForm">

            <!-- 1. CONFIGURATION CARD -->
           

            <!-- 2. DATA INGESTION CARD -->
           
               <!-- استبدل عنوان الكارت بهذا الجزء بالكامل لإضافة زرار الحذف بجانبه -->
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
    <div class="card-title" style="margin-bottom: 0; flex: 1;">
        <i class="fa-solid fa-database"></i> <span data-en="Data Ingestion (CSV)" data-ar="إدخال البيانات (CSV)">Data Ingestion (CSV)</span>
    </div>
    
    <!-- زرار مسح المجلد -->
    <button type="button" onclick="wipeRawData()" style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #ef4444; padding: 8px 18px; border-radius: 10px; cursor: pointer; font-family: inherit; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; transition: 0.3s;">
        <i class="fa-solid fa-trash-can"></i>
        <span data-en="Clear Raw Folder" data-ar="تفريغ المجلد">Clear Raw Folder</span>
    </button>
</div>
                
              
        
        <div class="input-group">
    <label data-en="Upload All Data Streams" data-ar="رفع جميع ملفات البيانات">
        Upload All Data Streams (XLS & CSV)
    </label>
    <div class="file-upload-box" style="height: auto; padding: 30px;">
        <input type="file" name="engine_files[]" accept=".csv, .xls, .xlsx" multiple required onchange="updateFileName(this)">
        
        <i class="fa-solid fa-cloud-arrow-up icon-upload" style="font-size: 3rem; color: var(--primary); margin-bottom: 15px;"></i>
        
        <span class="file-text" data-en="Select all 9 files and drop them here" data-ar="حدد الـ 9 ملفات معاً واسحبهم هنا" style="font-weight: bold; display: block;">
            Select all 9 files and drop them here
        </span>

        <!-- القائمة التوضيحية (المطلوبة في الصورة) -->
        <div id="fileHintList" style="margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-excel" style="color: #10b981;"></i> Student Roster (XLS)</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Rooms Capacities</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Exam Rules</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Academic Calendar</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Periods Rules</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Date-Period Slots</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Level Exam Policy</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> System Assumptions</div>
            <div style="font-size: 0.75rem; color: #94a3b8;"><i class="fa-solid fa-file-csv"></i> Room Availability</div>
        </div>

        <div class="file-name" id="fileCounter" style="margin-top: 15px; font-weight: 800; color: var(--accent);">
            No files selected
        </div>
    </div>

        </div>
    

 
   



           

            <!-- ACTION BUTTON -->
            <div class="action-area" style="animation-delay: 0.3s;">
                <button type="submit" class="btn-glow">
                    <i class="fa-solid fa-microchip"></i>
                    <span data-en="Initiate Sequence" data-ar="بدء المعالجة">Initiate Sequence</span>
                </button>
                <p style="margin-top: 15px; font-size: 0.9rem; color: var(--text-light);">
                    <span data-en="*Processing may take up to 60 seconds depending on dataset size." 
                          data-ar="*قد تستغرق المعالجة ما يصل إلى 60 ثانية حسب حجم البيانات.">
                          *Processing may take up to 60 seconds depending on dataset size.
                    </span>
                </p>
            </div>

        </form>
    </div>

    <!-- JS FOR PARTICLES & INTERACTION -->
    <script>
        // 1. Language Toggle Logic
        const langBtn = document.getElementById('langBtn');
        let currentLang = 'en';

        langBtn.addEventListener('click', (e) => {
            e.preventDefault(); 
            currentLang = currentLang === 'en' ? 'ar' : 'en';
            document.documentElement.lang = currentLang;
            document.documentElement.dir = currentLang === 'en' ? 'ltr' : 'rtl';
            document.body.style.fontFamily = currentLang === 'en' ? 'var(--font-en)' : 'var(--font-ar)';
            
            // Translate all elements
            document.querySelectorAll('[data-en]').forEach(el => {
                if(el.getAttribute(`data-${currentLang}`)) {
                    // Special handling for the Back button to keep the icon
                    if(el.classList.contains('nav-back')) {
                        const iconHtml = el.querySelector('i').outerHTML;
                        el.innerHTML = iconHtml + ' ' + el.getAttribute(`data-${currentLang}`);
                        // Flip arrow for RTL
                        el.querySelector('i').style.transform = currentLang === 'ar' ? 'rotate(180deg)' : 'rotate(0deg)';
                    } else {
                        el.textContent = el.getAttribute(`data-${currentLang}`);
                    }
                }
            });
            
            // Update Lang Button Text
            const langText = langBtn.querySelector('span');
            langText.textContent = currentLang === 'en' ? 'AR / EN' : 'EN / AR';
        });

        // 2. File Upload Interaction
        function updateFileName(input) {
    const box = input.parentElement;
    const nameDisplay = document.getElementById('fileCounter');
    const icon = box.querySelector('.icon-upload');
    
    if (input.files && input.files.length > 0) {
        // يعرض للمستخدم عدد الملفات اللي اختارها
        nameDisplay.textContent = input.files.length + " files selected for processing";
        nameDisplay.style.color = "#10b981"; // أخضر للنجاح
        
        box.classList.add('file-uploaded');
        icon.className = "fa-solid fa-circle-check icon-upload"; // يغير الأيقونة لعلامة صح
    } else {
        nameDisplay.textContent = "No files selected";
        nameDisplay.style.color = "var(--text-muted)";
    }
}

        // 3. Particle Effect
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 20;
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                const size = Math.random() * 2 + 1;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${Math.random() * 100}%`;
                const duration = Math.random() * 20 + 10;
                particle.style.animationDuration = `${duration}s`;
                particle.style.animationDelay = `${Math.random() * 5}s`;
                
                const colors = ['rgba(139, 92, 246, 0.3)', 'rgba(6, 182, 212, 0.3)'];
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                
                particlesContainer.appendChild(particle);
            }
        }
        window.addEventListener('DOMContentLoaded', createParticles);
        // وظيفة إرسال أمر الحذف للسيرفر
function wipeRawData() {
    if(confirm("Are you sure? This will permanently delete all files in the raw data folder.")) {
        fetch('wipe_logic.php')
        .then(response => response.text())
        .then(data => {
            alert(data);
            // إعادة تصفير الواجهة
            document.getElementById('fileCounter').textContent = "No files selected";
            document.getElementById('fileCounter').style.color = "var(--text-muted)";
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Failed to reach the server.");
        });
    }
}
    </script>
</body>
</html>