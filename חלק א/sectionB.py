import pandas as pd
from datetime import datetime
import numpy as np
import os
import csv



# קריאת הקובץ
df = pd.read_excel("time_series.xlsx")  # שים את שם הקובץ שלך פה

# פונקציה לבדוק אם timestamp בפורמט תקין
def is_valid_datetime(value):
    try:
        datetime.strptime(str(value), "%d/%m/%Y %H:%M")
        return True
    except (ValueError, TypeError):
        return False

# פונקציה לבדוק כפילויות
def check_duplicates(df):
    return df.duplicated(subset=["timestamp", "value"])

# פונקציה לבדוק אם value תקין
def is_valid_value(val):
    if pd.isna(val):
        return True
    try:
        float(val)  # אם אפשר להמיר למספר – תקין
        return True
    except ValueError:
        if str(val).strip().lower() in ["nan", "not_a_number"]:
            return True
    return False

def split_by_day(input_file, timestamp_column="timestamp"):
    """מפצל קובץ Excel לקבצי CSV לפי יום לפי עמודת timestamp"""
    df = pd.read_excel(input_file, engine="openpyxl")
    base_dir = os.path.dirname(os.path.abspath(input_file))
    file_list = []

    # המרה לתאריך (בלי שעה) מתוך עמודת timestamp
    df["date_only"] = pd.to_datetime(df[timestamp_column], format="%d/%m/%Y %H:%M", errors='coerce').dt.date

    # סינון שורות שאין להן תאריך תקין
    df = df.dropna(subset=["date_only"])

    # קיבוץ לפי יום
    grouped = df.groupby("date_only")

    for date, group in grouped:
        # שם קובץ לפי תאריך בפורמט YYYY-MM-DD
        date_str = date.strftime("%Y-%m-%d")
        output_file = os.path.join(base_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_{date_str}.csv")

        # שמירה לקובץ CSV
        group.drop(columns=["date_only"]).to_csv(output_file, index=False)
        file_list.append(output_file)
        print(f"נוצר קובץ: {output_file}")

    return file_list

def calculate_hourly_averages(file_list, timestamp_column="timestamp", value_column="value"):
    """
    מחשבת ממוצעים שעתיים לכל קובץ בנפרד ומחזירה מילון עם הממוצעים של כל הקבצים.
    """
    hourly_averages = {}

    for file_path in file_list:
        try:
            df = pd.read_csv(file_path)

            # המרה לתאריך
            df[timestamp_column] = pd.to_datetime(df[timestamp_column], format="%d/%m/%Y %H:%M", errors='coerce')
            df = df.dropna(subset=[timestamp_column, value_column])

            # המרה לערכים מספריים
            df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
            df = df.dropna(subset=[value_column])

            # יצירת עמודת שעה (שעה עגולה)
            df["hour"] = df[timestamp_column].dt.floor("h")

            # חישוב ממוצע לפי שעה עבור כל קובץ
            hourly_avg = df.groupby("hour")[value_column].mean().to_dict()

            # הוספת הממוצעים למילון הכללי
            hourly_averages[file_path] = hourly_avg

        except Exception as e:
            print(f"שגיאה בעיבוד הקובץ {file_path}: {e}")

    return hourly_averages

def dict_to_csv(data_dict, output_file):
    """
    מקבלת מילון וממירה אותו לקובץ CSV.
    """
    try:
        # יצירת קובץ CSV
        with open(output_file, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            # כותרות העמודות
            writer.writerow(["Key", "Value"])

            # כתיבת הנתונים
            for key, value in data_dict.items():
                writer.writerow([key, value])

        print(f"המילון נשמר לקובץ: {output_file}")
    
    except Exception as e:
        print(f"שגיאה בשמירת הקובץ: {e}")


df["is_valid_timestamp"] = df["timestamp"].apply(is_valid_datetime)
df["is_duplicate"] = check_duplicates(df)
df["is_valid_value"] = df["value"].apply(is_valid_value)

# הצגת שורות בעייתיות (אם יש)
invalid_rows = df[
    (~df["is_valid_timestamp"]) |
    (df["is_duplicate"]) |
    (~df["is_valid_value"])
]

print("שורות עם בעיות:")
print(invalid_rows)

file_list = split_by_day("time_series.xlsx")
hourly_averages = calculate_hourly_averages(file_list)
dict_to_csv(hourly_averages, "hourly_averages.csv")
print("נוצר קובץ סיכום בשם: hourly_averages.csv")
