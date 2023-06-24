import requests


def translate_text(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": "ru",
        "dt": "t",
        "q": text
    }
    response = requests.get(url, params=params)
    data = response.json()
    translated_text = data[0][0][0]
    return translated_text
