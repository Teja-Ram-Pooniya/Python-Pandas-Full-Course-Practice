import pandas as pd

# Original Dataframe
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

# Split 'Name' column into parts
df[['Surname', 'Rest']] = df['Name'].str.split(',', expand=True)
df[['Title', 'Full_Name']] = df['Rest'].str.split(n=1, expand=True)

# Optional: Remove parenthese from Title if any
df['Title'] = df['Title'].str.strip()

# Split Full_Name into First and Last Name
df[['First_Name', 'Last_Name']] = df['Full_Name'].str.rsplit(n=1, expand=True)

# Drop intermediate columns
df.drop(columns=['Name', 'Rest'], inplace=True)

# Reorder columns
df = df[['Surname', 'Title', 'First_Name', 'Last_Name', 'Age', "Sex"]]


filtered_by_age = df[df['Age'] > 35]
print(filtered_by_age)
print("=================================================")

filtered_by_name = df[df['First_Name'].str.contains("Ashok", case=False, na=False)]
print(filtered_by_name)
print("=================================================")

print(df)
