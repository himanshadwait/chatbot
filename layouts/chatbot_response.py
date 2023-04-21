import requests
import logging


def fetch_chatbot_response(character, question, character_history):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": f"{character['prompt']}"}] + character_history + [
            {"role": "user", "content": f"Q: {question}\n"}],
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        completion = response_data["choices"][0]["message"]["content"].strip()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        logging.error(f"Error while making the API request: {e}\n")
        completion = f"Error while making the API request for {character['name']}. Please try again later."
    return character, completion
