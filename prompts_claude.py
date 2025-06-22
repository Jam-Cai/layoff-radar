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

def extract_features(company_name, article):
    # Features:
	# 	company_name (done)
	# 	layoff_count
	# 	funding_raised
	# 	type of company (stage)
	# 	country
	# 	industry

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
                    f"layoff_count: how many people were laid off recently. must be an integer or empty\n"
                    f"funding_raised: must be an integer or empty. how much funding the company recieved from venture captial\n"
                    f"type_of_company: One of the following based on funding stage:\n"
                    f"  - Series B: Strong growth, expanding team and market reach, building business infrastructure.\n"
                    f"  - Series C: Large-scale expansion, entering new markets, launching new products, possible acquisitions.\n"
                    f"  - Series D: Late stage, often pre-IPO, used for strategic pivots, down rounds, or final growth pushes.\n"
                    f"  - Post-IPO: The company is already publicly traded on a stock exchange.\n\n"
                    f"country: the location that the news article is talking about, may be diffe3rent than the location_hq"
                    f"industry: what industry the company is in"
                )
            },
            {
                "role": "assistant",
                "content": '''{
                    "layoff_count": "",
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
                    "Respond ONLY with a JSON object matching the prefilled format. layoff_count and funding_raised MUST be integers"
                    "Each article has extracted features in the following JSON format:\n\n"
                    "{\n"
                    '  "layoff_count": "",\n'
                    '  "funding_raised": "",\n'
                    '  "type_of_company": "",\n'
                    '  "country": "",\n'
                    '  "industry": ""\n'
                    "}\n\n"
                    "Below is a list of these JSON objects from different articles. Your job is to analyze them and generate a single, best-estimate JSON object for the company. "
                    "If most entries are blank, infer reasonable values based on the ones that have data. For ambiguous or conflicting values, choose the most frequently occurring or most complete value. "
                    "Use common sense and consistency when merging. Ensure the result uses the same structure:\n\n"
                    "{\n"
                    '  "layoff_count": "",\n'
                    '  "funding_raised": "",\n'
                    '  "type_of_company": "",\n'
                    '  "country": "",\n'
                    '  "industry": ""\n'
                    "}\n\n")
            },
            {
                "role": "assistant",
                "content": '''{
                    "layoff_count": "",
                    "funding_raised": "",
                    "type_of_company": "",
                    "country": "",
                    "industry": ""
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