# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 15:48:48 2025

@author: T.R.P.
"""

import pandas as pd

# Original DataFrame
df = pd.DataFrame(
    {
        "Name": [
            "Ashok, Mr. Ashok Kumar Khoja",
            "Tarun, Mr. Tarun Kumar Dadich",
            "Yagyadut, Mr. Yagyadut Dadich"
        ],
        "Age": [36, 56, 33],
        "Sex": ["male", "male", "male"],
    }
)

# Clean up names
df[['Surname', 'Rest']] = df['Name'].str.split(',', expand=True)
df[['Title', 'Full_Name']] = df['Rest'].str.split(n=1, expand=True)
df['Title'] = df['Title'].str.strip()
df[['First_Name', 'Last_Name']] = df['Full_Name'].str.rsplit(n=1, expand=True)
df.drop(columns=['Name', 'Rest', 'Full_Name'], inplace=True)
df = df[['Surname', 'Title', 'First_Name', 'Last_Name', 'Age', 'Sex']]

# Save original cleaned data to CSV
df.to_csv("cleaned_data1.csv", index=False)


# 🔍 Search Function
def search_people(df, name_query=None, title_filter=None, sort_by='Age', ascending=True):
    filtered_df = df.copy()

    # Search by First Name or Surname
    if name_query:
        filtered_df = filtered_df[
            filtered_df['First_Name'].str.contains(name_query, case=False, na=False) |
            filtered_df['Surname'].str.contains(name_query, case=False, na=False)
        ]

    # Filter by Title
    if title_filter:
        filtered_df = filtered_df[filtered_df['Title'] == title_filter]

    # Sort the result
    if sort_by in ['Age', 'First_Name', 'Surname']:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

    return filtered_df


# 🖥️ Interactive CLI Interface
def cli_interface(df):
    print("🔍 Welcome to Person Search Tool!")
    name_query = input("🔎 Enter name or surname to search (leave blank for none): ").strip()
    title_filter = input("👔 Enter title to filter (e.g., Mr., leave blank for none): ").strip()
    sort_by = input("📊 Sort by (Age/First_Name/Surname) [default: Age]: ").strip() or "Age"
    order = input("⬆️ Sort order (asc/desc) [default: asc]: ").strip().lower() or "asc"
    ascending = order == "asc"

    # Run search
    result = search_people(df, name_query=name_query, title_filter=title_filter,
                           sort_by=sort_by, ascending=ascending)

    if not result.empty:
        print("\n✅ Search Results:")
        print(result.to_string(index=False))

        # Option to export
        export = input("\n💾 Export results to CSV? (y/n): ").strip().lower()
        if export == 'y':
            filename = input("📁 Enter filename (default: filtered_results.csv): ").strip() or "filtered_results.csv"
            result.to_csv(filename, index=False)
            print(f"📂 Results saved to '{filename}'")
    else:
        print("🚫 No matching records found.")


# Run the CLI tool
cli_interface(df)