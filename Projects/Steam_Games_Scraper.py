from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser, Node
import pandas as pd


# >>> FUNCTIONS <<<
# ------------------------------------------------------------------------------
def extract_full_body_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for all network communications to stop changing
        page.wait_for_load_state('networkidle')

        # Force playwright to scroll to the end of the page
        page.evaluate('() => window.scroll(0, document.body.scrollHeight)')

        # Wait for everything in the document to be loaded
        page.wait_for_load_state('domcontentloaded')

        # Take a screenshot of the page to check if the information is there
        # page.screenshot(path='steam.png', full_page=True)

        # Get full html of the page
        html = page.inner_html('body')
        return html
    
# ------------------------------------------------------------------------------
def parse_raw_attributes(node: Node, selectors: list):
    parsed = {}
    for s in selectors:
        match = s.get('match')
        type_ = s.get('type')
        selector = s.get('selector')
        name = s.get('name')

        if match == 'all':
            matched = node.css(selector)
            if type_ == 'text':
                parsed[name] = [node.text() for node in matched]
            elif type_ == 'node':
                parsed[name] = matched

        elif match == 'first':
            matched = node.css_first(selector)
            if type_ == 'text':
                parsed[name] = matched.text()
            elif type_ == 'node':
                parsed[name] = matched
    return parsed



# >>> TEST <<<
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    URL = 'https://store.steampowered.com/specials'
    
    html = extract_full_body_html(url=URL)
    tree = HTMLParser(html)
    divs = tree.css("div[class*='ImpressionTrackedElement']")

    # Extract information
    info = []
    for d in divs:
        title_element = d.css_first("a div[class*='StoreSaleWidgetTitle']") # Title
        thumbnail_element = d.css_first("div[class*='CapsuleImageCtn']") # Thumbnail
        tags_elements = [a.text() for a in d.css("a[class*='WidgetTag']")[:5]] # Tags
        date_element = d.css_first("div[class*='U5-JPeer1']") # Release Date
        price_element = d.css_first("div[class*='StoreSalePriceWidgetContainer']") # Prices

        if title_element is not None:
            title = title_element.text()
            thumbnail = thumbnail_element.css_first('img').attributes.get('src')
            tags = tags_elements
            date = date_element.text()
            original_price = price_element.css_first("div[class*='_1EK']").text()
            discount_price = price_element.css_first("div[class*='Wh0']").text()

            attrs = {
            'title': title,
            'tags': tags,
            'release date': date,
            'original price': original_price,
            'discount price': discount_price,
            'thumbnail': thumbnail,
            }
            info.append(attrs)

        else:
            pass

    df = pd.DataFrame(info)    
    df.to_csv('Projects/Steam_Games_Scraper.csv')