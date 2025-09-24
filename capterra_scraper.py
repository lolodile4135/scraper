from bs4 import BeautifulSoup

html = """<your full HTML page here>"""  # Replace with actual HTML

soup = BeautifulSoup(html, "html.parser")

reviews_section = soup.find("section", id="reviews", class_="container")
reviews_data = []

if reviews_section:
    # Find all review cards
    review_cards = reviews_section.find_all("div", class_="review-card")
    
    for card in review_cards:
        # Title
        title_tag = card.find("h3", class_="fs-3 fw-bold")
        title = title_tag.get_text(strip=True) if title_tag else None

        # Date
        date_tag = card.find("div", class_="fs-5 text-neutral-90")
        date = date_tag.get_text(strip=True) if date_tag else None

        # Review body (the first fs-4 lh-2 text-neutral-99 div after the card div)
        body_tag = card.find_next("div", class_="fs-4 lh-2 text-neutral-99")
        body = body_tag.get_text(strip=True) if body_tag else None

        reviews_data.append({
            "title": title,
            "date": date,
            "body": body
        })

# Print results
for r in reviews_data:
    print(r)
