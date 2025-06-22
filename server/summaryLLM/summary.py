import anthropic
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = anthropic.Anthropic(
  api_key=os.getenv("ANTHROPIC_API_KEY"),
)

header = """
You are analyzing layoff risk for companies. You'll receive a risk_level (0 - 100 scale) and company features.

Your task: Provide a 2-3 sentence justification explaining WHY this risk_level makes sense based on the features.

Features available: funding_raised, layoff_count, type_of_company, country, industry, company_name, additional_info

Note that not all features are available for all companies.

Guidelines:
- If risk_level is 0-30: emphasize stability factors
- If risk_level is 30-70: mention mixed signals 
- If risk_level is 70-100: highlight concerning indicators
- Be conservative - don't overstate beyond what the data suggests
- If key features are missing, mention this limits the analysis

Format: "Based on [specific features], the risk level of X.X appears reasonable because [reasoning]."
"""

def summerize(risk_level, features):
    information = f"Risk level: {risk_level}\nFeatures: {features}"
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

print(summerize(50, """
company_name: Oda Oslo Food
layoff_count: 150
funding_raised: 691.0 million
country: Norway
type_of_company: Food delivery/grocery
industry: Food & Beverage
additional_info: Layoff date: 2024-06-05
"""))