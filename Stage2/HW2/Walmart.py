from bs4 import BeautifulSoup
from selenium import webdriver
import re, sys


def create_walmart_csv(brand, total_pages):

    # Save data to csv file
    file_path = '/u/p/m/pmartinkus/Documents/CS_838/Stage 2/Data/Walmart_' + brand + '.csv'

    # The columns for the data
    cols = ['Name', 'Price', 'Brand', 'Screen Size', 'RAM Memory', 'Hard Drive Capacity', 'Processor Type',
            'Processor Speed', 'Operating System', 'Battery Life']

    # Get page html
    sys.path.append('/u/p/m/pmartinkus/Applications/bin/geckodriver.exe')
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)  # seconds
    url = 'https://www.walmart.com/browse/electronics/laptop-computers/3944_3951_1089430_1230091?cat_id=3944_3951_1089430_1230091_132960&facet=brand%3A'
    url = url + brand + '&grid=false&page=1&vertical_whitelist=home#searchProductResult'
    driver.get(url)
    html = driver.page_source

    # Keep getting new data rows until we have the required 3000
    page = 1
    while page <= total_pages:

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html)

        # Get all the links on this page
        hrefs = soup.find_all('a', {'class': 'product-title-link'})

        # get all of the data for each laptop
        prev = ' '
        regex = re.compile('[^0-9.]')
        for href in hrefs:

            # Save information about each laptop
            tuple = {}
            for col in cols:
                tuple[col] = str(float('nan'))

            # Get the name for this laptop
            tuple['Name'] = "'" + str(href['aria-label']).replace("'", '') + "'"

            # Get the soup object for this laptops page
            link = 'https://www.walmart.com' + str(href['href'])
            loaded = False
            attempts = 0
            while not loaded and not prev == link:
                try:
                    driver.get(link)
                    if 'table table-striped-odd specification' not in driver.page_source:
                        driver.find_element_by_css_selector('.btn.btn-badge.btn-badge-alt').click()
                    loaded = True
                except:
                    attempts += 1
                    if attempts > 3:
                        loaded = True
            html = driver.page_source
            soup_laptop = BeautifulSoup(html)
            prev = link

            # If we successfully loaded the next page
            if loaded == True and attempts <= 3:

                # Get the Price
                tag = soup_laptop.find('span', {'class': 'Price-group'})
                tuple['Price'] = float(regex.sub('', tag['title']))

                # Get the specifications
                table = soup_laptop.find('table', {'class': 'table table-striped-odd specification'})
                table_body = table.find('tbody')
                rows = table_body.find_all('tr')
                for row in rows:
                    key = row.find('th').text.strip()
                    val = "'" + row.find('td').text.strip() + "'"
                    if key in cols:
                        tuple[key] = val

                # Add the new tuple to the csv file
                line = ','.join([tuple['Name'], str(tuple['Price']), tuple['Brand'], tuple['Screen Size'],
                                tuple['RAM Memory'], tuple['Hard Drive Capacity'], tuple['Processor Type'],
                                tuple['Processor Speed'], tuple['Operating System'], tuple['Battery Life']])
                file = open(file_path, 'a')
                file.write(line + '\n')
                file.close()

        # Get the next page html
        page += 1
        if page <= total_pages:
            url = url.replace('page=' + str(page-1), 'page=' + str(page))
            driver.get(url)
            html = driver.page_source

    # Close the window when we're done
    driver.close()
