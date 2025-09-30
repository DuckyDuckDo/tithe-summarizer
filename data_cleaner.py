import pandas as pd
import glob

def extract_and_clean_sheet(excel_file, sheet):
    """Pass a .xlsx file and have this function clean up all the data to get a final dataframe that has entries of
    Date, Name, Amount Given, Transaction Type, Check Number (if applicable)"""
    df = pd.read_excel(excel_file, sheet_name = sheet)
    date = None
    method = None
    rows = []

    for _, row in df.iterrows():
        # Detect the date
        if pd.notna(row.iloc[0]):
            try:
                maybe_date = pd.to_datetime(row.iloc[0], errors = "coerce")
                if pd.notna(maybe_date):
                    date = maybe_date
            except:
                pass
        
        # Detect the End of the Worksheet and return the dataframe
        if isinstance(row.iloc[0], str):
            txt = row.iloc[0].strip().lower()
            if "weekly subtotal" in txt:
                return pd.DataFrame(rows, columns = ["Date", "Name", "Method", "Amount", "Check #"])
        
        # Switch Method if applicable
        if isinstance(row.iloc[1], str):
            txt = row.iloc[1].strip().lower()
            if "cash" in txt:
                method = "cash"
            elif "check" in txt:
                method = "check"
            elif "zelle" in txt:
                method = "zelle"
            elif "venmo" in txt:
                method = "venmo"
        
        # Extract Data
        if isinstance(row.iloc[2], str) and (pd.notna(row.iloc[3]) or pd.notna(row.iloc[4]) or pd.notna(row.iloc[5]) or pd.notna(row.iloc[6])):
            name = row.iloc[2].strip()
            if pd.notna(row.iloc[3]):
                amount = float(pd.to_numeric(row.iloc[3], errors = "coerce"))
            elif pd.notna(row.iloc[4]):
                amount = float(pd.to_numeric(row.iloc[4], errors = "coerce"))
            elif pd.notna(row.iloc[5]):
                amount = float(pd.to_numeric(row.iloc[5], errors = "coerce"))
            elif pd.notna(row.iloc[6]):
                amount = float(pd.to_numeric(row.iloc[6], errors = "coerce"))
            
            if method == "check":
                try:
                    check_number = int(row.iloc[1])
                except:
                    check_number = None
            else:
                check_number = None

            if amount:
                rows.append([date, name, method, amount, check_number])
    return pd.DataFrame(rows, columns = ["Date", "Name", "Method", "Amount", "Check #"])

def extract_all_data(folder):
    """
    Goes through the folder containing each month's offering summaries and extracts all the data and gives one final sheet
    """
    all_data = []
    for path in glob.glob(f"{folder}/*.xlsx"):
        print(f"Extracting from {path}")
        xls = pd.ExcelFile(path)
        for sheet in xls.sheet_names:
            if sheet.startswith("Week"):
                df = extract_and_clean_sheet(path, sheet)
                all_data.append(df)

    combined = pd.concat(all_data, ignore_index = True)
    combined["Date"] = pd.to_datetime(combined["Date"], errors = "coerce")
    combined["Amount"] = pd.to_numeric(combined["Amount"], errors = "coerce").fillna(0)
    return combined

if __name__ == "__main__":
    file_folder = "monthly_data"
    df = extract_all_data(file_folder)
    df = df.sort_values(by = "Date")
    df.to_csv("2025 Tithe Data.csv", index = False)
    print("All Tithing Data Saved")

