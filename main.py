from src.agent import FinancialNewsAgent
import os
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load environment variables from .env file
    
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        return
    agent = FinancialNewsAgent(api_key=os.getenv('OPENAI_API_KEY'))

    # Financial News Analysis
    analysis, total_input_tokens, total_output_tokens = agent.analyze_financial_news()
    print(f"Analysis complete. Total Input Tokens: {total_input_tokens}, Total Output Tokens: {total_output_tokens}")

    # Generate HTML Report
    html_report, total_input_tokens, total_output_tokens = agent.generate_html_report(analysis)
    print(f"{html_report}. Total Input Tokens: {total_input_tokens}, Total Output Tokens: {total_output_tokens}")

if __name__ == "__main__":
    main()
