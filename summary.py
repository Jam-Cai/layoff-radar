import anthropic
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = anthropic.Anthropic(
  api_key=os.getenv("CLAUDE_KEY"),
)

header = """
You are analyzing layoff risk for companies. You'll receive a risk_level (0 - 100 scale), company features, context about the comapny and industry, and 3 key points about the company with an impact, with more positive meaning more contributing to layoffs.

Your task: Provide a 2-3 sentence justification explaining WHY this risk_level makes sense based on the features and context.

Features available: funding_raised, layoff_count, type_of_company, country, industry, company_name, additional_info

Note that not all features are available for all companies.

Do NOT repeat the features, values of features, or risk level you are given. Explain as if the user has not seen the data you have seen. Provide insightful and non-superficial analysis."
"""

def get_summary(risk_level, features, context, key_points):
    information = f"Risk level: {risk_level}\nFeatures: {features}\nContext: {context}\nKey Points: {key_points}"
    message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    temperature=1,
    system=header,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": information
                }
            ]
        }
    ]
    )
    return message.content[0].text