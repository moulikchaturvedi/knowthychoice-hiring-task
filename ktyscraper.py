from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

def add_values_in_dict(sample_dict, key, list_of_values):
    ''' Append multiple values to a key in 
        the given dictionary '''
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

driver = webdriver.Chrome()

driver.implicitly_wait(3)
site = 'https://knowthychoice.in/blog/'
driver.get(site)

driver.implicitly_wait(7)
keyValue = {}
subLinks = driver.find_elements(By.TAG_NAME,'a')
subLinks = subLinks[6:16:]
linkfile = open("linkfile.txt", 'w')
for link in subLinks:
    linkfile.write(link.get_attribute('href') + '\n')
linkfile.close()
file = open("data.json", "w")
with open("linkfile.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    # print (stripped_line)
    driver.get(stripped_line)
    driver.implicitly_wait(5)
    heading = driver.find_element(By.TAG_NAME,'h2')
    topicsUL = driver.find_element(By.XPATH,'//*[@id="content"]/section[2]/div/div/div/article/ul[4]')
    topicsCovered = topicsUL.find_elements(By.TAG_NAME, 'li')
    for topic in topicsCovered:
        print (topic.text)
        add_values_in_dict(keyValue,heading.text, topic.text.split('-//-*-*-=-'))
file.write(json.dumps(keyValue))
file.close()

time.sleep(10)
driver.quit()