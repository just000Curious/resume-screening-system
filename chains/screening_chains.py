"""LangChain chains for resume screening"""

import json
from typing import Dict, Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from prompts.resume_prompts import (
    skill_extraction_prompt,
    job_requirements_prompt,
    matching_scoring_prompt
)

class ResumeScreeningChain:
    """Main chain for resume screening system"""
    
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0):
        """Initialize the chain with LLM"""
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            tags=["resume_screening"]  # LangSmith tags
        )
        
        # Create individual chains
        self.skill_extraction_chain = (
            skill_extraction_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        self.job_requirements_chain = (
            job_requirements_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        self.matching_scoring_chain = (
            matching_scoring_prompt 
            | self.llm 
            | StrOutputParser()
        )
    
    def extract_skills(self, resume_text: str) -> str:
        """Extract skills from resume"""
        with_tags = {"tags": ["skill_extraction"]}
        return self.skill_extraction_chain.invoke(
            {"resume_text": resume_text},
            config=with_tags
        )
    
    def extract_requirements(self, job_description: str) -> str:
        """Extract requirements from job description"""
        with_tags = {"tags": ["job_requirements"]}
        return self.job_requirements_chain.invoke(
            {"job_description": job_description},
            config=with_tags
        )
    
    def match_and_score(self, extracted_skills: str, job_requirements: str) -> str:
        """Match candidate skills with job requirements and generate score"""
        with_tags = {"tags": ["matching_scoring"]}
        return self.matching_scoring_chain.invoke(
            {
                "extracted_skills": extracted_skills,
                "job_requirements": job_requirements
            },
            config=with_tags
        )
    
    def screen_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Complete screening pipeline"""
        try:
            # Step 1: Extract job requirements
            print("📋 Extracting job requirements...")
            job_requirements = self.extract_requirements(job_description)
            
            # Step 2: Extract skills from resume
            print("🔍 Extracting skills from resume...")
            extracted_skills = self.extract_skills(resume_text)
            
            # Step 3: Match and score
            print("⚖️ Matching and scoring...")
            result = self.match_and_score(extracted_skills, job_requirements)
            
            # Parse JSON result
            try:
                # Extract JSON from the response
                result = result.strip()
                # Handle potential markdown code blocks
                if result.startswith("```json"):
                    result = result[7:]
                if result.startswith("```"):
                    result = result[3:]
                if result.endswith("```"):
                    result = result[:-3]
                
                result_json = json.loads(result.strip())
                return result_json
            except json.JSONDecodeError as e:
                # Fallback if JSON parsing fails
                return {
                    "total_score": 50,
                    "explanation": f"Error parsing result: {str(e)}. Raw output: {result}",
                    "recommendation": "Manual review required"
                }
                
        except Exception as e:
            return {
                "total_score": 0,
                "explanation": f"Error in screening pipeline: {str(e)}",
                "recommendation": "Error - needs manual review"
            }

def create_screening_chain():
    """Factory function to create screening chain"""
    return ResumeScreeningChain()