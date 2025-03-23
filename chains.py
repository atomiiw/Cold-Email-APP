from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from models import llm, claude

experience_summary = PromptTemplate.from_template(
    "Study this person's professional experience: {resume}. "
    "For each experience they have, use short phrases and keywords to characterize the experience."
    "Following this instruction: {experience_summary_requirement}."
)
experience_chain = LLMChain(llm=llm, prompt=experience_summary)

company_summary = PromptTemplate.from_template(
    "Look at what this company does: {company_info}. "
    "Use short phrases and keywords to characterize this company."
    "Following this instruction: {company_summary_requirement}."
)
company_chain = LLMChain(llm=llm, prompt=company_summary)

experience_company_matching = PromptTemplate.from_template(
    "Look at this company: {company_output}. "
    "Look at this person's professional experiences: {experience_output}."
    "First, silently (internally) reflect on the company's work and identify two distinctly different aspects of their product, technology, or overall approach—aim for clearly separate domains (e.g., hardware vs. data analysis, surgical precision vs. clinical result, neuroscience research vs. real-time robotics). Then, from the person's listed experiences, creatively select **two** that best match these distinctly different aspects you've identified. The two chosen experiences should be intentionally varied to showcase the person’s ability to contribute across different parts of the company's work. In your response: - Provide only the **titles** of the two selected experiences (no additional details). - After each title, clearly explain why you selected it, specifically highlighting how each experience uniquely connects to one distinct aspect of the company's work. Do it in a very specific way. Provide at least two reasons. In each reason imagine the specific task or situation where this experience of mine might come into use."
)
match_chain = LLMChain(llm=llm, prompt=experience_company_matching)

interest = PromptTemplate.from_template(
    "Look at this company: {company_output}. "
    "Look at this person's professional experiences: {experience_output}."
    "Why would this person be interested in this company? Why would they feel enthusiatic about the company's field, industry, vision and product? Speak in first person POV."
)
interest_chain = LLMChain(llm=llm, prompt=interest)

interest_processing = PromptTemplate.from_template(
    "You are given this information about why I like this company: {interest_output}"
    "{interest_requirement}"
)
interest_processing_chain = LLMChain(llm=claude, prompt=interest_processing)

email_prompt = PromptTemplate.from_template(
    "Craft a successful cold email for this person me."
    "My name is {my_name}, I am a {identity}."
    "I hope to work over summer at this company: {company_name}."
    "Following this instruction: {email_requirement}."
    "Strictly align with the following information that I've already written out:"
    "The thing to write in paragraph 1 about why I am interested in this company: {interest_processing_output}"
    "Why I am a fit, supported by relevant experiences: {match_output}"
)
email_chain = LLMChain(llm=llm, prompt=email_prompt)

email_opt_prompt = PromptTemplate.from_template(
    "Edit this email to more closely align with my needs: {email_output}"
    "This email is written to: {recipient_name}"
    "My name is {my_name}"
    "{email_opt_requirement}"
)
email_opt_chain = LLMChain(llm=llm, prompt=email_opt_prompt)