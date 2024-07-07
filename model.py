import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

def get_search_element_info(search_element):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query': search_element,
        'key': api_key,
        'limit': 1,
        'indent': True,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error fetching data from API: {response.status_code}, {response.text}"}

def extract_element_info(data):
    element_info = data.get('itemListElement', [])
    if element_info:
        element = element_info[0].get('result', {})
        name = element.get('name', 'N/A')
        description = element.get('description', 'N/A')
        url = element.get('detailedDescription', {}).get('url', 'N/A')
        biography = element.get('detailedDescription', {}).get('articleBody', 'N/A')
        
        contact_info = []
        if 'address' in element:
            address = element['address']
            contact_info.append(f"Address: {address.get('addressLocality', 'N/A')}, {address.get('addressRegion', 'N/A')} {address.get('postalCode', 'N/A')}")
        
        if 'contactPoint' in element:
            for contact_point in element['contactPoint']:
                contact_info.append(f"{contact_point.get('contactType', 'N/A')}: {contact_point.get('email', 'N/A')} (Email), {contact_point.get('telephone', 'N/A')} (Phone)")
        
        return {
            "name": name,
            "description": description,
            "url": url,
            "biography": biography,
            "contact_info": contact_info
        }
    return {"error": "No information found for the search element."}
