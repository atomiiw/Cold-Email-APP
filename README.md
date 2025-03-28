# 🎯 Cold Email Automation Tool for Summer Internship Outreach

This is a **Streamlit-based AI tool** that helps students generate high-quality, personalized cold emails for summer internship outreach—quickly and effectively.

🔗 **Launch the app**:  
[Cold Email App](https://cold-email-app-4bfy4gydmeqr6bqykfpthg.streamlit.app/)

---

## 📂 What You Need to Get Started

To use the app, you'll need to upload:

- **Your resume** (PDF)
- **Contacts CSV** from Apollo
- **Accounts CSV** from Apollo

> 🧪 A toy dataset is available in the `Toy Data/` folder for testing purposes.

---

## ⚙️ How It Works

This app is powered by **LangChain** and a set of **specialized AI agents**, each handling a specific part of the cold email creation process:

1. **Company Analysis** – Understands the company from Apollo data and short user input  
2. **Self Analysis** – Extracts relevant highlights from your resume  
3. **Fit Discovery** – Finds alignment between you and the company  
4. **Email Drafting** – Writes a personalized cold email  
5. **Email Polishing** – Refines the language to sound more natural and compelling

📝 If the company information from Apollo is under 30 words, the app will prompt you to supplement it manually. You’ll be given a link and just need to paste in a short blurb—this step is integrated into the workflow.

---

## 📤 Output

The final result is a **downloadable CSV** containing:

- Personalized email content
- Contact information

You can then copy and paste the content directly into your emails.

---

## 🔮 What’s Next

Future versions will:

- Automate the company information supplementing step using a browser tool
- Allow full in-app editing and sending of emails directly from the interface
