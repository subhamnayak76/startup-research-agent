# AI Startup Research Agent 🤖

An intelligent research agent built with LangGraph and LangChain that automatically discovers and extracts detailed information about startups from web searches. Perfect for investors, recruiters, or anyone researching startup companies.

## 🌟 Features

- **Intelligent Query Refinement**: Automatically enhances user queries for optimal search results
- **Web Search Integration**: Leverages Exa API for high-quality startup information retrieval
- **Structured Data Extraction**: Uses Google Gemini 2.5 Flash to extract company profiles with structured output
- **Comprehensive Company Profiles**: Extracts name, founders, website, tech stack, funding info, YC batch, and more
- **Multi-Stage Workflow**: Employs LangGraph's state machine for reliable, step-by-step processing
- **RESTful API**: FastAPI backend with MongoDB for user management and query history
- **Automated Report Generation**: Creates formatted reports with all discovered companies

## 🏗️ Architecture

The agent uses a multi-node workflow powered by LangGraph:
```
START → Query Refinement → Web Search → Data Extraction → Report Generation → END
```

Each node is responsible for a specific task:
- **Query Refinement Node**: Optimizes search queries using LLM
- **Search Node**: Executes web searches via Exa API
- **Extraction Node**: Parses results into structured company profiles
- **Report Node**: Formats findings into readable reports

## 🛠️ Tech Stack

- **AI/LLM**: LangChain, LangGraph, Google Gemini 2.5 Flash
- **Web Framework**: FastAPI
- **Database**: MongoDB with Beanie ODM
- **Search**: Exa API
- **Authentication**: bcrypt for password hashing
- **Validation**: Pydantic models

## 📋 Prerequisites

- Python 3.8+
- MongoDB instance (local or cloud)
- Google Gemini API key
- Exa API key

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-startup-research-agent.git
cd ai-startup-research-agent
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
EXA_API_KEY=your_exa_api_key_here
mongo_url=mongodb://localhost:27017
```

## 🎯 Usage

### Starting the Server
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. User Registration
```http
POST /users/signup
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### 2. User Login
```http
POST /users/signin
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### 3. Research Startups
```http
POST /agent/query
Content-Type: application/json

{
  "query": "YC startups building AI tools for developers"
}
```

**Response:**
```json
{
  "query": "YC startups building AI tools for developers",
  "companies": [
    {
      "name": "Example AI Inc",
      "founded_year": "2023",
      "founders": "Jane Doe, John Smith",
      "website": "https://example-ai.com",
      "description": "AI-powered developer tools platform",
      "tech_stack": "Python, React, TensorFlow",
      "funding_info": "Seed - $2M",
      "yc_batch": "W24"
    }
  ],
  "report": "Query: YC startups building AI tools for developers\nCompanies Found: 1\n\n..."
}
```

## 📁 Project Structure
```
.
├── agent/
│   └── research_agent.py      # Core LangGraph workflow
├── models/
│   └── user.py                # MongoDB user model
├── routes/
│   ├── user.py                # User authentication routes
│   └── query.py               # Research query routes
├── schema/
│   └── user.py                # Pydantic schemas
├── database.py                # MongoDB connection setup
├── main.py                    # FastAPI application entry point
├── .env                       # Environment variables (not in repo)
├── .gitignore
└── requirements.txt
```

## 🔍 How It Works

### 1. Query Refinement
The agent analyzes your natural language query and creates an optimized search query targeting:
- Startup names and official websites
- Founder information
- Company descriptions and products
- Technology stack details
- Funding and batch information

### 2. Web Search
Uses Exa API to search for relevant startup information with:
- Top 5 results per query
- Text content extraction
- Highlighted relevant passages

### 3. Data Extraction
Google Gemini parses search results into structured company profiles using Pydantic models for type safety and validation.

### 4. Report Generation
Creates a formatted text report with all discovered companies and their details.

## 🔐 Security Features

- Password hashing with bcrypt
- Email validation with Pydantic
- MongoDB document-level security
- Environment variable protection for API keys

## 📊 Example Queries
```
"Find Y Combinator startups in the AI space from 2024"
"Startups building developer tools with Python and React"
"Companies in fintech that raised Series A in 2023"
"AI startups founded by ex-Google engineers"
```


---
