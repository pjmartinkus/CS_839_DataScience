from bs4 import BeautifulSoup
from selenium import webdriver
import re, sys


def create_amazon_csv():

    # Save data to csv file
    file_path = '/u/p/m/pmartinkus/Documents/CS_838/Stage 2/Data/Amazon.csv'
    file = open(file_path, 'w')
    file.write('Name,Price,Brand,Screen Size,RAM,Hard Drive Capacity,Processor Type,Processor Speed,Operating System,Battery Life\n')
    file.close()

    # The columns for the data
    cols = ['Name', 'Price', 'Brand', 'Screen Size', 'RAM Size', 'Hard-Drive Size', 'Processor (CPU) Manufacturer',
            'Processor Speed', 'Operating System', 'Battery Life']

    # Get page html
    #sys.path.append('/u/p/m/pmartinkus/Applications/bin/geckodriver.exe')
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)  # seconds
    url = 'https://www.amazon.com/s/ref=sr_pg_1?rh=n%3A172282%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108%2Ck%3Alaptop&keywords=laptop&ie=UTF8&qid=1521225482'
    driver.get(url)
    html = driver.page_source

    # Keep getting new data rows until we have the required 3000
    laptops = 0
    page = 1
    while laptops < 3100:

        # Parse with Beautiful Soup
        soup = BeautifulSoup(html)

        # Get all the links on this page
        hrefs = []
        divs = soup.find_all('div', {'class': 'a-fixed-left-grid-col a-col-right'})
        for div in divs:
            # Remove sponsored links (they are not always laptops)
            if 0 == len(div.find_all('h5', {'class': 'a-spacing-none a-color-tertiary s-sponsored-list-header s-sponsored-header sp-pixel-data a-text-normal'})):
                hrefs.append(div.find('a', {'class': 'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'}))

        # get all of the data for each laptop
        regex = re.compile('[^0-9.]')
        for href in hrefs:

            # Save information about each laptop
            tuple = {}
            for col in cols:
                tuple[col] = str(float('NaN'))

            # Get the soup object for this laptops page
            loaded = False
            attempts = 0
            if href is not None:
                link = str(href['href'])
            while href is not None and not loaded:
                driver.get(link)
                if 'HLCXComparisonTable' in driver.page_source:
                    loaded = True
                else:
                    attempts += 1
                    if attempts > 3:
                        loaded = True
            html = driver.page_source
            soup_laptop = BeautifulSoup(html)

            # If we successfully loaded the next page
            if loaded is True and attempts <= 3:

                # Get the name for this laptop
                if href['title'] is not None:
                    tuple['Name'] = "'" + str(href['title']).replace("'", '') + "'"
                else:
                    tag = soup_laptop.find('span', {'id': 'productTitle'})
                    tuple['Name'] = "'" + tag.text.strip().replace("'", '') + "'"

                # Get the Price
                tag = soup_laptop.find('span', {'id': 'priceblock_ourprice'})
                if tag is not None:
                    tuple['Price'] = float(regex.sub('', tag.text))

                # Get the Brand
                tag = soup_laptop.find('a', {'id': 'bylineInfo'})
                if tag is not None:
                    tuple['Brand'] = tag.text.strip()

                # Get the specifications
                table = soup_laptop.find('table', {'id': 'HLCXComparisonTable'})
                table_body = table.find('tbody')
                rows = table_body.find_all('tr')
                for row in rows:
                    if row.find('th') is not None and row.find('td') is not None:
                        key = row.find('th').text.strip()
                        val = "'" + row.find('td').text.strip() + "'"
                        if key in cols and key != 'Price' and val != "'—'":
                            tuple[key] = val

                # Add the new tuple to the csv file
                line = ','.join([tuple['Name'], str(tuple['Price']), tuple['Brand'], tuple['Screen Size'],
                                 tuple['RAM Size'], tuple['Hard-Drive Size'], tuple['Processor (CPU) Manufacturer'],
                                 tuple['Processor Speed'], tuple['Operating System'], tuple['Battery Life']])
                file = open(file_path, 'a')
                file.write(line + '\n')
                file.close()
                laptops += 1

        # Get the next page html
        page += 1
        url = url.replace('page=' + str(page-1), 'page=' + str(page))
        url = url.replace('sr_pg_' + str(page - 1), 'sr_pg_' + str(page))
        driver.get(url)
        html = driver.page_source

    # Close the window when we're done
    driver.close()
