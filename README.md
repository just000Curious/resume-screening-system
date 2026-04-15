# AI Resume Screening System

## Overview
An AI-powered resume screening system that evaluates candidates against job descriptions using LangChain and LangSmith. The system automatically extracts skills, analyzes requirements, and generates detailed scoring reports.

## Features
- ✅ Skill extraction from resumes
- ✅ Job requirement analysis
- ✅ Automated scoring (0-100)
- ✅ Explainable AI outputs with reasoning
- ✅ LangSmith tracing for debugging
- ✅ Modular pipeline architecture
- ✅ JSON output for integration

## Prerequisites
- Python 3.9+
- OpenAI API key
- LangSmith API key (optional, for tracing)

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install langchain-core langchain-openai python-dotenv
```

## Configuration

### 1. Create `.env` File
Create a `.env` file in the project root and add your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LangSmith Configuration (Optional)
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=resume_screening_system
```

### 2. Add Sample Data
The system comes with sample candidates in the `data/` folder:
- `job_description.txt` - Target job requirements
- `strong_candidate.txt` - High-performing candidate
- `average_candidate.txt` - Mid-range candidate
- `weak_candidate.txt` - Poor-fit candidate

You can modify these files or add your own candidates.

## Running the Application

### Option 1: Run with Virtual Environment (Recommended)
```bash
# Activate venv (if not already activated)
.\venv\Scripts\Activate.ps1

# Run the application
python main.py
```

### Option 2: Run with Explicit Python Path
```bash
.\venv\Scripts\python.exe main.py
```

## Output

After running, the system generates:

1. **Console Output** - Real-time progress and results with color-coded scores
2. **JSON Results** - Individual result files for each candidate
   - `results_Strong_Candidate_TIMESTAMP.json`
   - `results_Average_Candidate_TIMESTAMP.json`
   - `results_Weak_Candidate_TIMESTAMP.json`
3. **Summary Report** - `summary_TIMESTAMP.json` with overall analysis

### Sample Output Format
```json
{
  "total_score": 85,
  "breakdown": {
    "technical_skills": {
      "score": 90,
      "weight": 40,
      "reasoning": "All required Python, SQL, AWS skills present"
    },
    "experience": {
      "score": 75,
      "weight": 30,
      "reasoning": "5 years experience meets 3+ year requirement"
    },
    "tools": {...},
    "education": {...}
  },
  "strengths": ["Strong Python background", "AWS experience"],
  "gaps": ["Missing Docker experience"],
  "recommendation": "Hire"
}
```

## Project Structure
```
resume-screening-system/
├── main.py                      # Main entry point
├── README.md                    # This file
├── requirements.txt             # Dependencies list
├── .env                         # API keys (not in git)
├── venv/                        # Virtual environment
├── chains/
│   ├── __init__.py
│   └── screening_chains.py      # LangChain screening pipeline
├── prompts/
│   ├── __init__.py
│   └── resume_prompts.py        # LLM prompt templates
└── data/
    ├── job_description.txt      # Target job requirements
    ├── strong_candidate.txt     # Sample candidates
    ├── average_candidate.txt
    └── weak_candidate.txt
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langchain'`
**Solution:** Make sure the virtual environment is activated and dependencies are installed.
```bash
.\venv\Scripts\Activate.ps1
pip install langchain-core langchain-openai python-dotenv
```

### Issue: `OPENAI_API_KEY not found`
**Solution:** Ensure `.env` file exists in the project root with valid API key.

### Issue: `403 Forbidden` from LangSmith
**Solution:** Your LangSmith API key may be invalid. You can disable tracing by removing LangSmith configuration from `.env`.

## Dependencies
- **langchain-core** - LangChain core library for building LLM chains
- **langchain-openai** - OpenAI integration for LangChain
- **python-dotenv** - Environment variable management
