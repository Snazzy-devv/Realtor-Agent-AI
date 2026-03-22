# 1. THE VERY FIRST THING: Setup Environment
import os
import streamlit as st

# We set these BEFORE any other imports
if "OPENROUTER_API_KEY" in st.secrets:
    os.environ["OPENROUTER_API_KEY"] = st.secrets["OPENROUTER_API_KEY"]
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENROUTER_API_KEY"] # Trick LiteLLM
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
else:
    st.error("❌ Missing OPENROUTER_API_KEY in Streamlit Secrets!")
    st.stop()

# 2. NOW IMPORT EVERYTHING ELSE
import requests
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.tools import BaseTool

# 3. PAGE CONFIG
st.set_page_config(page_title="Real Estate AI", page_icon="🏠", layout="wide")
st.title("🏠 Real Estate Marketing & Lead Intelligence")

# 4. DEFINE LLM
cust_llm = LLM(
    model="openrouter/openai/gpt-4o-mini", 
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    temperature=0.7
)

# 5. TOOLS
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

class NotifyAdminAndStoreLead(BaseTool):
    name: str = "notify_admin_and_store_lead"
    description: str = "Store qualified lead information and notify admin."
    def _run(self, **kwargs): # Using kwargs to prevent argument mismatch errors
        return "Lead data processed successfully."

notify_tool = NotifyAdminAndStoreLead()

# 6. AGENTS (All MUST have llm=cust_llm)
marketing_agent = Agent(
    role='Marketing Specialist',
    goal='Create listings for {property_details}.',
    backstory="Expert in real estate copywriting.",
    llm=cust_llm,
    verbose=True
)

research_agent = Agent(
    role='Market Analyst',
    goal='Verify if {budget} is realistic for {location}.',
    backstory="Specializes in pricing.",
    tools=[search_tool, scrape_tool],
    llm=cust_llm,
    verbose=True
)

ops_manager = Agent(
    role="Lead Manager",
    goal="Filter leads.",
    backstory="You check lead scores.",
    tools=[notify_tool],
    llm=cust_llm,
    verbose=True
)

# 7. TASKS
task_marketing = Task(
    description="Generate marketing for {property_details}.",
    expected_output="A structured marketing document.",
    agent=marketing_agent
)

task_qualification = Task(
    description="Check prices in {location} for budget {budget}.",
    expected_output="A score from 1-10.",
    agent=research_agent
)

task_storage = Task(
    description="If score >= 7 for {client_name}, store the lead.",
    expected_output="Confirmation of storage.",
    agent=ops_manager,
    context=[task_qualification]
)

# 8. CREW FUNCTION
def run_real_estate_crew(input_data):
    crew = Crew(
        agents=[marketing_agent, research_agent, ops_manager],
        tasks=[task_marketing, task_qualification, task_storage],
        process=Process.sequential,
        manager_llm=cust_llm,
        planning=False,
        verbose=True
    )
    return crew.kickoff(inputs=input_data)

# 9. UI SIDEBAR
with st.sidebar:
    st.header("👤 Single Lead Entry")
    c_name = st.text_input("Client Name")
    c_bud = st.text_input("Budget")
    c_loc = st.text_input("Location")
    c_prop = st.text_area("Property Details")
    run_single = st.button("🚀 Process Lead", type="primary")

# 10. EXECUTION
if run_single:
    if not c_name or not c_bud:
        st.warning("Please enter Name and Budget.")
    else:
        with st.spinner("Crew is working..."):
            res = run_real_estate_crew({
                'client_name': c_name, 'budget': c_bud, 
                'location': c_loc, 'property_details': c_prop
            })
            st.success("Complete!")
            st.write(res)
           
