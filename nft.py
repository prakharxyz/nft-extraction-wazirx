from asyncio.windows_events import NULL
from attr import attrs
import time
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

plist = []  #empty list declaed which will contain dictionaries of each nft

URL = "https://nft.wazirx.org"


def selenium_work(website_url, t):
    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(website_url)
    time.sleep(t)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html5lib') #website content
    return soup

soup1 = selenium_work(URL + '/activity', 10)
table = soup1.find('div', attrs = {'class':'ant-table-body'})

for row in table.findAll('tr', attrs = {'class':'ant-table-row ant-table-row-level-0'}):   #each row starting with div and have this class name

    token_link = row.find('a', attrs= {'class':'sc-ciOKUB itWoQV'})['href']
    print(token_link)

    soup2 = selenium_work(URL + token_link, 2)
   
    title = soup2.find('h1', attrs= {'class':'bid-token__details--title'}).get_text()

    try:
        collection = soup2.find('div', attrs= {'class':'sc-fujyAs sc-pNWdM inEejM dfRghT bid-token__details--title-2'}).get_text()
    except:
        collection = '-'
    try:
        price = soup2.find('div', class_='sc-fujyAs sc-pNWdM hrjtPB koAsrp').get_text() + ' (' + soup2.find('div', class_='sc-fujyAs sc-pNWdM cAtPIA hBkTwE').get_text() + ') '
    except:
        price = '-'
    print(title, collection, price)

    try:
        img_link = soup2.find('img', attrs= {'class':'asset-img-wrapper bid-token__asset-wrapper--asset-fit'})['src']
    except:
        img_link = 'unable to fetch'
    print(img_link)

    try:
        creator = soup2.findAll('a', attrs= {'class':'avatar'})[0].find('div', class_='avatar__info--title-wrapper').get_text()
        owner = soup2.findAll('a', attrs= {'class':'avatar'})[1].find('div', class_='avatar__info--title-wrapper').get_text()
    except:
        creator = 'Split'
        owner = soup2.find('a', attrs= {'class':'avatar'}).find('div', class_='avatar__info--title-wrapper').get_text()

    
    print('CREATOR - '+creator, 'OWNER - '+owner)

    print(' TRADE HISTORY - ')
    historyList = []
    try:
        token_history_list = soup2.find('div', attrs= {'class':'token-history--list'})
        for history in token_history_list.findAll('div', attrs= {'class':'token-list-item'}):
            trade = history.find('div', class_='token-list-item--transaction-details').get_text() + ' for ' + history.find('div', class_='token-list-item--amount').get_text() 
            print(trade)
            historyList.append(trade)
    except:
        print('No history')

    desc = soup2.find('div', class_='token-history--content').get_text()

    plist.append({'TITLE':title, 'COLLECTION':collection, 'PRICE':price, 'CREATOR':creator, 'OWNER':owner, 'IMAGE':img_link, 'DESCRIPTION':desc, 'HISTORY':historyList, 'LINK':URL+token_link})


#TO WRITE LIST ON EXCEL

with open('NFT_list.csv','w', encoding="utf-8") as f: #open file to write

    details = ['TITLE','COLLECTION','PRICE','CREATOR','OWNER','IMAGE','DESCRIPTION','HISTORY','LINK'] #field names
    writer = csv.DictWriter(f,fieldnames= details) #to write dict to csv
    writer.writeheader() 
    for j in plist : 
        writer.writerow(j) #iterate through each map in plist and write that map in csv
    print('DONE')


    