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
        i=0
        print("START")
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
            i=i+1
            print("###" +"url" + str(i) + "###")
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
                # 'vndesc_html': [str(elem) for elem in vndesc_elements],
                # 'vntags_html': [str(elem) for elem in vntags_elements]
            }
            
            return result
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return {'url': url, 'error': str(e)}




urls = [
    "https://vndb.org/v2002",
"https://vndb.org/v92",
"https://vndb.org/v7771",
"https://vndb.org/v20802",
"https://vndb.org/v2153",
"https://vndb.org/v2016",
"https://vndb.org/v18717",
"https://vndb.org/v24",
"https://vndb.org/v17909",
"https://vndb.org/v12402",
"https://vndb.org/v68",
"https://vndb.org/v562",
"https://vndb.org/v21438",
"https://vndb.org/v3144",
"https://vndb.org/v19987",
"https://vndb.org/v20431",
"https://vndb.org/v3660",
"https://vndb.org/v4",
"https://vndb.org/v21069",
"https://vndb.org/v1913",
"https://vndb.org/v26154",
"https://vndb.org/v37150",
"https://vndb.org/v777",
"https://vndb.org/v5",
"https://vndb.org/v22313",
"https://vndb.org/v11",
"https://vndb.org/v1141",
"https://vndb.org/v26523",
"https://vndb.org/v31813",
"https://vndb.org/v19035",
"https://vndb.org/v31055",
"https://vndb.org/v67",
"https://vndb.org/v716",
"https://vndb.org/v21267",
"https://vndb.org/v18397",
"https://vndb.org/v751",
"https://vndb.org/v31929",
"https://vndb.org/v26987",
"https://vndb.org/v13188",
"https://vndb.org/v3770",
"https://vndb.org/v5922",
"https://vndb.org/v28731",
"https://vndb.org/v6639",
"https://vndb.org/v20424",
"https://vndb.org/v21675",
"https://vndb.org/v17012",
"https://vndb.org/v17",
"https://vndb.org/v6656",
"https://vndb.org/v22728",
"https://vndb.org/v2088",
"https://vndb.org/v17018",
"https://vndb.org/v30925",
"https://vndb.org/v2888",
"https://vndb.org/v16418",
"https://vndb.org/v11472",
"https://vndb.org/v14910",
"https://vndb.org/v38511",
"https://vndb.org/v10028",
"https://vndb.org/v20591",
"https://vndb.org/v1842",
"https://vndb.org/v31805",
"https://vndb.org/v5154",
"https://vndb.org/v5844",
"https://vndb.org/v27685",
"https://vndb.org/v1299",
"https://vndb.org/v18152",
"https://vndb.org/v1143",
"https://vndb.org/v14018",
"https://vndb.org/v36687",
"https://vndb.org/v15395",
"https://vndb.org/v835",
"https://vndb.org/v768",
"https://vndb.org/v1483",
"https://vndb.org/v487",
"https://vndb.org/v23741",
"https://vndb.org/v26391",
"https://vndb.org/v7721",
"https://vndb.org/v37651",
"https://vndb.org/v19011",
"https://vndb.org/v33504",
"https://vndb.org/v13083",
"https://vndb.org/v18649",
"https://vndb.org/v13802",
"https://vndb.org/v16032",
"https://vndb.org/v25635",
"https://vndb.org/v17642",
"https://vndb.org/v12849",
"https://vndb.org/v50081",
"https://vndb.org/v1358",
"https://vndb.org/v29661",
"https://vndb.org/v432",
"https://vndb.org/v25288",
"https://vndb.org/v3112",
"https://vndb.org/v13882",
"https://vndb.org/v4463",
"https://vndb.org/v27557",
"https://vndb.org/v1278",
"https://vndb.org/v3883",
"https://vndb.org/v12455",
"https://vndb.org/v17046",
"https://vndb.org/v27916",
"https://vndb.org/v37713",
"https://vndb.org/v4918",
"https://vndb.org/v3697",
"https://vndb.org/v47866",
"https://vndb.org/v23097",
"https://vndb.org/v31360",
"https://vndb.org/v38886",
"https://vndb.org/v33368",
"https://vndb.org/v42652",
"https://vndb.org/v29443",
"https://vndb.org/v2045",
"https://vndb.org/v211",
"https://vndb.org/v30919",
"https://vndb.org/v23077",
"https://vndb.org/v1564",
"https://vndb.org/v26485",
"https://vndb.org/v30804",
"https://vndb.org/v44096",
"https://vndb.org/v18160",
"https://vndb.org/v25931",
"https://vndb.org/v2836",
"https://vndb.org/v7809",
"https://vndb.org/v16131",
"https://vndb.org/v26307",
"https://vndb.org/v33924",
"https://vndb.org/v11849",
"https://vndb.org/v13",
"https://vndb.org/v20592",
"https://vndb.org/v17853",
"https://vndb.org/v6723",
"https://vndb.org/v6245",
"https://vndb.org/v12260",
"https://vndb.org/v32555",
"https://vndb.org/v25616",
"https://vndb.org/v16463",
"https://vndb.org/v24610",
"https://vndb.org/v18778",
"https://vndb.org/v19545",
"https://vndb.org/v8095",
"https://vndb.org/v21852",
"https://vndb.org/v31533",
"https://vndb.org/v44101",
"https://vndb.org/v7",
"https://vndb.org/v20602",
"https://vndb.org/v19810",
"https://vndb.org/v9678",
"https://vndb.org/v19494",
"https://vndb.org/v1360",
"https://vndb.org/v24803",
"https://vndb.org/v19223",
"https://vndb.org/v18953",
"https://vndb.org/v23125",
"https://vndb.org/v13994",
"https://vndb.org/v12369",
"https://vndb.org/v29909",
"https://vndb.org/v19273",
"https://vndb.org/v57",
"https://vndb.org/v29383",
"https://vndb.org/v26530",
"https://vndb.org/v4936",
"https://vndb.org/v16212",
"https://vndb.org/v50008",
"https://vndb.org/v1347",
"https://vndb.org/v15871",
"https://vndb.org/v12984",
"https://vndb.org/v1306",
"https://vndb.org/v7302",
"https://vndb.org/v33175",
"https://vndb.org/v38",
"https://vndb.org/v3941",
"https://vndb.org/v776",
"https://vndb.org/v51437",
"https://vndb.org/v18157",
"https://vndb.org/v2133",
"https://vndb.org/v5834",
"https://vndb.org/v12246",
"https://vndb.org/v12392",
"https://vndb.org/v36674",
"https://vndb.org/v50",
"https://vndb.org/v7679",
"https://vndb.org/v25912",
"https://vndb.org/v2956",
"https://vndb.org/v5652",
"https://vndb.org/v568",
"https://vndb.org/v46116",
"https://vndb.org/v34454",
"https://vndb.org/v41944",
"https://vndb.org/v43288",
"https://vndb.org/v14908",
"https://vndb.org/v13905",
"https://vndb.org/v28123",
"https://vndb.org/v24717",
"https://vndb.org/v548",
"https://vndb.org/v15605",
"https://vndb.org/v3130",
"https://vndb.org/v26664",
"https://vndb.org/v16261",
"https://vndb.org/v31567",
"https://vndb.org/v36776"
]


# Example usage
import json

def main():
    # List of URLs to scrape
    # urls = [
    #     'https://vndb.org/v2002',
    # ]
    
    # Create scraper instance
    scraper = WebScraper()
    
    # Fetch and scrape data
    results = scraper.fetch_and_scrape_urls(urls)
    
    # Save results to JSON file
    output_file = "visual_novel_data.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"Data successfully saved to {output_file}")
        
        # Print a brief summary
        print(f"Saved data for {len(results)} visual novels")
        for result in results:
            print(f"- {result.get('name', 'Unknown title')}")
            if 'error' in result:
                print(f"  Error: {result['error']}")
    
    except Exception as e:
        print(f"Error saving to JSON file: {str(e)}")
    
    return results


if __name__ == "__main__":
    main()