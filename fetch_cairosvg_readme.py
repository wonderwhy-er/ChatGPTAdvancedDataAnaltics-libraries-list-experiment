
import requests
from bs4 import BeautifulSoup

def fetch_github_readme():
    # Fetch PyPI page for CairoSVG
    response = requests.get('https://pypi.org/project/CairoSVG/')
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract GitHub link
    github_link = soup.find('a', class_='vertical-tabs__tab')['href']
    
    # Modify the link to directly point to the README.md on GitHub
    if 'github.com' in github_link:
        readme_link = f"{github_link}/blob/main/README.md"
        
        # Fetch README content
        readme_response = requests.get(readme_link)
        readme_soup = BeautifulSoup(readme_response.content, 'html.parser')
        
        # GitHub displays the README content within an article tag
        readme_content = readme_soup.find('article', class_='markdown-body entry-content container-lg').get_text()
        
        return readme_content
    else:
        return "GitHub link not found."

if __name__ == '__main__':
    readme = fetch_github_readme()
    print(readme)

