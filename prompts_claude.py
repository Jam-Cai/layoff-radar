from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def fix_json(json_string):
    response = client.messages.create(
        model="claude-3-5-haiku-20241022", 
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract the string mentioned as structured data. Respond ONLY with a JSON object. "
                    f"This string meant to be a json object, but it couldn't be converted to a json object. "
                    f"Please return a proper json string of {json_string}"
                )
            },
        ]
    )

    try:
        return json.loads(response.content[0].text)
    except Exception as e:
        print("Failed to parse response:", e)
        return {"error": str(e), "raw": response.content[0].text} 

def extract_companies(article_text):
    response = client.messages.create(
        model="claude-3-5-haiku-20241022", 
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the companies mentioned in the articles as structured data. "
                    "Respond ONLY with a JSON object matching the prefilled format."
                )
            },
            {
                "role": "assistant",
                "content": '''{
                "company_names": []
                }'''
            },
            {
                "role": "user",
                "content": f"Here is the article:\n\n{article_text}"
            }
        ]
    )

    try:
        return json.loads(response.content[0].text)
    except Exception as e:
        print("Failed to parse response:", e)
        return {"error": str(e), "raw": response.content[0].text}

def summarize_articles(articles_text, company):
    response = client.messages.create(
        model="claude-sonnet-4-20250514", 
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract the structured data about {company} from the articles. Respond ONLY with a JSON object matching the prefilled format.\n"
                    f"summary: Summarize the major points about {company} in the following news articles. Output 4-5 sentences.\n"
                    f"key_points: Identify the top 3 factors about the company that contribute to the risk_level. Be as specific as possible, avoid general phrases. Have a mix between positive and negative. They must NOT be names of products. They must be 1-3 words. Output a JSON list\n"
                    f"impact: For each key_point, assign a number from -60 (strongly preventing layoffs) to 60 (strongly causing layoffs), based on how it likely influences layoffs. MUST be a JSON list\n"
                    "You MUST include at least one negative number, try to include more. Make up negative factors."
                    "A positive number means the factor increases the chance of layoffs. (e.g., 'revenue decline': 45).\n"
                    "A negative number means it reduces the risk of layoffs, (e.g., 'new funding': -30 or 'defense collaboration': -20).\n" 
                    "Do not assign positive values to factors that help the company grow or expand.\n"       
                    "Use your judgment, and be consistent with the meaning of the numbers.\n"
                ),
            },
            {
                "role": "assistant",
                "content": '''{
                    "summary": "",
                    "key_points": [],
                    "impact": [],
                }'''
            },
            {
                "role": "user",
                "content": f"Extract: \n\n{articles_text}"
            }
        ]
    )

    try:
        return json.loads(response.content[0].text)
    except Exception as e:
        return fix_json(response.content[0].text)
        

def extract_features(company_name, article):
    # class Features(BaseModel):
    #     Location_HQ: str
    #     Industry: str
    #     Stage: str
    #     Year: int
    #     log10_Funds_Raised: int

    response = client.messages.create(
        model="claude-sonnet-4-20250514", 
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract the structured data about {company_name} from the articles. Respond ONLY with a JSON object matching the prefilled format.\n"
                    f"Use the following context to answer the query:\n"
                    f"If information is not avalible for any of these, leave them as an empty string\n"
                    f"Location_HQ: where the company is headquatered, must be a string\n"
                    f"Industry: the industry that the company is in\n"
                    f"Stage: One of the following based on funding stage:\n"
                    f"  - A: Focuses on optimizing the product and market fit\n"
                    f"  - B: Strong growth, expanding team and market reach, building business infrastructure.\n"
                    f"  - C: Large-scale expansion, entering new markets, launching new products, possible acquisitions.\n"
                    f"  - D: Late stage, often pre-IPO, used for strategic pivots, down rounds, or final growth pushes.\n"
                    f"  - Private: Company is privately owned\n"
                    f"  - Post-IPO: The company is already publicly traded on a stock exchange.\n\n"
                    f"Year: The year that the events of the article took place. must be a single integer or empty\n"
                    f"log10_Funds_Raised: How much money the company raised after log 10. must be a single integer or empty"
                )
            },
            {
                "role": "assistant",
                "content": '''{
                    "Location_HQ": "",
                    "funding_raised": "",
                    "type_of_company": "",
                    "country": "",
                    "industry": ""
                }'''
            },
            {
                "role": "user",
                "content": f"Extract: \n\n{article}"
            }
        ]
    )

    return response.content[0].text

def combine_features(features_list):
    joined_features = "\n".join(features_list)

    response = client.messages.create(
        model="claude-3-5-haiku-20241022", 
        max_tokens=1024,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the structured data by consolidating information from multiple news articles. "
                    "Respond ONLY with a JSON object matching the prefilled format. Year and log10_Funds_Raised MUST be integers. "
                    "If log10_Funds_Raised is empty, make it 0."
                    "Each article has extracted features in the following JSON format:\n\n"
                    "{\n"
                    '  "Location_HQ": "",\n'
                    '  "Industry": "",\n'
                    '  "Stage": "",\n'
                    '  "Year": "",\n'
                    '  "log10_Funds_Raised": ""\n'
                    "}\n\n"
                    "Below is a list of these JSON objects from different articles. Your job is to analyze them and generate a single, best-estimate JSON object for the company. "
                    "If most entries are blank, infer reasonable values based on the ones that have data. For ambiguous or conflicting values, choose the most frequently occurring or most complete value. "
                    "Use common sense and consistency when merging. log10_Funds_Raised and Year MUST be integers, enter 0 only if entirely unsure. Ensure the result uses the same structure:\n\n"
                    "{\n"
                    '  "Location_HQ": "",\n'
                    '  "Industry": "",\n'
                    '  "Stage": "",\n'
                    '  "Year": "",\n'
                    '  "log10_Funds_Raised": ""\n'
                    "}\n\n")
            },
            {
                "role": "assistant",
                "content": '''{
                    "Location_HQ": "",
                    "Industry": "",
                    "Stage": "",
                    "Year": "",
                    "log10_Funds_Raised": ""
                }'''
            },
            {
                "role": "user",
                "content": f"Here are the features: \n\n{joined_features}"
            }
        ]
    )

    try:
        return json.loads(response.content[0].text)
    except Exception as e:
        return fix_json(response.content[0].text)
    
