"""Prompt templates for resume screening system"""

from langchain_core.prompts import PromptTemplate

# Skill Extraction Prompt
skill_extraction_template = """
You are an expert HR analyst. Extract skills, experience, and tools from the following resume.

CRITICAL RULES:
1. ONLY extract information that is EXPLICITLY mentioned in the resume
2. Do NOT assume or hallucinate any skills not present
3. If information is not available, mark it as "Not specified"
4. Be precise and factual

Resume:
{resume_text}

Extract the following in JSON format:
{{
    "technical_skills": ["list of programming languages, frameworks, and technical skills"],
    "soft_skills": ["list of soft skills mentioned"],
    "experience_years": "number of years (if mentioned)",
    "tools": ["list of tools, software, platforms"],
    "education": "highest degree mentioned",
    "certifications": ["list of certifications"]
}}

Extraction:
"""

skill_extraction_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=skill_extraction_template
)

# Job Requirements Extraction Prompt
job_requirements_template = """
You are an expert HR analyst. Extract key requirements from the following job description.

CRITICAL RULES:
1. Extract requirements EXACTLY as stated
2. Categorize by importance (required vs preferred)
3. Be specific and accurate

Job Description:
{job_description}

Extract in JSON format:
{{
    "required_skills": ["must-have skills"],
    "preferred_skills": ["nice-to-have skills"],
    "min_experience": "minimum years required",
    "required_tools": ["tools mentioned as required"],
    "education_requirement": "minimum education needed"
}}

Extraction:
"""

job_requirements_prompt = PromptTemplate(
    input_variables=["job_description"],
    template=job_requirements_template
)

# Matching and Scoring Prompt
matching_scoring_template = """
You are an AI resume screening system. Compare the candidate's extracted information with job requirements.

Candidate Data:
{extracted_skills}

Job Requirements:
{job_requirements}

CRITICAL RULES:
1. Score based ONLY on the extracted information
2. Do NOT assume any missing information
3. Provide detailed reasoning for each scoring decision
4. Score breakdown:
   - 90-100: Excellent match (exceeds or meets all requirements)
   - 70-89: Good match (meets most requirements)
   - 50-69: Average match (meets some requirements)
   - 30-49: Below average (meets few requirements)
   - 0-29: Poor match (meets almost no requirements)

Calculate match scores for:
1. Technical Skills Match (weight: 40%)
2. Experience Match (weight: 30%)
3. Tools Match (weight: 20%)
4. Education Match (weight: 10%)

Output MUST be in this JSON format:
{{
    "total_score": "number between 0-100",
    "breakdown": {{
        "technical_skills": {{
            "score": "number",
            "weight": 40,
            "reasoning": "explanation"
        }},
        "experience": {{
            "score": "number",
            "weight": 30,
            "reasoning": "explanation"
        }},
        "tools": {{
            "score": "number",
            "weight": 20,
            "reasoning": "explanation"
        }},
        "education": {{
            "score": "number",
            "weight": 10,
            "reasoning": "explanation"
        }}
    }},
    "explanation": "Overall reasoning for the total score",
    "strengths": ["list of strong matches"],
    "gaps": ["list of missing requirements"],
    "recommendation": "Hire/Interview/Reject based on score"
}}

Scoring:
"""

matching_scoring_prompt = PromptTemplate(
    input_variables=["extracted_skills", "job_requirements"],
    template=matching_scoring_template
)

# Few-shot examples for better performance
few_shot_examples = """
Example 1:
Candidate: Python, SQL, Machine Learning, 5 years experience
Job: Python, SQL, Deep Learning, 3+ years
Score: 75 (Good match - missing Deep Learning but exceeds experience)

Example 2:
Candidate: Excel, PowerPoint, 1 year experience
Job: Python, SQL, Machine Learning, 3+ years
Score: 15 (Poor match - major skill gaps)

Example 3:
Candidate: Python, SQL, AWS, Deep Learning, 4 years
Job: Python, SQL, AWS, Machine Learning, 3+ years
Score: 90 (Excellent match - meets all requirements)
"""