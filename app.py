from openai import OpenAI
from dotenv import load_dotenv, get_key, find_dotenv
import requests

load_dotenv()
dotenv_path = find_dotenv()

def main():
    openai_key = get_key(dotenv_path, 'OPENAI_KEY')
    client = OpenAI(api_key=openai_key)

    response = extract_keywords(client)
    response = f"isDeleted:0  AND ({response.choices[0].message.content}) AND NOT status:Archive"
    print('Lucene Search: ', response)

    candidates = bullhorn_response(response)
    
    print(candidates)

def extract_keywords(client):
    prompt = open("prompts/create-lucene.txt").read()
    prompt += open("data/posting.txt").read()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a reliable bot who responds with clear, quick answers."},
            {"role": "user", "content": prompt},
        ],
        temperature = 0.1
    )
    return response

def bullhorn_response(query):
    try:
        rest_url = get_key(dotenv_path, 'BH_REST_URL')
        rest_token = get_key(dotenv_path, 'BH_REST_TOKEN')
        url = f"{rest_url}search/Candidate?BhRestToken={rest_token}&fields=id,dateAdded,name"

        body = {
            "query": query
        }

        response = requests.post(url, json=body)
        response.raise_for_status()
        print('Request was successful')
        print('Response content:', response.text)
        return response
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # HTTP error (e.g., 400, 401, 403, 404, 500, etc.)
        print('Response content:', response.text)  # Response content might give more information
    except Exception as err:
        print(f'Other error occurred: {err}')  # Non-HTTP error (e.g., network problem)
    
if __name__ == "__main__":
    main()