# >>> HTML Extraction <<<
from selectolax.parser import HTMLParser
from httpx import get
import logging
import shutil
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# >>> FUNCTIONS <<<
# ------------------------------------------------------------------------------
def get_img_tags_for(term=None):
    if not term:
        raise Exception('No Search Term Provided')

    url = f'https://unsplash.com/s/photos/{term}'
    response = get(url)

    if response.status_code != 200:
        raise Exception('Error Getting Response')
    
    tree = HTMLParser(response.text)
    imgs = tree.css('figure a img + img')
    return imgs

# ------------------------------------------------------------------------------
def img_filter(url: str, keywords: list) -> bool:
    return not any(x in url for x in keywords)

# ------------------------------------------------------------------------------
def get_high_res_img_url(img_node):
    srcset = img_node.attrs['srcset']
    srcset_list = srcset.split(', ')

    url_res = [src.split(', ') for src in srcset_list 
               if img_filter(src, ['plus', 'premium', 'profile'])]
    
    if not url_res:
        return None
    
    return url_res[0][0].split('?')[0]

# ------------------------------------------------------------------------------
def save_images(img_urls, amount=10 ,dest_dir='scraped images', tags=''):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    img_urls = img_urls[:amount]

    for url in img_urls:
        response = get(url)
        logging.info(f'Downloading {url}...')

        file_name = url.split('/')[-1]

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(f'{dest_dir}/{tags}{file_name}.jpeg', 'wb') as f:
            f.write(response.content)
            logging.info(f'Saved {file_name}, with size {round(len(response.content)/1024/1024,2)} MB.')



# >>> TEST <<<
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    search_tag = 'galaxy'

    img_nodes = get_img_tags_for(search_tag)
    all_img_urls = [get_high_res_img_url(i) for i in img_nodes]
    img_urls = [u for u in all_img_urls if u]
    # print(img_urls)

    save_images(img_urls, amount=5, dest_dir='scraped images', tags=search_tag)