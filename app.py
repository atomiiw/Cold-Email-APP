import streamlit as st
import pandas as pd
import re
import math

from email_generator import generate_emails
from read_file import read_docx, read_pdf

# -------------------------------
# Navigation with session state
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

# -------------------------------
# Page 1: File Upload
# -------------------------------
if st.session_state.page == 1:
    st.title("Step 1: Upload Files")
    st.write("Please upload the following:")
    company_csv = st.file_uploader("Upload Company CSV", type="csv")
    contacts_csv = st.file_uploader("Upload Contacts CSV", type="csv")
    resume_file = st.file_uploader("Upload Resume (docx or pdf)", type=["docx", "pdf"])
    
    if company_csv and contacts_csv and resume_file:
        if st.button("Next"):
            st.session_state.company_csv = company_csv
            st.session_state.contacts_csv = contacts_csv
            st.session_state.resume_file = resume_file
            st.session_state.page = 2
            st.rerun()

# -------------------------------
# Page 2: Processing and Additional Info
# -------------------------------
elif st.session_state.page == 2:
    st.title("Step 2: Processing")
    try:
        accounts = pd.read_csv(st.session_state.company_csv)
        contacts = pd.read_csv(st.session_state.contacts_csv)
    except Exception as e:
        st.error(f"Error reading CSV files: {e}")
        st.stop()
    
    # Read the resume file based on its type.
    resume_file = st.session_state.resume_file
    if resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = read_docx(resume_file)
    elif resume_file.type == "application/pdf":
        resume_text = read_pdf(resume_file)
    else:
        st.error("Unsupported resume file type.")
        st.stop()
    
    # Check companies for sufficient information in "Short Description"
    more_info_needed_for = []
    websites_for_reference = []
    
    if 'Short Description' not in accounts.columns:
        st.error("The accounts CSV must include a 'Short Description' column.")
        st.stop()
    
    for _, company in accounts.iterrows():
        company_description = str(company['Short Description'])
        words = re.split(r"[,\.;\s]+", company_description)
        words = [word for word in words if word]
        if len(words) < 30:
            more_info_needed_for.append(company['Company'])
            websites_for_reference.append(company['Website'])
    
    additional_info = {}
    if more_info_needed_for:
        st.write("Provide additional details (at least 30 words each) for the following companies:")
        for idx, company in enumerate(more_info_needed_for):
            label = f"{company} ({websites_for_reference[idx]})"
            additional_info[company] = st.text_area(label, key=company)
        
        if st.button("Submit Additional Info"):
            all_valid = True
            for company, info in additional_info.items():
                word_count = len(re.split(r"\s+", info.strip()))
                if word_count < 30:
                    st.error(f"Additional info for {company} is too short (only {word_count} words).")
                    all_valid = False
            if all_valid:
                # Append additional info to the company's short description
                for company in more_info_needed_for:
                    accounts.loc[accounts['Company'] == company, 'Short Description'] = \
                        accounts.loc[accounts['Company'] == company, 'Short Description'] + " " + additional_info[company]
                st.session_state.accounts = accounts
                st.session_state.contacts = contacts
                st.session_state.resume_text = resume_text
                st.session_state.page = 3
                st.experimental_rerun()
    else:
        st.write("All companies have sufficient information.")
        st.session_state.accounts = accounts
        st.session_state.contacts = contacts
        st.session_state.resume_text = resume_text
        if st.button("Next"):
            st.session_state.page = 3
            st.experimental_rerun()

# -------------------------------
# Page 3: Email Generation and CSV Download
# -------------------------------
elif st.session_state.page == 3:
    st.title("Step 3: Generating Emails")
    accounts = st.session_state.accounts
    contacts = st.session_state.contacts
    resume_text = st.session_state.resume_text
    
    num_accounts = len(accounts)
    # Estimated time: for 20 accounts, 7 minutes are required.
    estimated_time = math.ceil((num_accounts / 20) * 7)
    st.write(f"Estimated processing time: {estimated_time} minute(s)")
    
    with st.spinner("Producing emails..."):
        email_list = generate_emails(accounts, contacts, resume_text)
    
    st.write("Emails generated successfully!")
    
    # Convert the email list to a DataFrame and reorder columns.
    email_df = pd.DataFrame(email_list)
    email_df = email_df.rename(columns={"Website": "company website"})
    
    # Ensure the DataFrame has these columns in the desired order:
    desired_order = ["Company Name", "company website", "Recipient Title", "Recipient Name", "Recipient Email", "Subject", "Email Content"]
    email_df = email_df[[col for col in desired_order if col in email_df.columns]]
    
    # For companies with multiple entries, prioritize those with a filled "Recipient Name".
    email_df["recipient_priority"] = email_df["Recipient Name"].apply(lambda x: 0 if x.strip() else 1)
    email_df = email_df.sort_values(by=["Company Name", "recipient_priority"]).drop(columns=["recipient_priority"])
    
    st.dataframe(email_df)
    
    # Create CSV for download.
    csv = email_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Email CSV",
        data=csv,
        file_name="emails.csv",
        mime="text/csv"
    )
    
    st.write("Process complete!")
