import streamlit as st
import pandas as pd
import os

DATA_FILE = "people_data.csv"

# Load data from CSV if exists
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        # Custom sample data
        df = pd.DataFrame([
            {
                "Surname": "Kumar",
                "Title": "Mr.",
                "First_Name": "Rajesh",
                "Last_Name": "Pandey",
                "Age": 42,
                "Sex": "male"
            },
            {
                "Surname": "Sharma",
                "Title": "Ms.",
                "First_Name": "Priya",
                "Last_Name": "Sharma",
                "Age": 35,
                "Sex": "female"
            },
            {
                "Surname": "Singh",
                "Title": "Mr.",
                "First_Name": "Amit",
                "Last_Name": "Singh",
                "Age": 29,
                "Sex": "male"
            },
            {
                "Surname": "Patel",
                "Title": "Dr.",
                "First_Name": "Neha",
                "Last_Name": "Patel",
                "Age": 47,
                "Sex": "female"
            },
            {
                "Surname": "Ali",
                "Title": "Mr.",
                "First_Name": "Imran",
                "Last_Name": "Khan",
                "Age": 51,
                "Sex": "male"
            }
        ])
        save_data(df)  # Save default data
    return df


# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# Initialize session state for storing data
if 'people_df' not in st.session_state:
    st.session_state.people_df = load_data()

# Sidebar manual entry form
st.sidebar.header("➕ Add New Person")

with st.sidebar.form("add_person_form"):
    surname = st.text_input("Surname (e.g., Kumar)")
    title = st.selectbox("Title", ["Mr.", "Ms.", "Mrs.", "Dr."])
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    sex = st.selectbox("Sex", ["male", "female", "other"])

    submitted = st.form_submit_button("Add Person")

    if submitted:
        if surname and first_name and last_name:
            new_entry = pd.DataFrame([{
                "Surname": surname,
                "Title": title,
                "First_Name": first_name,
                "Last_Name": last_name,
                "Age": age,
                "Sex": sex
            }])
            st.session_state.people_df = pd.concat([st.session_state.people_df, new_entry], ignore_index=True)
            save_data(st.session_state.people_df)
            st.success("✅ Person added!")
        else:
            st.error("❗ Please fill in Surname, First Name, and Last Name.")

# Sidebar delete options
st.sidebar.header("🗑️ Delete Records")
delete_option = st.sidebar.radio("Select deletion option:", ["None", "Delete by Index", "Delete All"])

if delete_option == "Delete by Index":
    index_to_delete = st.sidebar.number_input("Enter row index to delete", min_value=0, max_value=len(st.session_state.people_df)-1)
    if st.sidebar.button("Delete Row"):
        st.session_state.people_df = st.session_state.people_df.drop(index_to_delete).reset_index(drop=True)
        save_data(st.session_state.people_df)
        st.success(f"🗑️ Row {index_to_delete} deleted!")

elif delete_option == "Delete All":
    if st.sidebar.button("Confirm Delete All"):
        st.session_state.people_df = pd.DataFrame(columns=["Surname", "Title", "First_Name", "Last_Name", "Age", "Sex"])
        save_data(st.session_state.people_df)
        st.success("💥 All records deleted!")

# Main search interface
st.title("🔍 Person Search Tool")

name_query = st.text_input("🔎 Search by Name or Surname")
title_filter = st.selectbox("👔 Filter by Title", options=["All"] + list(st.session_state.people_df["Title"].unique()), index=0)

sort_by = st.selectbox("📊 Sort By", options=["Age", "First_Name", "Surname"], index=0)
ascending = st.radio("⬆️ Sort Order", options=["Ascending", "Descending"], index=0)
ascending = ascending == "Ascending"

# Apply Filters
filtered_df = st.session_state.people_df.copy()

if name_query:
    filtered_df = filtered_df[
        filtered_df['First_Name'].str.contains(name_query, case=False, na=False) |
        filtered_df['Surname'].str.contains(name_query, case=False, na=False)
    ]

if title_filter != "All":
    filtered_df = filtered_df[filtered_df['Title'] == title_filter]

# Sort
filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

# Display Results
st.subheader("📋 Search Results")
st.dataframe(filtered_df, use_container_width=True)

# Summary Statistics
if not filtered_df.empty:
    st.subheader("📊 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Average Age", round(filtered_df["Age"].mean(), 1))
    col3.metric("Oldest", filtered_df["Age"].max())

    st.bar_chart(filtered_df['Title'].value_counts())

# CSV Download Button
@st.cache_data
def convert_df_to_csv(data):
    return data.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered_df)

st.download_button(
    label="💾 Download as CSV",
    data=csv,
    file_name='filtered_results.csv',
    mime='text/csv'
)
