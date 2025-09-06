from playwright.sync_api import sync_playwright
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os
import glob

with sync_playwright() as p:
    no_images = []
    links_to_process=[]

    load_dotenv(".env")
    download_path = os.getenv("DOWNLOAD_PATH")
    image_download_path = os.getenv("DOWNLOAD_PATH_IMAGES")
    browser = p.chromium.launch(channel="chrome", downloads_path=download_path, headless=False)
    context = browser.new_context()
    page = browser.new_page()

    filenames_in_directory = glob.glob(f'{download_path}*.html')
    print(f"{len(filenames_in_directory)} HTML files")

    page.goto(f"{os.getenv("BASE_URL")}")

    for site_partial in filenames_in_directory:
        print(f'Currently searching through the {site_partial} webpage')
        try:
           page.goto(f"{os.getenv("BASE_URL")}/{site_partial}")
           page.wait_for_timeout(2000)
           found_images = []

           imgs = page.query_selector_all("img")
           for img in imgs:
               src = img.get_attribute("src")
               if src.startswith("http"):
                   found_images.append(src)
                   
           print(f' Found {len(found_images)} images')
           if len(found_images) > 0:
               save_path = (f'{image_download_path}{site_partial.split("/")[-1].split(".")[0]}/')
               os.mkdir(save_path)
               for index, found_image in enumerate(found_images):
                   page.goto(found_image)
                   page.get_by_role("img").screenshot(animations="disabled", path=f"{save_path}image-{index}.png")
               no_images.append(site_partial + " - no images")
               pd.DataFrame(no_images).to_csv(f'pages_without-images-{datetime.today().strftime('%Y-5m-%d')}.csv', index=False)

        except Exception as e:
            print(e)
            no_images.append(site_partial + " - Exception")
            pd.DataFrame(no_images).to_csv(f'web-pages-with-exceptions-{datetime.today().strftime('%Y-5m-%d')}.csv', index=False)

context.close()
browser.close()