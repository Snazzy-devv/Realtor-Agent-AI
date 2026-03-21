# 🏡 Realtor Agent AI

An AI-powered real estate assistant built with CrewAI and Streamlit that helps users search, analyze, and explore property listings through a conversational interface. This project demonstrates how autonomous agents and Large Language Models (LLMs) can collaborate using tools like web search and scraping to deliver intelligent real estate insights.

---

## 🚀 Overview

This Realtor Agent allows users to interact naturally (via chat UI) to find properties based on preferences such as location, budget, and property type. It leverages agent-based workflows to gather, analyze, and present real estate data.

---

## 📌 Features

* 🔍 Property search using real-time web data
* 💬 Conversational interface powered by Streamlit
* 🤖 Multi-agent system using CrewAI
* 🌐 Web search integration (SerperDevTool)
* 🕸️ Website scraping for property details
* 📊 Intelligent summaries and recommendations
* 📥 Captures and stores qualified leads
* 📊 Automatically saves leads to Google Sheets

---

## 🚀 Demo

*check for demo video in file below*

---

## 🛠️ Tech Stack

* Python
* Streamlit
* CrewAI
* OpenAI API
* SerperDevTool (Search API)
* ScrapeWebsiteTool
* dotenv
* Requests / JSON

---

## 📂 Project Structure

```
realtor-agent/
│── app.py
│── .env
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/Snazzy-devv/realtor-agent.git
cd realtor-agent
```

2. Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_api_key_here
SERPER_API_KEY=your_serper_api_key
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the provided local URL in your browser and start interacting with the agent.

---

## 💬 Example Queries

* "Find a 3-bedroom house in Lagos"
* "Show me affordable apartments in Abuja"
* "Search for houses in Port Harcourt under 50 million"
* "Get details of properties in a specific area"

---

## 🧠 How It Works

1. User enters a query via the Streamlit interface
2. CrewAI agents are initialized with specific roles
3. Agents use tools like search and web scraping
4. The system identifies qualified leads based on user intent
5. Lead details (e.g., preferences, budget, location) are captured
6. Data is automatically stored in Google Sheets
7. Final response is generated and displayed to the user

---

## 🔒 Environment Variables

| Variable       | Description             |
| -------------- | ----------------------- |
| OPENAI_API_KEY | Your OpenAI API key     |
| SERPER_API_KEY | API key for search tool |

---

## 🧪 Future Improvements

* 🗺️ Map-based property visualization
* 📈 Price prediction using ML models
* 🏘️ Integration with real estate APIs
* 🧠 Memory for personalized searches
* 📱 Better UI/UX improvements

---

## 💼 Business Value

This project goes beyond a typical chatbot by solving a real business problem in real estate: **lead generation and qualification**.

* 🧲 **Automated Lead Capture**: Converts conversations into actionable leads without manual effort
* 🎯 **Lead Qualification**: Filters serious buyers based on budget, location, and intent
* 📊 **Centralized Data Storage**: Automatically stores leads in Google Sheets for easy access and tracking
* ⚡ **Faster Response Time**: Provides instant replies to potential clients, improving engagement
* 💰 **Sales Enablement**: Helps realtors focus only on high-quality prospects, increasing conversion rates

This system can be directly adapted for real estate agencies, property platforms, or sales teams looking to automate customer interaction and lead management.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License.

## 🙌 Acknowledgements

* OpenAI
* CrewAI
* Streamlit
* Serper API

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
