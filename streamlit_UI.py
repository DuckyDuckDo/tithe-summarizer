import streamlit as st
import pandas as pd

st.set_page_config(page_title = "VGOMNE 2025 Tithe Summary")

st.title("VGOMNE 2025 Tithe Dashboard")


@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates = ["Date"])
    df["Year"] =  df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week
    return df

uploaded_file = st.file_uploader("Upload your cleaned tithing contributions CSV file here", type = ["csv"])

# If file upload was successful, parse the file 
if uploaded_file:
    df = load_data(uploaded_file)
    st.header("Overview")
    st.metric("Total Contributions in 2025", f"${df["Amount"].sum():,.2f}")

    # Four Tabs for the Dashboard
    tab1, tab2, tab3, tab4 = st.tabs(
        ["By Person", "By Method", "By Time", "All Transactions"]
    )

    with tab1:
        st.subheader("Contributions by Person")
        selected_year = int(st.selectbox("Select Year", sorted(df["Year"].unique())))
        person_summary = (
            df[df["Year"] == selected_year]
            .groupby("Name")["Amount"].sum().reset_index()
        )
        st.dataframe(person_summary)

    with tab2:
        st.subheader("Contributions by Method")
        method_summary = (
            df.groupby(["Year", "Method"])["Amount"]
            .sum()
            .reset_index()
            .pivot(index = "Year", columns = "Method", values = "Amount")
            .fillna(0)
        )
        st.dataframe(method_summary)
    
    with tab3:
        st.subheader("Contributions by Time")
        time_view = st.radio("View by:", ["Monthly", "Weekly"], horizontal = True)
        if time_view == "Monthly":
            monthly = df.groupby(["Year", "Month"])["Amount"].sum().reset_index()
            st.dataframe(monthly)
        else:
            weekly = df.groupby(["Date"])["Amount"].sum().reset_index()
            st.dataframe(weekly)
    
    with tab4:
        st.subheader("All Transactions")
        st.dataframe(df)