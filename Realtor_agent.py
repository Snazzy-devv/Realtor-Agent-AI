# RealEstateAgent.py

# %% IMPORTS
import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# %% LOAD ENVIRONMENT VARIABLES
load_dotenv(override=True)

# Fetch OpenRouter API key from Streamlit secrets or .env
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("❌ OpenRouter API key not found! Please set it in Streamlit Secrets or .env.")
    st.stop()

# Set CrewAI / LiteLLM environment variables
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# %% STREAMLIT PAGE SETUP
st.set_page_config(page_title="Real Estate AI Agent", page_icon="🏠", layout="wide")
st.title("🏠 Real Estate Marketing & Lead Intelligence")

# %% INITIALIZE LLM
cust_llm = LLM(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    temperature=0.7,
)

# %% TOOLS
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Custom tool to notify admin & store leads
class NotifyAdminAndStoreLead(BaseTool):
    name: str = "notify_admin_and_store_lead"
    description: str = "Store qualified lead info and notify admin."

    def _run(self, client_name: str, client_email: str, client_phone: str, score: int):
        print("New Qualified Lead")
        print("Name:", client_name)
        print("Email:", client_email)
        print("Phone:", client_phone)
        print("Score:", score)
        return "Lead stored and admin notified"

notify_tool = NotifyAdminAndStoreLead()

# Optional webhook version
def notify_admin_and_store_lead_webhook(lead_data_json):
    WEBHOOK_URL = "https://script.google.com/macros/s/YOUR_WEB_APP_ID/exec"
    try:
        data = json.loads(lead_data_json)
        response = requests.post(WEBHOOK_URL, json=data)
        return f"Success: Lead logged. Response: {response.text}"
    except Exception as e:
        return f"Error sending lead: {str(e)}"

# %% AGENTS
marketing_agent = Agent(
    role='Marketing Content Specialist',
    goal='Create high-conversion listings and social media content for {property_details}.',
    backstory="Expert in real estate copywriting and digital marketing trends.",
    verbose=True,
    max_iter=3
)

research_agent = Agent(
    role='Market Data Analyst',
    goal='Verify if the lead budget of {budget} is realistic for {location}.',
    backstory="Specializes in real-time market pricing. You verify if lead expectations match reality.",
    tools=[search_tool, scrape_tool],
    verbose=True,
    max_iter=3
)

ops_manager = Agent(
    role="Lead Operations Manager",
    goal="Filter high-quality leads and store their contact info.",
    backstory="You check lead scores and store leads with score greater than 7.",
    tools=[notify_tool],
    verbose=True,
    max_iter=3
)

# %% TASKS
task_marketing = Task(
    description="""Generate a full marketing kit for {property_details}:
    1. Professional Listing Description.
    2. Instagram Caption.
    3. WhatsApp Broadcast message.""",
    expected_output="A structured document containing all marketing copy.",
    agent=marketing_agent
)

task_qualification = Task(
    description="""Search for current real estate prices in {location}. 
    Compare the lead's budget ({budget}) and timeline ({timeline}) to market reality.
    Assign a quality score from 1-10 and explain why.""",
    expected_output="A lead evaluation report with a 1-10 score and reasoning.",
    agent=research_agent
)

task_storage = Task(
    description="""Review the qualification report for {client_name}. 
    If the score is 7 or higher, create a JSON string with these keys: 
    'name', 'email', 'phone', 'location', 'budget', 'score', 'summary'.
    Then, call notify_admin_and_store_lead with that JSON string.""",
    expected_output="Confirmation that the lead was stored or a reason for rejection.",
    agent=ops_manager,
    context=[task_qualification]
)

# %% STREAMLIT UI - SIDEBAR
with st.sidebar:
    st.header("👤 Single Lead Entry")
    c_name = st.text_input("Client Name", placeholder="John Doe")
    c_email = st.text_input("Email")
    c_phone = st.text_input("Phone")
    c_loc = st.text_input("Location", placeholder="Lekki, Lagos")
    c_bud = st.text_input("Budget", placeholder="$500,000")
    c_time = st.selectbox("Timeline", ["Immediate", "1-3 Months", "Looking"])
    c_prop = st.text_area("Property Details", placeholder="e.g. 4-bedroom terrace")
    
    run_single = st.button("🚀 Process Single Lead", type="primary")

    st.divider()
    
    st.header("📂 Batch Processing")
    st.write("Run the pre-defined daily list of leads.")
    run_batch = st.button("🔄 Run Daily Batch")

# %% HELPER FUNCTION
def run_real_estate_crew(input_data):
    crew = Crew(
        agents=[marketing_agent, research_agent, ops_manager],
        tasks=[task_marketing, task_qualification, task_storage],
        process=Process.sequential,
        verbose=True
    )
    return crew.kickoff(inputs=input_data)

# %% SINGLE LEAD LOGIC
if run_single:
    if not c_name or not c_bud:
        st.warning("Please enter at least a Name and Budget.")
    else:
        with st.spinner(f"Analyzing {c_name}..."):
            inputs = {
                'client_name': c_name, 'client_email': c_email, 'client_phone': c_phone,
                'property_details': c_prop, 'budget': c_bud, 'location': c_loc, 'timeline': c_time
            }
            result = run_real_estate_crew(inputs)
            st.success("Lead Processing Complete!")
            st.markdown("### 📊 AI System Report")
            st.info(result)

# %% BATCH PROCESSING LOGIC
if run_batch:
    daily_leads = [
        {'client_name': 'Alice Smith', 'client_email': 'alice@example.com', 'client_phone': '+234111222', 'property_details': '3BR Apartment in Lekki', 'budget': '$150,000', 'location': 'Lekki, Lagos', 'timeline': '3 months'},
        {'client_name': 'Bob Jones', 'client_email': 'bob@example.com', 'client_phone': '+234333444', 'property_details': '5BR Mansion in Ikoyi', 'budget': '$2,000,000', 'location': 'Ikoyi, Lagos', 'timeline': 'Immediate'}
    ]
    
    st.write(f"Processing {len(daily_leads)} leads...")
    for lead in daily_leads:
        with st.expander(f"Processing: {lead['client_name']}", expanded=True):
            result = run_real_estate_crew(lead)
            st.write(result)
    st.success("All batch leads processed!")
