# translate/translator.py

import re
import requests
from config import API_KEY


def is_number(token):
    return re.fullmatch(r'[+-]?(\d+(\.\d+)?|\.\d+)', token) is not None


def preserve_numbers_translate(text, target_lang):
    tokens = text.split()
    translated_tokens = []

    for token in tokens:
        if is_number(token) or re.fullmatch(r'₹?\d+(,\d{3})*(\.\d{1,2})?', token):  # match rupee values
            translated_tokens.append(token)
        else:
            resp = requests.post(
                f"https://translation.googleapis.com/language/translate/v2",
                params={
                    "q": token,
                    "target": target_lang,
                    "format": "text",
                    "key": API_KEY
                }
            )
            try:
                translated_token = resp.json()['data']['translations'][0]['translatedText']
            except:
                translated_token = token
            translated_tokens.append(translated_token)

    return ' '.join(translated_tokens)
