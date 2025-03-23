from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from models import llm
from chains import experience_chain, company_chain, match_chain, interest_chain, interest_processing_chain, email_chain, email_opt_chain
from prompts import experience_summary_requirement, company_summary_requirement, interest_requirement, email_requirement, email_opt_requirement, email_opt_requirement

def generate_emails(accounts, contacts, resume):
    """
    Given:
      - accounts: a DataFrame with columns including 'Company', 'Short Description', and optionally 'Website'
      - contacts: a DataFrame with columns including 'Company', 'First Name', 'Last Name', 'Title', 'Email'
      - resume: a string containing the candidate's resume
    
    Global variables expected:
      - experience_summary, experience_summary_requirement
      - company_summary, company_summary_requirement
      - experience_company_matching
      - interest
      - interest_processing, interest_requirement
      - email_prompt, email_requirement
      - email_opt_prompt, email_opt_requirement
      - llm, claude
      
    Returns:
      A list of dictionaries, each with keys:
        'Subject', 'Email Content', 'Recipient Name', 'Recipient Title',
        'Recipient Email', 'Company Name', 'Website'
    """
    # --- Step 1: Use two simple agents to extract my_name and identity from the resume ---
    # Create prompt templates for extracting first name and professional identity.
    my_name_prompt = PromptTemplate.from_template(
        "Extract the candidate's first name from the resume. Resume: {resume}"
    )
    identity_prompt = PromptTemplate.from_template(
        "Extract a brief summary of my professional identity (including education and field) from the resume. Resume: {resume}"
    )
    my_name_chain = LLMChain(llm=llm, prompt=my_name_prompt)
    identity_chain = LLMChain(llm=llm, prompt=identity_prompt)
    
    # Run the chains to get my_name and identity.
    my_name = my_name_chain.run({"resume": resume}).strip()
    identity = identity_chain.run({"resume": resume}).strip()
    
    # --- Step 2: Generate a summary of experiences once using the resume ---
    experience_output = experience_chain.run({
        "resume": resume,
        "experience_summary_requirement": experience_summary_requirement
    })
    
    # List to store the output emails.
    email_list = []
    
    # --- Step 3: Process each company in accounts ---
    for _, company_row in accounts.iterrows():
        company_name = company_row["Company"]
        # Prepare company_info using the company's name and its short description.
        company_info = f"{company_name} - {company_row['Short Description']}"
        
        # Get a summary of what the company does.
        company_output = company_chain.run({
            "company_info": company_info,
            "company_summary_requirement": company_summary_requirement
        })
        
        # Match the candidate’s experiences with the company’s distinct aspects.
        match_output = match_chain.run({
            "company_output": company_output,
            "experience_output": experience_output
        })
        
        # Generate a personal interest statement.
        interest_output = interest_chain.run({
            "company_output": company_output,
            "experience_output": experience_output
        })
        
        # Process the interest output further.
        interest_processing_output = interest_processing_chain.run({
            "interest_output": interest_output,
            "interest_requirement": interest_requirement
        })
        
        # Create the initial email content.
        email_output = email_chain.run({
            "my_name": my_name,
            "identity": identity,
            "company_name": company_name,
            "email_requirement": email_requirement,
            "interest_processing_output": interest_processing_output,
            "match_output": match_output
        })
        
        # --- Step 4: Find matching contacts for the current company ---
        potential_contacts = contacts[contacts["Company"] == company_name]
        # filter by Title containing desired keywords.
        filtered_contacts = potential_contacts[
            potential_contacts["Title"].str.contains(r"\b(CEO|CTO|Founder|Co-Founder)\b", case=False, na=False)
        ]
        # Use filtered contacts if available.
        if not filtered_contacts.empty:
            selected_contacts = filtered_contacts
        else:
            selected_contacts = None
        
        # --- Step 5: Create emails for each matching contact (or a single email with blank recipient if none) ---
        if selected_contacts is not None and not selected_contacts.empty:
            for _, contact_row in selected_contacts.iterrows():
                recipient_name = f"{contact_row['First Name']} {contact_row['Last Name']}"
                recipient_title = contact_row["Title"]
                recipient_email = contact_row["Email"]
                # Optimize the email by addressing the recipient by name.
                email_opt_output = email_opt_chain.run({
                    "email_output": email_output,
                    "recipient_name": recipient_name,
                    "my_name": my_name,
                    "email_opt_requirement": email_opt_requirement
                })
                email_opt_output += "\n P.S. My resume is attached for your reference."
                # Generate a subject line.
                subject = email_opt_output.split('\n\n')[0].strip()
                # Get rid of the subject line from the email_opt_output
                email_opt_output = '\n\n'.join(email_opt_output.split('\n\n')[1:]).lstrip()
                # Get Website if available.
                company_link = company_row["Website"] if "Website" in company_row.index else ""
                # Append the email information to the list.
                email_list.append({
                    "Subject": subject,
                    "Email Content": email_opt_output,
                    "Recipient Name": recipient_name,
                    "Recipient Title": recipient_title,
                    "Recipient Email": recipient_email,
                    "Company Name": company_name,
                    "Website": company_link
                })
        else:
            # No matching contacts were found; create an email with blank recipient details.
            email_opt_output = email_opt_chain.run({
                "email_output": email_output,
                "recipient_name": "",
                "my_name": my_name,
                "email_opt_requirement": email_opt_requirement
            })
            email_opt_output += "\n P.S. My resume is attached for your reference."
            subject = email_opt_output.split('\n\n')[0].strip()
            email_opt_output = '\n\n'.join(email_opt_output.split('\n\n')[1:]).lstrip()
            company_link = company_row["Website"] if "Website" in company_row.index else ""
            email_list.append({
                "Subject": subject,
                "Email Content": email_opt_output,
                "Recipient Name": "",
                "Recipient Title": "",
                "Recipient Email": "",
                "Company Name": company_name,
                "Website": company_link
            })
    
    return email_list