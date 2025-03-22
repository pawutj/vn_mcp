import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Any, Optional


class WebScraper:
    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize the web scraper with optional custom user agent.
        
        Args:
            user_agent: Optional custom user agent string to use for requests
        """
        self.user_agent = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
    
    def fetch_and_scrape_urls(self, urls: List[str], delay_range: tuple = (1, 3)) -> List[Dict[str, Any]]:
        """
        Fetch multiple URLs and scrape 'vndesc' and 'vntags' class data from each.
        
        Args:
            urls: List of URLs to scrape
            delay_range: Tuple of (min_seconds, max_seconds) to wait between requests
            
        Returns:
            List of dictionaries containing scraped data for each URL
        """
        results = []
        
        for url in urls:
            try:
                # Add random delay to avoid getting blocked
                if len(results) > 0:  # No delay for the first request
                    delay = random.uniform(delay_range[0], delay_range[1])
                    time.sleep(delay)
                
                # Get data from this URL
                data = self.scrape_single_url(url)
                if data:
                    results.append(data)
                
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
        
        return results
    
    def scrape_single_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single URL for 'vndesc' and 'vntags' class data.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing scraped data or empty dict if failed
        """
        try:
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find elements with class 'vndesc' and div with id 'vntags'
            vndesc_elements = soup.find_all(class_='vndesc')
            vntags_elements = [soup.find('div', id='vntags')] if soup.find('div', id='vntags') else []
            
            # Find the second h1 element for the name
            h1_elements = soup.find_all('h1')
            name = h1_elements[1].get_text(strip=True) if len(h1_elements) >= 2 else ""
            
            # Extract text from elements
            vndesc_text = [elem.get_text(strip=True) for elem in vndesc_elements]
            
            # Extract text from vntags elements, split by comma and remove digits
            vntags_text = []
            for elem in vntags_elements:
                if elem:
                    # Get the text content
                    text = elem.get_text(strip=True)
                    # Split by comma
                    tags = [tag.strip() for tag in text.split('.')]
                    # Remove digits from each tag
                    clean_tags = [''.join(c for c in tag if not c.isdigit()) for tag in tags]
                    # Remove any empty tags after cleaning
                    clean_tags = [tag.strip() for tag in clean_tags if tag.strip()]
                    vntags_text.append(clean_tags)
            
            # Create result dictionary
            result = {
                'url': url,
                'name': name,
                'vndesc': vndesc_text,
                'vntags': vntags_text,
                # Include the raw elements for further processing if needed
                'vndesc_html': [str(elem) for elem in vndesc_elements],
                'vntags_html': [str(elem) for elem in vntags_elements]
            }
            
            return result
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return {'url': url, 'error': str(e)}


# Example usage
def main():
    # List of URLs to scrape
    urls = [
        'https://vndb.org/v2002',
    ]
    
    # Create scraper instance
    scraper = WebScraper()
    
    # Fetch and scrape data
    results = scraper.fetch_and_scrape_urls(urls)
    
    # Print results
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} from {result['url']}:")
        print(f"Name: {result.get('name', 'Not found')}")
        print(f"vndesc items: {len(result['vndesc'])}")
        print(f"vntags items: {len(result['vntags'])}")
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            # Print first item from each category as sample
            if result['vndesc']:
                print(f"Sample vndesc: {result['vndesc'][0][:100]}...")
            if result['vntags'] and result['vntags'][0]:
                print(f"Sample vntags list: {result['vntags'][0]}")
    
    return results


if __name__ == "__main__":
    main()