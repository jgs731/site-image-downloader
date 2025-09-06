Define base url of target website
Define links to process (this can be stored in a dictionary, array or passed into the code using a CSV file (just a minor tweak required for this!)
Go through defined links to process and capture the image URLs using the src attribute (skip past pages with no images found)
In the found images array, loop through and download images, using the Playwright screenshot method which will save images into respective folders for each web page
Document any errors or pages with no images (this should be fine, but for spot checking) and any errors/exceptions are documented in separate CSV files
