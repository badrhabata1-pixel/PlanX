<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanX | Final Schedule</title>

    <!-- Fonts & Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        :root {
            --bg-core: #0f172a;
            --bg-secondary: #1e293b;
            --primary: #8b5cf6;
            --accent: #06b6d4;
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --border-light: rgba(139, 92, 246, 0.3);
            --font-en: 'Outfit', sans-serif;
            --success: #10b981;
            --danger: #ef4444;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        
        body {
            background-color: var(--bg-core);
            color: var(--text-main);
            font-family: var(--font-en);
            background-image: radial-gradient(circle at 50% 0%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
            min-height: 100vh;
        }

        /* NAVBAR */
        .navbar {
            padding: 15px 5%; display: flex; justify-content: space-between; align-items: center;
            background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid var(--border-light);
            position: sticky; top: 0; z-index: 100;
        }
        .brand { font-size: 1.5rem; font-weight: 900; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 10px; }
        .brand i { color: var(--primary); }
        .btn-nav {
            padding: 8px 20px; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 0.9rem;
            border: 1px solid var(--border-light); color: var(--text-muted); transition: 0.3s;
        }
        .btn-nav:hover { background: var(--primary); color: white; border-color: transparent; }

        /* CONTAINER */
        .container { max-width: 1200px; margin: 50px auto; padding: 0 20px; }
        
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header h1 span { color: var(--accent); }

        /* TABLE CARD */
        .table-card {
            background: #1e293b; border-radius: 20px; border: 1px solid var(--border-light);
            overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        table { width: 100%; border-collapse: collapse; }
        
        th {
            background: rgba(139, 92, 246, 0.15); color: var(--accent); padding: 20px; text-align: left;
            font-weight: 800; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;
        }
        
        td { padding: 18px 20px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text-muted); vertical-align: middle; }
        tr:last-child td { border-bottom: none; }
        tr:hover { background: rgba(255,255,255,0.02); }

        .badge { padding: 6px 15px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; display: inline-block; white-space: nowrap; }
        .day { background: rgba(6, 182, 212, 0.15); color: var(--accent); border: 1px solid rgba(6, 182, 212, 0.3); }
        .period { background: rgba(139, 92, 246, 0.15); color: var(--primary); border: 1px solid rgba(139, 92, 246, 0.3); }
        
        .status-success { background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 50px; padding: 5px 12px; font-size: 0.8rem; font-weight: bold; }
        .status-danger { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 50px; padding: 5px 12px; font-size: 0.8rem; font-weight: bold; }

        .course-name { font-weight: bold; color: #fff; font-size: 1.05rem; }
        .course-id { font-family: monospace; color: var(--text-muted); opacity: 0.6; }
        .student-count { font-weight: bold; color: #fff; display: flex; align-items: center; gap: 8px; }
        .student-count i { color: var(--text-muted); font-size: 0.9rem; }

        /* BUTTONS */
        .actions { margin-top: 30px; display: flex; justify-content: center; gap: 20px; }
        .btn-action {
            padding: 15px 35px; border-radius: 12px; font-weight: 700; text-decoration: none;
            display: inline-flex; align-items: center; gap: 10px; transition: 0.3s; border: none; cursor: pointer;
        }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 10px 30px -5px var(--primary); }
        
        .btn-secondary { background: transparent; border: 1px solid var(--accent); color: var(--accent); }
        .btn-secondary:hover { background: var(--accent); color: white; }

        /* ========================================= */
        /* ============ PRINT STYLES =============== */
        /* ========================================= */
        @media print {
            /* 1. Reset Backgrounds & Colors */
            body { 
                background: white !important; 
                background-image: none !important; 
                color: black !important; 
                margin: 0; padding: 0;
            }
            .container { 
                max-width: 100% !important; 
                margin: 0 !important; 
                padding: 10px !important; 
            }

            /* 2. Hide Non-Printable Elements */
            .navbar, .actions, .btn-action, .header p { 
                display: none !important; 
            }

            /* 3. Improve Header Visibility */
            .header h1 { 
                color: black !important; 
                font-size: 24pt !important;
                margin-top: 0;
            }
            .header h1 span { color: #333 !important; } /* Make 'Schedule' dark grey */

            /* 4. Table Styling for Paper */
            .table-card {
                background: white !important;
                border: none !important;
                box-shadow: none !important;
                border-radius: 0 !important;
            }
            
            table {
                width: 100% !important;
                border: 2px solid #000 !important;
            }

            th {
                background-color: #f0f0f0 !important; /* Light Grey Header */
                color: #000 !important;
                border: 1px solid #000 !important;
                font-weight: bold !important;
            }

            td {
                background-color: white !important;
                color: #000 !important;
                border: 1px solid #000 !important;
                padding: 10px !important;
            }
            
            tr:hover { background: none !important; }

            /* 5. Fix Text Colors inside Table */
            .course-name, .student-count, .course-id { 
                color: #000 !important; 
            }
            .student-count i { color: #000 !important; }

            /* 6. Badges (Day/Period) - Turn into Outlines */
            .badge {
                border: 1px solid #000 !important;
                background: transparent !important;
                color: #000 !important;
                box-shadow: none !important;
            }
            
            /* 7. Status Labels */
            .status-success, .status-danger {
                background: transparent !important;
                color: #000 !important;
                border: 1px solid #000 !important;
                font-weight: bold !important;
            }

            /* 8. Page Setup */
            @page {
                size: A4;
                margin: 1cm;
            }
        }
    </style>
</head>
<body>

    <!-- NAV -->
    <nav class="navbar">
        <a href="index.php" class="brand"><i class="fa-solid fa-layer-group"></i> PlanX</a>
        <a href="workspace.php" class="btn-nav"><i class="fa-solid fa-plus"></i> New Schedule</a>
    </nav>

    <!-- CONTENT -->
    <div class="container">
        
        <div class="header">
            <h1>Final <span>Examination Schedule</span></h1>
            <p style="color: var(--text-muted);">Optimization completed successfully. Check details below.</p>
        </div>

        <div class="table-card">
            <?php
            // مسار ملف النتيجة اللي المحرك بيطلعه
            $csvFile = __DIR__ . "/planx_ai_engine/final_expert_schedule.csv";

            if (!file_exists($csvFile)) {
                echo "<div style='padding:50px; text-align:center;'>
                        <i class='fa-solid fa-triangle-exclamation' style='font-size:3rem; color:var(--danger);'></i>
                        <p style='margin-top:15px;'>No schedule file found. Please run the AI Engine first.</p>
                      </div>";
            } else {
                $file = fopen($csvFile, "r");
                $headers = fgetcsv($file); // قراءة السطر الأول (العناوين)

                echo "<table>";
                echo "<thead><tr>
                        <th width='20%'>Date & Time</th>
                        <th width='12%'>Code</th>
                        <th>Course Title</th>
                        <th width='10%'>Students</th>
                        <th width='20%'>Rooms Assigned</th>
                        <th width='10%'>Status</th>
                      </tr></thead>";
                echo "<tbody>";

                // قراءة البيانات صف بصف من الملف
                while (($row = fgetcsv($file)) !== FALSE) {
                    // ترتيب الأعمدة في ملف المحرك الجديد غالباً:
                    // 0: exam_id, 1: period_id, 2: time_slot (D...S...), 3: students, 4: rooms, 5: rooms_count, 6: rooms_capacity_sum
                    
                    $eid       = $row[0];
                    $time_info = $row[2]; // الوقت (اليوم والفترة)
                    $students  = $row[3];
                    $rooms     = $row[4];
                    $cap_sum   = $row[6];

                    // تجميل شكل الوقت (اختياري)
                    $display_time = str_replace('_', ' | ', $time_info);

                    echo "<tr>";
                    
                    // Date & Time
                    echo "<td>
                            <div style='display:flex; flex-direction:column; gap:5px;'>
                                <span class='badge day' style='font-size:0.7rem;'>$display_time</span>
                            </div>
                          </td>";
                    
                    echo "<td class='course-id'>#$eid</td>";
                    echo "<td class='course-name'>Course Optimization $eid</td>"; // الاسم بيتحسن بربطه بجدول المواد لو تحب
                    
                    echo "<td>
                            <span class='student-count'>
                                <i class='fa-solid fa-users'></i> $students
                            </span>
                          </td>";

                    // عرض القاعات (ميزة المحرك الجديد)
                    echo "<td>
                            <span style='color:var(--accent); font-size:0.85rem;'>
                                <i class='fa-solid fa-door-open'></i> Rooms: $rooms
                            </span>
                          </td>";
                    
                    echo "<td><span class='status-success'><i class='fa-solid fa-check'></i> Optimized</span></td>";
                    echo "</tr>";
                }
                echo "</tbody></table>";
                fclose($file);
            }
            ?>
        </div>
        <div class="actions">
            <button onclick="window.print()" class="btn-action btn-primary">
                <i class="fa-solid fa-print"></i> Print / Save PDF
            </button>
            <a href="workspace.php" class="btn-action btn-secondary">
                <i class="fa-solid fa-rotate-right"></i> Generate New
            </a>
        </div>

    </div>

</body>
</html>