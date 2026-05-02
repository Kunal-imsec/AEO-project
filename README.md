<div align="center">

# 🤖✨ AEO Project
### *Answer Engine Optimization — because SEO is so last decade*

![Python](https://img.shields.io/badge/Python-63%25-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-35%25-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Bundler-646CFF?style=for-the-badge&logo=vite&logoColor=white)

> 🧠 *"If your brand isn't showing up in AI answers, does it even exist?"*

</div>

---

## 🌟 What is this?

**AEO Project** is a full-stack AI-powered tool that helps you understand how your brand is perceived by **Large Language Models** (LLMs). Think of it as SEO, but for the AI era — tracking how often, where, and alongside whom your brand appears in AI-generated responses.

```
Traditional SEO   →   "Rank on Google"
AEO               →   "Be mentioned by AI"  🤯
```

It sends queries to multiple LLMs, parses their responses, extracts brand mentions and rankings, detects competitors, and delivers clean, structured reports — all through a slick React frontend.

---

## 🗂️ Project Structure

```
AEO-project/
│
├── 🐍 aeo-backend/          # Python + FastAPI powerhouse
│   ├── main.py              # 🚪 API entry point
│   ├── llm_orchestrator.py  # 🎭 Calls multiple LLMs
│   ├── query_generator.py   # 🧠 Crafts smart prompts
│   ├── response_parser.py   # 🔍 Extracts brand signals
│   ├── report_builder.py    # 📊 Builds final reports
│   ├── requirements.txt     # 📦 Python deps
│   └── .env                 # 🔑 API keys (keep secret!)
│
├── ⚛️  aeo-frontend/         # React + Vite magic
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputForm.jsx    # 📝 Query input UI
│   │   │   └── ReportCard.jsx   # 📋 Results display
│   │   ├── App.jsx              # 🏠 Root component
│   │   └── main.jsx             # 🚀 Entry point
│   ├── index.html
│   └── package.json
│
├── .gitignore
└── README.md                # 👋 You are here!
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Multi-LLM Querying** | Fires your query at multiple AI engines simultaneously |
| 📊 **Brand Visibility Score** | Quantifies how prominently your brand appears |
| 🏆 **Ranking Detection** | Finds where your brand sits in the pecking order |
| ⚔️ **Competitor Identification** | Automatically spots rival brands in responses |
| 📄 **Structured Reports** | Clean JSON + UI reports ready for decision-making |
| ⚡ **FastAPI Backend** | Blazing-fast async Python API |
| 🎨 **React Frontend** | Smooth, modern UI to interact with all that data |

---

## 🛠️ Tech Stack

### 🐍 Backend
- **Python** — core language (63% of codebase!)
- **FastAPI** — async REST API framework
- **Uvicorn** — lightning-fast ASGI server
- **NLP / Regex parsing** — response analysis engine
- **Multi-LLM orchestration** — Groq, OpenAI, etc.

### ⚛️ Frontend
- **React** — component-based UI
- **Vite** — next-gen build tooling
- **JavaScript** — 35% of codebase
- **Tailwind CSS** — clean, utility-first styling

---

## 🚀 Getting Started

### Prerequisites

Make sure you have these installed:
- 🐍 Python 3.9+
- 📦 Node.js 18+
- 🔑 API keys for your chosen LLMs (Groq / OpenAI)

---

### 1️⃣ Clone the repo

```bash
git clone https://github.com/Kunal-imsec/AEO-project.git
cd AEO-project
```

---

### 2️⃣ Set up the Backend

```bash
cd aeo-backend
pip install -r requirements.txt
```

Create your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Start the server:

```bash
uvicorn main:app --reload
```

> 🟢 Backend will be live at `http://localhost:8000`

---

### 3️⃣ Set up the Frontend

```bash
cd ../aeo-frontend
npm install
npm run dev
```

> 🎨 Frontend will be live at `http://localhost:5173`

---

## 🔄 How It Works

```
 You type a query
       │
       ▼
  ┌─────────────┐
  │  React UI   │  ← InputForm.jsx
  └──────┬──────┘
         │ HTTP POST
         ▼
  ┌─────────────────┐
  │   FastAPI App   │  ← main.py
  └──────┬──────────┘
         │
         ▼
  ┌───────────────────────┐
  │   LLM Orchestrator    │  ← Sends to GPT, Groq, etc.
  └──────────┬────────────┘
             │ raw responses
             ▼
  ┌───────────────────────┐
  │   Response Parser     │  ← Extracts brand signals
  └──────────┬────────────┘
             │ structured data
             ▼
  ┌───────────────────────┐
  │   Report Builder      │  ← Compiles final insights
  └──────────┬────────────┘
             │ JSON report
             ▼
  ┌─────────────┐
  │  React UI   │  ← ReportCard.jsx displays results
  └─────────────┘
```

---

## 📊 Example Output

```json
{
  "query": "best cloud storage providers",
  "brand": "Dropbox",
  "mention_count": 6,
  "average_rank": 3.2,
  "visibility_score": 78.4,
  "competitors_detected": [
    "Google Drive",
    "OneDrive",
    "iCloud",
    "Box"
  ],
  "llms_queried": ["gpt-4o", "llama3-70b"],
  "timestamp": "2026-05-03T10:32:00Z"
}
```

---

## 🎯 Use Cases

- 🏢 **Brand managers** — track AI presence across LLMs
- 📣 **Marketing teams** — optimize content for AI answer engines
- 🔬 **Researchers** — study how LLMs represent brand data
- 🧑‍💼 **Consultants** — generate AEO audit reports for clients
- 🎓 **Students** — learn full-stack AI app development

---

## 🗺️ Roadmap

- [x] Multi-LLM query orchestration
- [x] Brand mention extraction
- [x] Competitor detection
- [x] React frontend with report display
- [ ] 📈 Real-time streaming responses
- [ ] 📅 Historical trend tracking
- [ ] 🗺️ Dashboard with charts & analytics
- [ ] 🔗 RAG integration for custom brand datasets
- [ ] 🐳 Docker Compose deployment
- [ ] 🔒 User authentication & saved reports

---

## 🤝 Contributing

Contributions are super welcome! 🎉

```bash
# Fork the repo, then:
git checkout -b feature/your-amazing-feature
git commit -m "✨ add: your amazing feature"
git push origin feature/your-amazing-feature
# Open a Pull Request!
```

Please keep commits clean and descriptive. 💅

---

## 📜 License

This project is licensed under the **MIT License** — use it, fork it, build on it. 🚀

---

## 👨‍💻 Author

<div align="center">

**Kunal** · [@Kunal-imsec](https://github.com/Kunal-imsec)

*Building tools for the AI-first world* 🌍

---

⭐ **If this project helped you, drop a star!** ⭐

*It takes 2 seconds and makes my day* ☀️

</div>

Just say: **“make it top 1% project”**
::contentReference[oaicite:1]{index=1}
```
