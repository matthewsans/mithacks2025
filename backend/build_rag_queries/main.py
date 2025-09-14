from backend.build_rag_queries.break_into_questions import break_down_financial_question
import time

API_KEY = "gk-lg2FEI1z_oknwrbbbuya"

def break_down_mock(user_question: str):
    """Mock version that provides sample financial questions without API call"""
    print("Using mock data to bypass API timeout...")
    
    # Sample financial questions based on the user input
    if "apple" in user_question.lower() and "google" in user_question.lower():
        sub_questions = [
            "What is Apple's total revenue for the most recent fiscal year?",
            "What is Google's total revenue for the most recent fiscal year?", 
            "What is Apple's net income margin?",
            "What is Google's net income margin?",
            "What is Apple's research and development spending?",
            "What is Google's research and development spending?",
            "What is Apple's market capitalization?",
            "What is Google's market capitalization?",
            "What is Apple's debt-to-equity ratio?",
            "What is Google's debt-to-equity ratio?"
        ]
    else:
        # Generic financial questions
        sub_questions = [
            "What is the company's total revenue?",
            "What is the company's net income?",
            "What is the company's profit margin?",
            "What is the company's revenue growth rate?",
            "What is the company's research and development spending?",
            "What is the company's market capitalization?",
            "What is the company's debt-to-equity ratio?",
            "What is the company's return on equity?",
            "What is the company's current ratio?",
            "What is the company's earnings per share?"
        ]
    
    for i, q in enumerate(sub_questions, 1):
        print(f"{i}. {q}")

    return sub_questions

def break_down(user_question: str):
    """Main function that tries API first, falls back to mock on timeout"""
    try:
        print("Attempting to use Tandem API...")
        sub_questions = break_down_financial_question(user_question, API_KEY)
        
        for i, q in enumerate(sub_questions, 1):
            print(f"{i}. {q}")
        
        return sub_questions
        
    except Exception as e:
        print(f"API call failed: {e}")
        print("Falling back to mock data...")
        return break_down_mock(user_question)