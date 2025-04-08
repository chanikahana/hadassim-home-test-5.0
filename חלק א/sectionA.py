import pandas as pd
import os
import re  # לשימוש עם ביטויים רגולריים (Regular Expressions)

def split_excel_file(input_file, rows_per_file=100000):
    df = pd.read_excel(input_file, engine="openpyxl")  # קריאת הקובץ הראשי
    base_dir = os.path.dirname(os.path.abspath(input_file))  # מיקום שמירת הקבצים
    base_name = os.path.splitext(os.path.basename(input_file))[0]  # שם בסיסי לקובץ
    file_list = []

    total_rows = len(df)
    num_parts = (total_rows // rows_per_file) + (1 if total_rows % rows_per_file != 0 else 0)

    for i in range(num_parts):
        start_row = i * rows_per_file
        end_row = min((i + 1) * rows_per_file, total_rows)
        
        df_part = df.iloc[start_row:end_row]  # חיתוך
        output_file = os.path.join(base_dir, f"{base_name}_part{i+1}.csv")
        df_part.to_csv(output_file, index=False)  # שמירה כ־CSV
        file_list.append(output_file)
        print(f"נוצר קובץ: {output_file}")

    return file_list

def count_errors(file_list):
    """מקבלת רשימת קבצי אקסל, קוראת את העמודות ומחשבת את השגיאות"""
    error_counts = {}

    for file_path in file_list:
        try:
            df = pd.read_csv(file_path)

            # נניח שהמידע כולו בעמודה הראשונה
            for row in df.iloc[:, 0].dropna().astype(str):
                match = re.search(r"Error:\s*(\S+)", row)
                if match:
                    error_type = match.group(1)
                    error_counts[error_type] = error_counts.get(error_type, 0) + 1

            print(f"סיים לקרוא את הקובץ: {file_path}")

        except Exception as e:
            print(f"שגיאה בקריאת הקובץ {file_path}: {e}")

    return error_counts

def get_top_n_errors(error_counts, n):
    """ממיינת את המילון לפי כמות השגיאות (הערכים) ומחזירה את ה-N שגיאות הראשונות"""
    # מיון המילון לפי הערכים בצורה יורדת (הערך הגבוה ביותר קודם)
    sorted_errors = sorted(error_counts.items(), key=lambda item: item[1], reverse=True)
    
    # מחזירים את ה-N הראשון של המילון
    return dict(sorted_errors[:n])

# קריאה לפונקציה
input_file = "logs.txt.xlsx"
file_list = split_excel_file(input_file)

# קריאת השגיאות מכל הקבצים
errors_list = count_errors(file_list)

error_summary = get_top_n_errors(errors_list, 3)  # קבלת 5 השגיאות הנפוצות ביותר

# הצגת התוצאה
print("\n🔹 סיכום השגיאות מכל קבצי האקסל:")
for error, count in error_summary.items():
    print(f"{error}: {count}")
