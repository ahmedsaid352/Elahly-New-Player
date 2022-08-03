import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from time import sleep

teams_urls =[]
links =[]
positions = []
names =[]

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()

browser.get("https://www.transfermarkt.com/afrika-cup-qualifikation/teilnehmer/pokalwettbewerb/AFCQ/saison_id/2021")
sleep(1)
teams_urls = browser.find_elements(By.XPATH,'//*[@id="yw1"]/table/tbody/tr[*]/td[2]/a')
for i in range(len(teams_urls)):
    teams_urls[i] = teams_urls[i].get_attribute('href')

for j in range(len(teams_urls)):
    browser.get(teams_urls[j])
    sleep(1)
    newurl = browser.find_element(By.XPATH,'//*[@id="main"]/main/div[3]/div[1]/div[1]/div[3]/a[2]').get_attribute('href')
    browser.get(newurl)
    sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(html,"html.parser")
    heights = soup.select('#yw1 > table > tbody > tr > td:nth-child(5)')
    allnames = soup.select('#yw1 > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td.hauptlink > a')
    allpositions = soup.select('#yw1 > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td')
    for c in range(len(heights)):
        if (heights[c].text == "1,86 m"):
            playerName = allnames[c].text
            playerLink = 'https://www.transfermarkt.com' + allnames[c]['href']
            playerPosition = allpositions[c].text
            names.append(playerName)
            links.append(playerLink)
            positions.append(playerPosition)

information = {
    'name':names,
    'link':links,
    'positions':positions
}
df = pd.DataFrame(information)
df.to_excel('allExpectedPlayers.xlsx',index=False)
print("\n\n data collected successfully")