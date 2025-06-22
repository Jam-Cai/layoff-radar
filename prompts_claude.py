from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def fix_json(json_string):
    response = client.messages.create(
        model="claude-sonnet-4-20250514", 
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
        model="claude-sonnet-4-20250514", 
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
                    f"Summarize the major points about {company} in the following news articles. Output 4-5 sentences. "
                    f"Article:\n\n {articles_text}"
                )
            },
        ]
    )

    return response.content[0].text

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
                    f"Extract the structured data about {company_name} from the article. Respond ONLY with a JSON object matching the prefilled format.\n"
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
        model="claude-sonnet-4-20250514", 
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
                    "Use common sense and consistency when merging. Ensure the result uses the same structure:\n\n"
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