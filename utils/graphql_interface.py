import requests
from pathlib import Path

def run_anilist_query(query: str, variables: dict | None) -> dict:
    url = "https://graphql.anilist.co"

    payload: dict[str, str | dict] = {
        "query": query
    }
    if variables:
        payload["variables"] = variables

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json = payload, headers = headers)

        response.raise_for_status() 
        
        result = response.json()

        if "errors" in result:
            print(f"graphql syntax error: {result['errors']}")

            assert(False)
            
        return result.get("data")
    
    except requests.exceptions.RequestException as err:
        print(f"network connection failed: {err}")

        assert(False)
    
def get_query_from_file_path(relative_file_path: str) -> str:
    project_root = Path(__file__).parent.parent

    file_path = project_root / relative_file_path

    with open(file_path, 'r') as file:
        file_content = file.read()

    return file_content