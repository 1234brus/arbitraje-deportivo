import requests

API_KEY = "92e3f3b0307def524c27714e1e3761a2"

def obtener_cuotas():
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?apiKey={API_KEY}&regions=eu&markets=h2h&oddsFormat=decimal"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return response.json()
