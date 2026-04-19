import pandas as pd
from models import Period
from ingestion.validators import validate_required_columns
from datetime import datetime, timedelta

def parse_periods(df):
    # 1. تنظيف أسماء الأعمدة
    df.columns = [str(col).strip().lower() for col in df.columns]

    # --- معالجة أسماء الأعمدة ---
    if 'id' in df.columns and 'period_id' not in df.columns:
        df = df.rename(columns={'id': 'period_id'})
    if 'time' in df.columns and 'start_time' not in df.columns:
        df = df.rename(columns={'time': 'start_time'})

    # 2. حساب end_time لو مش موجود
    if 'end_time' not in df.columns:
        if 'length' in df.columns:
            def calculate_end(row):
                try:
                    start_str = str(row['start_time'])
                    if " " in start_str: start_str = start_str.split(" ")[1]
                    start_dt = datetime.strptime(start_str, '%H:%M:%S') if len(start_str.split(':')) == 3 else datetime.strptime(start_str, '%H:%M')
                    duration = int(row['length'])
                    end_dt = start_dt + timedelta(minutes=duration)
                    return end_dt.strftime('%H:%M')
                except: return "N/A"
            df['end_time'] = df.apply(calculate_end, axis=1)
        else:
            df['end_time'] = "Not Specified"

    # --- التعديل السحري لحل مشكلة الـ P1 ---
    # بنحول الـ ID لـ string ونضيف له حرف P لو هو رقم بس، عشان يطابق ملف المتاحية
    def normalize_id(p_id):
        p_id_str = str(p_id).strip().upper()
        # لو المعرف رقم بس (زي 1)، هنخليه P1
        if p_id_str.isdigit():
            return f"P{p_id_str}"
        return p_id_str

    df['period_id'] = df['period_id'].apply(normalize_id)

    # 3. التحقق النهائي
    REQUIRED_COLUMNS = ['period_id', 'start_time', 'end_time']
    validate_required_columns(df, REQUIRED_COLUMNS, "periods_from_rules.csv")

    periods = []
    for _, row in df.iterrows():
        try:
            period = Period(
                period_id=str(row['period_id']), # نحفظه كـ string
                start_time=str(row['start_time']).strip(),
                end_time=str(row['end_time']).strip()
            )
            periods.append(period)
        except Exception as e:
            print(f"⚠️ Skipping row: {e}")
            continue
            
    return periods