import pandas as pd
import datetime as dt
data_path = "2025 Tithe Data.csv"
df = pd.read_csv(data_path)
df_by_name = df.groupby(df["Name"])["Amount"].sum()
print(df_by_name)
df_by_name.to_csv("Tithe 2025 By Name.csv")