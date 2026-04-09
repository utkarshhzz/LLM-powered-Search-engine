# Agentic AI Chatbot with Web Search & Research Tools 🤖🔍

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A powerful, interactive AI agent built with **Streamlit** and **LangChain**. Instead of just guessing answers, this agent utilizes native tool-calling via the ultra-fast **Groq API (Llama 3)** to dynamically search the web, pull academic papers, and query historical facts to answer your complex questions with grounded data.

## ✨ Features

- **🧠 Agentic Tool-Calling**: The LLM autonomously decides *if* and *when* it needs to use external tools to answer a prompt.
- **⚡ Ultra-Fast Inference**: Powered by the Groq LPU API running Llama 3 for near-instant reasoning.
- **🌐 DuckDuckGo Search**: Real-time web scraping for up-to-date news and information.
- **📚 ArXiv Integration**: Directly queries academic and scientific papers for deep-dive research questions.
- **🏛️ Wikipedia Integration**: Instantly summarizes encyclopedic entries for factual accuracy.
- **شف Transparent Reasoning**: The UI exposes the agent's intermediate steps, showing exactly which tool was used and what data was retrieved.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/) (Modern `create_tool_calling_agent` & `AgentExecutor`)
- **LLM**: Llama-3-8b-instant (via [Groq](https://groq.com/))
- **Tools**: `ArxivQueryRun`, `WikipediaQueryRun`, `DuckDuckGoSearchRun`

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A free [Groq API Key](https://console.groq.com/keys)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/agentic-ai-chatbot.git
   cd agentic-ai-chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   Create a new file named `.env` in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🎮 Usage

Start the Streamlit development server by running:

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8502`. Type a query like *"What are the latest papers on QLoRA?"* and watch the agent fetch real-time data!

## 💡 How it Works

1. The user inputs a query.
2. The prompt is passed to the **Llama 3** model, alongside descriptions of available tools (ArXiv, Wikipedia, Web Search).
3. The LLM determines the best tool for the job and generates a JSON-formatted tool call.
4. LangChain's `AgentExecutor` runs the requested tool, feeds the scraped data back to the LLM.
5. The LLM formulates a final, highly accurate response which is streamed to the front-end, along with dropdowns showing the exact tool interactions.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/agentic-ai-chatbot/issues).

## 📝 License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
