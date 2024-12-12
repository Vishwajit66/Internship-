import requests

def fetch_google_results(query):
    google_api_key = 'AIzaSyAnlkwEZq2Ut_lFNSeshyRStrLpvEZb0kU'
    google_search_engine_id = '71ea9a1b1dd854cc3'
    google_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_search_engine_id}&q={query}"

    response = requests.get(google_url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return None

# Example usage:
user_query = input("Enter your query: ")
search_results = fetch_google_results(user_query)

if search_results:
    for index, item in enumerate(search_results, start=1):
        print(f"Result {index}:")
        print(f"Title: {item.get('title')}")
        print(f"Link: {item.get('link')}")
        print(f"Snippet: {item.get('snippet')}")
        print()
else:
    print("Failed to retrieve search results.")