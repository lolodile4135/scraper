import requests
from bs4 import BeautifulSoup
from datetime import datetime


parser = argparse.ArgumentParser(description="Scrape G2 reviews for a product within a date range")

parser.add_argument("product", help="Product name (as in URL, e.g., shopify)")
parser.add_argument("start_date", help="Start date in YYYY-MM-DD format")
parser.add_argument("end_date", help="End date in YYYY-MM-DD format")

args = parser.parse_args()

product_name = args.product
start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

print(f"Scraping reviews for: {product_name}")
print(f"From {start_date.date()} to {end_date.date()}")

def scrape_g2_reviews(product_name, start_date, end_date):
    """
    Scrape G2 reviews for a product within a date range.
    
    Args:
        product_name (str): e.g. "shopify"
        start_date (str): "YYYY-MM-DD"
        end_date (str): "YYYY-MM-DD"
    
    Returns:
        List[dict]: Each dict has 'date', 'title', 'body', 'stars'
    """
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    reviews_data = []
    page = 1
    while True:
        url = f"https://www.g2.com/products/{product_name}/reviews?page={page}&_pjax=%23pjax-container"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            break  # Stop if page not found
        
        soup = BeautifulSoup(res.text, "html.parser")
        blocks = soup.find_all("div", attrs={"data-poison": True})
        if not blocks:
            break  # No more reviews
        
        found_review = False
        for block in blocks:
            for article in block.find_all("article"):
                # Extract date
                date_tag = article.select_one("label.elv-tracking-normal.elv-text-sm")
                date_str = date_tag.get_text(strip=True) if date_tag else None
                if not date_str:
                    continue
                
                # Convert date to datetime object
                try:
                    review_dt = datetime.strptime(date_str, "%m/%d/%Y")
                except:
                    continue
                
                # Filter by start and end date
                if review_dt < start_dt or review_dt > end_dt:
                    continue
                
                found_review = True
                
                # Extract title
                title_tag = article.select_one("div.elv-text-lg.elv-font-bold")
                title = title_tag.get_text(strip=True) if title_tag else None
                
                # Extract body
                text_tag = article.select_one("div.review-body, p")
                body = text_tag.get_text(strip=True) if text_tag else None
                
                # Extract stars (like "5/5")
                stars_tag = article.select_one("label.elv-tracking-normal.elv-text-base")
                stars = stars_tag.get_text(strip=True) if stars_tag else None
                
                reviews_data.append({
                    "date": date_str,
                    "title": title,
                    "body": body,
                    "stars": stars
                })
        
        if not found_review:
            break  # No reviews in this page within date range
        
        page += 1  # Next page
    
    return reviews_data

# Example usage
all_reviews = scrape_g2_reviews(product_name)

filtered_reviews = [
    r for r in all_reviews
    if start_date <= datetime.strptime(r["date"], "%m/%d/%Y") <= end_date
]

print(filtered_reviews)
