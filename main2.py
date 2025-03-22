import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

def scrape_tc_title_links(urls: List[str]) -> List[Dict]:
    """
    Scrape data from href elements inside td tags with class "tc_title".
    
    Args:
        urls: List of URLs to scrape
        
    Returns:
        List of dictionaries containing title and href data
    """
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in urls:
        try:
            # Add delay to avoid hitting server too quickly
            time.sleep(1)
            
            # Make the request
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all td elements with class "tc_title"
            tc_title_elements = soup.find_all('td', class_='tc_title')
            
            for element in tc_title_elements:
                # Find anchor tag inside the td element
                anchor = element.find('a')
                if anchor:
                    # Extract href and title
                    href = anchor.get('href')
                    title = anchor.get('title') or anchor.text.strip()
                    lang = anchor.get('lang', '')
                    
                    # Ensure the href is a full URL if it's relative
                    if href and href.startswith('/'):
                        base_url = '/'.join(url.split('/')[:3])  # Extract protocol and domain
                        href = base_url + href
                    
                    results.append({
                        'title': title,
                        'href': href,
                        'lang': lang,
                        'text': anchor.text.strip(),
                        'source_url': url
                    })
                    
            print(f"Successfully scraped {url}, found {len(tc_title_elements)} tc_title elements")
                    
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            
    return results

# Example usage:
if __name__ == "__main__":
    urls_to_scrape = [
        "https://vndb.org/v?cfil=&f=&fil=&p=1&rfil=&s=24M",
    ]
    
    results = scrape_tc_title_links(urls_to_scrape)
    
    # Print the results
    for i, result in enumerate(results, 1):
        print(f'''"{result['href']}",''')