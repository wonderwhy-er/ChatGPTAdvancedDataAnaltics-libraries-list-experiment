
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
    
    # Extract GitHub link
    github_anchor = soup.find('a', class_='vertical-tabs__tab')
    if github_anchor:
        github_link = github_anchor['href']
        
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
            return f"Unexpected link found: {github_link}"
    else:
        return "GitHub link (anchor with class 'vertical-tabs__tab') not found on the page."

if __name__ == '__main__':
    readme = fetch_github_readme()
    print(readme)

