import streamlit as st
import os
import requests
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.tools import BaseTool

# 1. SETUP KEYS & ENVIRONMENT
# This must happen BEFORE the agents are initialized
if "OPENROUTER_API_KEY" in st.secrets:
    os.environ["OPENROUTER_API_KEY"] = st.secrets["OPENROUTER_API_KEY"]
    # Provide a dummy OpenAI key to satisfy CrewAI's internal checks
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key"
    # Map all internal calls to OpenRouter
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
else:
    st.error("Missing OPENROUTER_API_KEY in Streamlit Secrets!")

# 2. DEFINE THE OPENROUTER LLM
cust_llm = LLM(
    model="openrouter/openai/gpt-4o-mini", 
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    temperature=0.7,
)

# 3. PAGE SETUP
st.set_page_config(page_title="Real Estate AI Agent", page_icon="🏠", layout="wide")
st.title("🏠 Real Estate Marketing & Lead Intelligence")

# 4. TOOLS
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

class NotifyAdminAndStoreLead(BaseTool):
    name: str = "notify_admin_and_store_lead"
    description: str = "Store qualified lead information and notify admin."
    def _run(self, client_name: str, client_email: str, client_phone: str, score: int):
        return f"Lead for {client_name} stored and admin notified."

notify_tool = NotifyAdminAndStoreLead()

# 5. AGENTS (Assigned cust_llm to every agent)
marketing_agent = Agent(
    role='Marketing Content Specialist',
    goal='Create listings for {property_details}.',
    backstory="Expert in real estate copywriting.",
    llm=cust_llm, # <--- FIXED
    verbose=True
)

research_agent = Agent(
    role='Market Data Analyst',
    goal='Verify if the budget of {budget} is realistic for {location}.',
    backstory="Specializes in real-time market pricing.",
    tools=[search_tool, scrape_tool],
    llm=cust_llm, # <--- FIXED
    verbose=True
)

ops_manager = Agent(
    role="Lead Operations Manager",
    goal="Filter high-quality leads.",
    backstory="You check lead scores.",
    tools=[notify_tool],
    llm=cust_llm, # <--- FIXED
    verbose=True
)

# 6. TASKS
task_marketing = Task(
    description="Generate a marketing kit for {property_details}.",
    expected_output="Marketing copy document.",
    agent=marketing_agent
)

task_qualification = Task(
    description="Search prices in {location} and compare to budget {budget}.",
    expected_output="Evaluation report with a 1-10 score.",
    agent=research_agent
)

task_storage = Task(
    description="If score >= 7 for {client_name}, call notify_tool.",
    expected_output="Confirmation of storage.",
    agent=ops_manager,
    context=[task_qualification]
)

# 7. CREW FUNCTION (Added manager_llm)
def run_real_estate_crew(input_data):
    crew = Crew(
        agents=[marketing_agent, research_agent, ops_manager],
        tasks=[task_marketing, task_qualification, task_storage],
        process=Process.sequential,
        manager_llm=cust_llm, # <--- FIXED: Forces manager to use OpenRouter
        planning=False,       # <--- FIXED: Prevents default OpenAI planning calls
        verbose=True
    )
    return crew.kickoff(inputs=input_data)

# 8. UI LOGIC (Remains the same as your code)
with st.sidebar:
    st.header("👤 Single Lead Entry")
    c_name = st.text_input("Client Name")
    c_bud = st.text_input("Budget")
    # ... (rest of your inputs)
    run_single = st.button("🚀 Process Single Lead", type="primary")

if run_single:
    if not c_name or not c_bud:
        st.warning("Please enter at least a Name and Budget.")
    else:
        with st.spinner(f"Analyzing {c_name}..."):
            inputs = {'client_name': c_name, 'budget': c_bud, 'location': 'Lagos', 'property_details': 'House'} # Simplified for test
            result = run_real_estate_crew(inputs)
            st.info(result)
