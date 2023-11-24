import streamlit as st
import pandas as pd
from datetime import datetime

st.title("AMS Lab Management App")

st.write("In this application, we would like to provide real time status of our labs.")

st.subheader("Status of our labs")
current_date = datetime.now()
st.write(f"Current date: {current_date.strftime('%d-%B-%Y')}")

# latest status
df = pd.read_excel('current_stat.xlsx')

# Function to apply custom styling
def highlight_text(cell):
    return 'color: green' if 'Available' in cell else 'color: red'

# Apply custom styling to the 'Status' column
styled_df = df.style.applymap(lambda cell: highlight_text(cell), subset=['Status'])
styled_df = styled_df.hide_index()


# Display the table without the index column using HTML
st.markdown(styled_df.to_html(), unsafe_allow_html=True)
st.write('\n')
# Display a web link
st.markdown('[Click here](https://docs.google.com/spreadsheets/d/1_IVksfmKi8lxfHcUD-qgFm-vPgqTXohnld9FkTa-4HE/edit?usp=sharing) to see our lab schedule.')
st.markdown('[Click here](https://docs.google.com/spreadsheets/d/1YY7TXEHvCvMn-DkrQDjyUXLIO1fnPV7xlOb-NvwHtwo/edit?usp=sharing) to see detail information of each lab.')

# Convert dataframe to dictionnary
data = df.to_dict(orient='list')

st.sidebar.markdown("<h2 style='color: blue;'>To use lab, fill in the infomaton below:</h2>", unsafe_allow_html=True)
room = st.sidebar.selectbox("Select a room: ", data['Labs'])
name = st.sidebar.text_input('Enter your name:')
s_id = st.sidebar.text_input('Enter your student id:')
p_no = st.sidebar.text_input("Enter your phone number:")
t_in = datetime.now().strftime("%H:%M")
st.sidebar.write('Time in:')
st.sidebar.write(t_in)
t_out = st.sidebar.text_input("Enter time out:")

bu = st.sidebar.button("Enter")

if bu:
    r_index = data['Labs'].index(room)
    data['Status'][r_index] = "Unavailable"
    data['Key at/with'][r_index] = name
    data['Stduent ID'][r_index] = s_id
    data['Phone number'][r_index] = p_no
    data['Time In'][r_index] = t_in
    data['Time Out'][r_index] = t_out

    # Update DataFrame
    df_updated = pd.DataFrame(data)
    # Apply custom styling to the 'Highlighted Text' column
    styled_df_updated = df_updated.style.applymap(lambda cell: highlight_text(cell), subset=['Status'])
    # Display the table without the index column using HTML
    st.subheader("The status will be updated to:")
    st.markdown(styled_df_updated.to_html(index=False), unsafe_allow_html=True)

    # Save DataFrame to Excel without index
    df_updated.to_excel('current_stat.xlsx', index=False)

st.sidebar.markdown("<h2 style='color: red;'>This section is for AMS admins only!</h2>", unsafe_allow_html=True)

st.sidebar.write("Select lab room that you want to reset")
lab = st.sidebar.selectbox("Select a lab: ", data['Labs'])

# User credentials
valid_users = {'AMS1': 'password1', 'AMS2': 'password2'}

username = st.sidebar.text_input("Username:")
password = st.sidebar.text_input("Password:", type="password")

r_bu = st.sidebar.button("Reset")

if (username in valid_users and password == valid_users[username]) and r_bu:
    st.sidebar.success("Login Successful!")
    r_index = data['Labs'].index(lab)
    data['Status'][r_index] = "Available"
    data['Key at/with'][r_index] = "AMS-103F"
    data['Stduent ID'][r_index] = ""
    data['Phone number'][r_index] = ""
    data['Time In'][r_index] = ""
    data['Time Out'][r_index] = ""

    # Update DataFrame
    df_updated = pd.DataFrame(data)
    # Apply custom styling to the 'Highlighted Text' column
    styled_df_updated = df_updated.style.applymap(lambda cell: highlight_text(cell), subset=['Status'])
    # Display the table without the index column using HTML
    st.subheader("The status will be updated to:")
    st.markdown(styled_df_updated.to_html(index=False), unsafe_allow_html=True)
    # Save DataFrame to Excel without index
    df_updated.to_excel('current_stat.xlsx', index=False) 
 




