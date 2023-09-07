
import requests
from bs4 import BeautifulSoup
import json

def fetch_pypi_project_description(package_name):
    # The base URL for the PyPi package
    base_url = f"https://pypi.org/project/{package_name}/"
    
    try:
        # Fetch content from PyPi
        response = requests.get(base_url)
        print(f"Request to {base_url} returned status code {response.status_code}")
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the project description content
        description_content = soup.find(class_='project-description')
        
        if description_content:
            return description_content.get_text()
        else:
            print(f"Project description not found on the PyPi page for {package_name}.")
            return None
    except Exception as e:
        print(f"Error fetching project description for {package_name}. Error: {e}")
        return None

# Load the initial JSON
with open('installed_libraries.json', 'r') as f:
    libraries_data = json.load(f)

# Iterate over libraries and fetch project descriptions
for library in libraries_data:
    if not library["readme"]:
        print(f"Fetching project description for {library['name']}...")
        library["readme"] = fetch_pypi_project_description(library["name"]) or ""
        
        # Save the updated JSON
        with open('installed_libraries.json', 'w') as f:
            json.dump(libraries_data, f, indent=4)

print("Process completed!")
