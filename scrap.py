import json
import requests
from bs4 import BeautifulSoup

def extract_project_description(library_name):
    url = f"https://pypi.org/project/{library_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with class .project-description
    div = soup.find('div', class_='project-description')

    # Return the plain text content
    return div.get_text() if div else ""

def main():
    # Load the library names
    with open("libraries_with_warehouse.json", "r") as file:
        libraries = json.load(file)

    descriptions = {}
    for library in libraries:
        print(f"Scraping {library}...")
        descriptions[library] = extract_project_description(library)

    # Save the results to a JSON file
    with open("library_descriptions.json", "w") as file:
        json.dump(descriptions, file, indent=4)

    print("Scraping completed and data saved to library_descriptions.json")

if __name__ == "__main__":
    main()