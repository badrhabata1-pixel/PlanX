import pandas as pd
from models import Room
from ingestion.validators import validate_required_columns

def parse_rooms(df):
    # --- الذكاء الاصطناعي لترجمة الأعمدة (Smart Column Mapping) ---
    
    # تحويل الحروف كلها لـ small عشان نتفادى أخطاء الكتابة
    df.columns = [str(col).strip().lower() for col in df.columns]

    # لو الملف فيه أعمدة id و size هنترجمها للأسماء اللي المحرك متوقعها
    if 'id' in df.columns and 'size' in df.columns:
        df = df.rename(columns={'id': 'room_code', 'size': 'capacity'})
        
    # إضافة الأعمدة الناقصة بقيم افتراضية عشان المحرك يكمل شغل
    if 'room_name' not in df.columns and 'room_code' in df.columns:
        df['room_name'] = "Room " + df['room_code'].astype(str)
        
    if 'room_type' not in df.columns:
        df['room_type'] = "Standard"

    # التحقق من أن الأعمدة المطلوبة أصبحت موجودة
    REQUIRED_COLUMNS =['room_name', 'room_code', 'capacity', 'room_type']
    validate_required_columns(df, REQUIRED_COLUMNS, "rooms_capacities.csv")

    rooms =[]
    for _, row in df.iterrows():
        room = Room(
            room_name=str(row['room_name']).strip(),
            room_code=str(row['room_code']).strip(),
            capacity=int(row['capacity']),
            room_type=str(row['room_type']).strip()
        )
        rooms.append(room)
        
    return rooms