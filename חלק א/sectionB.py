import pandas as pd
import os

# קריאת נתונים לפי סוג קובץ
def read_data(file_path):
    if file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    elif file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".parquet"):
        return pd.read_parquet(file_path)
    else:
        raise ValueError("פורמט קובץ לא נתמך. נסה קובץ xlsx, csv או parquet.")

# בדיקות ניקוי נתונים
def validate_data(df):
    # בדיקה לעמודות נדרשות
    if 'Timestamp' not in df.columns or 'value' not in df.columns:
        raise ValueError("הקובץ חייב להכיל עמודות בשם 'Timestamp' ו-'value'")
    
    # המרה לפורמט תאריך
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])  # הסרת תאריכים לא תקינים
    
    # הסרת כפילויות
    df = df.drop_duplicates()

    # בדיקה נוספת – ערכים שליליים
    df = df[df['value'] >= 0]

    return df

# פיצול הקובץ לפי יום
def split_by_day(df, output_dir="daily_parts"):
    os.makedirs(output_dir, exist_ok=True)
    df['date'] = df['Timestamp'].dt.date
    file_list = []
    for date, group in df.groupby('date'):
        file_name = os.path.join(output_dir, f"{date}.csv")
        group.to_csv(file_name, index=False)
        file_list.append(file_name)
    return file_list

# חישוב ממוצעים שעתיים עבור קובץ אחד
def compute_hourly_averages(file_path):
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['hour'] = df['Timestamp'].dt.floor('H')  
    hourly_avg = df.groupby('hour')['value'].mean().reset_index()
    hourly_avg.columns = ['Timestamp', 'Average']
    return hourly_avg


def process_all_parts(file_list, output_path="final_hourly_averages.csv"):
    all_results = pd.DataFrame()
    for file in file_list:
        part_avg = compute_hourly_averages(file)
        all_results = pd.concat([all_results, part_avg], ignore_index=True)

   
    final_result = all_results.groupby('Timestamp')['Average'].mean().reset_index()
    final_result.to_csv(output_path, index=False)
    print(f"הקובץ הסופי נשמר ב: {output_path}")


def main():
    file_path = "time_series.xlsx"  # יש לשים כאן את הנתיב לקובץ
    df = read_data(file_path)
    print("שמות העמודות בקובץ:")
    print(df.columns)
    df = validate_data(df)

    file_list = split_by_day(df)
    process_all_parts(file_list)

if __name__ == "__main__":
    main()
