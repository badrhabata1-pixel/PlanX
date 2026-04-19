from pathlib import Path

# المسار الأساسي لفولدر المحرك
BASE_DIR = Path(__file__).resolve().parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"

# هنا وحدنا الأسماء (شيلنا التواريخ) عشان الـ PHP يبعت الملفات بالأسماء دي والمحرك يلقطها فوراً
ROSTER_FILE = DATA_RAW_DIR / "student_roster.xls" 
ROOMS_FILE = DATA_RAW_DIR / "rooms_capacities.csv"
PERIODS_FILE = DATA_RAW_DIR / "periods_from_rules.csv"
CALENDAR_FILE = DATA_RAW_DIR / "planx_academic_calendar.csv"
SLOTS_FILE = DATA_RAW_DIR / "planx_date_period_slots.csv"
LEVEL_POLICY_FILE = DATA_RAW_DIR / "planx_level_exam_policy.csv"
RULES_FILE = DATA_RAW_DIR / "exam_rules.csv"
ASSUMPTIONS_FILE = DATA_RAW_DIR / "planx_system_assumptions.csv"
ROOM_AVAILABILITY_FILE = DATA_RAW_DIR / "room_availability_template.csv"

# فولدر المخرجات
OUTPUTS_DIR = BASE_DIR / "output"