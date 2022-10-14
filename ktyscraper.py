# importing dependencies
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Function to Append values to a key in the dictionary
def add_values_in_dict(sample_dict, key, list_of_values):
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

# Sets up the browser
# I have already set up the path to the webdriver in env values
driver = webdriver.Chrome()

driver.implicitly_wait(3)
site = 'https://knowthychoice.in/blog/'
driver.get(site)
driver.implicitly_wait(7)

# data_dict stores the Heading and Course Contents as key/value pairs
data_dict = {}

# subLinks stores the subject links
subLinks = driver.find_elements(By.TAG_NAME,'a')
subLinks = subLinks[6:16:]
# linkfile.txt stores the subject links in a file for further use so as to prevent errors in the script
linkfile = open("linkfile.txt", 'w')
for link in subLinks:
    linkfile.write(link.get_attribute('href') + '\n')
linkfile.close()

# data.json stores the OUTPUT DATA as JSON
file = open("data.json", "w")

with open("linkfile.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    driver.get(stripped_line)
    driver.implicitly_wait(5)
    heading = driver.find_element(By.TAG_NAME,'h2')
    topicsUL = driver.find_element(By.XPATH,'//*[@id="content"]/section[2]/div/div/div/article/ul[4]')
    topicsCovered = topicsUL.find_elements(By.TAG_NAME, 'li')
    for topic in topicsCovered:
        # split text by '-//-*-*-=-' to prevent splitting of the string into pieces while appending it to the dictionary
        add_values_in_dict(data_dict,heading.text, topic.text.split('-//-*-*-=-'))

# converts the dictionary to JSON format and stores in the data.json file
file.write(json.dumps(data_dict))
file.close()

# waits for 10 seconds and quits the browser
time.sleep(10)
driver.quit()