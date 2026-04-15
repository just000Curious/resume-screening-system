"""Main script for AI Resume Screening System"""

import os
from dotenv import load_dotenv
from chains.screening_chains import ResumeScreeningChain
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# LangSmith configuration - MANDATORY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")  # Set this in .env
os.environ["LANGCHAIN_PROJECT"] = "resume_screening_system"

# OpenAI configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # Set this in .env

def load_file(filepath):
    """Load text from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

def save_results(results, candidate_name):
    """Save screening results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results_{candidate_name}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to {filename}")

def print_results(results, candidate_name):
    """Pretty print screening results"""
    print("\n" + "="*60)
    print(f"📊 SCREENING RESULTS: {candidate_name}")
    print("="*60)
    
    if "total_score" in results:
        score = results["total_score"]
        # Color coding for score
        if score >= 70:
            status = "🟢 STRONG CANDIDATE"
        elif score >= 50:
            status = "🟡 AVERAGE CANDIDATE"
        else:
            status = "🔴 WEAK CANDIDATE"
        
        print(f"\n📈 Total Score: {score}/100")
        print(f"🎯 Status: {status}")
        
        if "breakdown" in results:
            print("\n📋 Score Breakdown:")
            for category, data in results["breakdown"].items():
                print(f"  • {category.replace('_', ' ').title()}: {data.get('score', 'N/A')}/100")
                if "reasoning" in data:
                    print(f"    Reasoning: {data['reasoning']}")
        
        if "explanation" in results:
            print(f"\n💡 Explanation:\n{results['explanation']}")
        
        if "strengths" in results and results["strengths"]:
            print("\n✅ Strengths:")
            for strength in results["strengths"]:
                print(f"  • {strength}")
        
        if "gaps" in results and results["gaps"]:
            print("\n⚠️ Gaps:")
            for gap in results["gaps"]:
                print(f"  • {gap}")
        
        if "recommendation" in results:
            print(f"\n🎯 Recommendation: {results['recommendation']}")
    
    print("="*60 + "\n")

def main():
    """Main execution function"""
    print("🚀 AI Resume Screening System Started")
    print("="*50)
    
    # Load job description
    print("\n📄 Loading job description...")
    job_description = load_file("data/job_description.txt")
    if not job_description:
        print("❌ Job description not found!")
        return
    
    # Load resumes
    resumes = {
        "Strong_Candidate": load_file("data/strong_candidate.txt"),
        "Average_Candidate": load_file("data/average_candidate.txt"),
        "Weak_Candidate": load_file("data/weak_candidate.txt")
    }
    
    # Check if all resumes loaded
    for name, content in resumes.items():
        if not content:
            print(f"❌ {name} resume not found!")
            return
    
    # Initialize screening system
    print("\n🔧 Initializing screening system...")
    screener = ResumeScreeningChain()
    
    # Process each resume
    all_results = {}
    
    for candidate_name, resume_text in resumes.items():
        print(f"\n{'='*50}")
        print(f"📝 Processing {candidate_name}...")
        print(f"{'='*50}")
        
        try:
            # Run screening pipeline
            result = screener.screen_resume(resume_text, job_description)
            
            # Store results
            all_results[candidate_name] = result
            
            # Print results
            print_results(result, candidate_name)
            
            # Save individual results
            save_results(result, candidate_name)
            
        except Exception as e:
            print(f"❌ Error processing {candidate_name}: {str(e)}")
            error_result = {
                "total_score": 0,
                "explanation": f"Processing error: {str(e)}",
                "recommendation": "Error - needs investigation"
            }
            all_results[candidate_name] = error_result
            save_results(error_result, f"{candidate_name}_ERROR")
    
    # Summary report
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY REPORT")
    print("="*60)
    
    summary = []
    for candidate, result in all_results.items():
        score = result.get("total_score", 0)
        recommendation = result.get("recommendation", "Unknown")
        summary.append({
            "candidate": candidate,
            "score": score,
            "recommendation": recommendation
        })
    
    # Sort by score
    summary.sort(key=lambda x: x["score"], reverse=True)
    
    print("\nRanking:")
    for idx, item in enumerate(summary, 1):
        print(f"{idx}. {item['candidate']}: {item['score']}/100 - {item['recommendation']}")
    
    # Determine best candidate
    if summary:
        best = summary[0]
        print(f"\n🏆 Best Candidate: {best['candidate']} with score {best['score']}/100")
    
    print("\n✅ Screening completed!")
    print("\n📌 LangSmith Tracing:")
    print("   Check your LangSmith dashboard for detailed traces of all 3 runs")
    print("   Each run shows all pipeline steps: skill extraction → matching → scoring → explanation")
    
    # Save complete summary
    summary_file = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": all_results,
            "ranking": summary
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete summary saved to: {summary_file}")
    print("="*60)

if __name__ == "__main__":
    main()