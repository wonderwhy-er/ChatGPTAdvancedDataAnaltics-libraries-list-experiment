
import requests
from bs4 import BeautifulSoup
import json

def fetch_github_readme_content(package_name):
    # The base URL for the PyPi package
    base_url = f"https://pypi.org/project/{package_name}/"
    
    try:
        # Fetch content from PyPi
        response = requests.get(base_url)
        print(f"Request to {base_url} returned status code {response.status_code}")
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all anchor links
        all_links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # Identify GitHub link from the PyPi page
        github_link = next((link for link in all_links if 'github.com' in link), None)
        
        if github_link:
            # Fetch content from GitHub repository main page
            github_response = requests.get(github_link)
            github_soup = BeautifulSoup(github_response.content, 'html.parser')
            
            # Locate the element with id 'readme'
            readme_content = github_soup.find(id='readme')
            
            if readme_content:
                return readme_content.get_text()
            else:
                print(f"README content not found on the GitHub page for {package_name}.")
                return None
        else:
            print(f"GitHub link not found on the PyPi page for {package_name}.")
            return None
    except Exception as e:
        print(f"Error fetching README for {package_name}. Error: {e}")
        return None

# Load the initial JSON
with open('installed_libraries.json', 'r') as f:
    libraries_data = json.load(f)

# Iterate over libraries and fetch READMEs
for library in libraries_data:
    if not library["readme"]:
        print(f"Fetching README for {library['name']}...")
        library["readme"] = fetch_github_readme_content(library["name"]) or ""
        
        # Save the updated JSON
        with open('installed_libraries.json', 'w') as f:
            json.dump(libraries_data, f, indent=4)

print("Process completed!")
