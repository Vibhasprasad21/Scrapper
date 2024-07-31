from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import pprint

def extract_table_value(td):
    try:
        return td.find_element(By.TAG_NAME, 'span').text
    except Exception as e:
        return td.text

def extract_details(project):
    name = project.find_element(By.TAG_NAME, 'span').text
    print('>>> Finding details for ', name)
    link = project.find_element(By.TAG_NAME, 'a')
    # Open details modal
    link.click()
    # Wait for modal to load
    time.sleep(15)
    # Find table elements, [key1, value1, key2, value2]
    tableElements = driver.find_elements(By.CSS_SELECTOR, '#project-menu-html > div:nth-child(2) > div > div > table > tbody > tr > td')
    # Partition list to find even index elements to be key
    tableKeys = [e.text for e in tableElements[::2]]
    # Partition list to find odd index elements to be value
    # Some values like pan no are nested inside span, call method to extract
    tableValues = [extract_table_value(e) for e in tableElements[1::2]]
    table = dict(zip(tableKeys, tableValues))
    table['ProjectName'] = name # Add back project name missing from table
    # Close modal so next click of a-tag will work correctly
    driver.find_elements(By.CSS_SELECTOR, 'button.close[data-dismiss=modal]')[0].click()
    return table

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://hprera.nic.in/PublicDashboard')
    time.sleep(60) # Wait to load whole page
    # Find all projects listed
    all_projects = driver.find_elements(By.CSS_SELECTOR, '#reg-Projects > div > div > div > div > div')
    projects = all_projects[:6]
    print('>>> Found projects, extracting details')
    details = [extract_details(project) for project in projects]
    print('>>> Completed scraping')
    pprint.pprint(details)


