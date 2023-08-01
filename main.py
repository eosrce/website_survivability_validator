import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# Define a function to check website status and homepage content
def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        if response.status_code == 304:
            print(f"{url} has a 304 redirect.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('h2', text='主页'):
            print(f"{url} is a homepage.")
    except requests.exceptions.RequestException as e:
        print(f"{url} is not reachable: {e}")

# Load URLs from a text file
def load_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return urls

if __name__ == "__main__":
    # Replace 'urls.txt' with the path to your input text file containing URLs
    urls = load_urls_from_file('urls.txt')

    # Set proxies if needed
    proxies = {
        'http': 'http://user:password@proxy_host:proxy_port',
        'https': 'https://user:password@proxy_host:proxy_port',
    }

    # Use ThreadPoolExecutor for high concurrency
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_website, urls)