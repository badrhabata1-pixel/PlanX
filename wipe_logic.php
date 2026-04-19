<?php
// المسار الدقيق للمجلد الذي تريد تنظيفه
$targetFolder = __DIR__ . DIRECTORY_SEPARATOR . 'planx_ai_engine' . DIRECTORY_SEPARATOR . 'data' . DIRECTORY_SEPARATOR . 'raw';

if (is_dir($targetFolder)) {
    // الحصول على جميع الملفات داخل المجلد
    $files = glob($targetFolder . DIRECTORY_SEPARATOR . '*'); 
    
    $deletedCount = 0;
    foreach ($files as $file) {
        if (is_file($file)) {
            unlink($file); // حذف الملف نهائياً
            $deletedCount++;
        }
    }
    
    if ($deletedCount > 0) {
        echo "Successfully cleared $deletedCount files. Folder is now empty.";
    } else {
        echo "The folder is already clean.";
    }
} else {
    echo "Error: Directory not found at $targetFolder";
}
?>