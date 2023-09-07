
import requests
from bs4 import BeautifulSoup

def fetch_github_readme():
    # Fetch PyPI page for CairoSVG
    response = requests.get('https://pypi.org/project/CairoSVG/')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Log the initial request details
    print(f"Request to {response.url} returned status code {response.status_code}")
    
    # Extract and log all anchor links from the page for debugging
    all_links = [a['href'] for a in soup.find_all('a', href=True)]
    print(f"All anchor links on the page:\n{all_links}\n")
    
    # Extract GitHub link from the list of all links
    github_link = next((link for link in all_links if 'github.com' in link), None)

    if github_link:
        # Modify the link to directly point to the README.md on GitHub
        readme_link = f"{github_link}/blob/main/README.md"
        
        # Fetch README content
        readme_response = requests.get(readme_link)
        readme_soup = BeautifulSoup(readme_response.content, 'html.parser')
        
        # GitHub displays the README content within an article tag
        readme_content = readme_soup.find('article', class_='markdown-body entry-content container-lg').get_text()
        
        return readme_content
    else:
        return "GitHub link not found on the page."

if __name__ == '__main__':
    readme = fetch_github_readme()
    print(readme)

