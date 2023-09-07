import requests
from bs4 import BeautifulSoup

def fetch_github_readme_content():
    # The base URL for the PyPi package
    base_url = "https://pypi.org/project/CairoSVG/"
    
    # Fetch content from PyPi
    response = requests.get(base_url)
    print(f"Request to {base_url} returned status code {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all anchor links
    all_links = [a['href'] for a in soup.find_all('a', href=True)]
    print("All anchor links on the page:")
    print(all_links)

    # Identify GitHub link from the PyPi page
    github_link = next((link for link in all_links if 'github.com' in link and 'Kozea/CairoSVG' in link), None)
    
    if github_link:
        # Fetch content from GitHub repository main page
        github_response = requests.get(github_link)
        github_soup = BeautifulSoup(github_response.content, 'html.parser')
        
        # Locate the element with id 'readme'
        readme_content = github_soup.find(id='readme')
        
        if readme_content:
            return readme_content.get_text()
        else:
            return "README content not found on the GitHub page."
    else:
        return "GitHub link not found on the PyPi page."

# Test
print(fetch_github_readme_content())