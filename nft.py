from asyncio.windows_events import NULL
from attr import attrs
import time
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

plist = []  #empty list declaed which will contain dictionaries of each nft

URL = "https://nft.wazirx.org/discover?sort=recent-desc"


def selenium_work(website_url):
    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(website_url)
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html5lib') #website content
    return soup

soup1 = selenium_work(URL)


for row in soup1.findAll('div', attrs = {'class':'sc-GvhzO dJLfZQ token-card'}):   #each row starting with div and have this class name

    token_link = row.find('a', attrs= {'class':'token-card--link'})['href']
    
    title = row.find('h2', attrs= {'class':'sc-dFRpbK eKnEFZ token-card__title'}).get_text()

    # owner = row.find('a', attrs= {'class':'avatar'}).get_text()
    # if(owner==NULL):
    #     owner = row.find('a', attrs= {'class':'avatar'}).find('div', attrs= {'class':'avatar__info'}).get_text()

    price = row.find('div', attrs= {'class':'token-card__price--wrapper--1'}).get_text()

    print(title, price)

    soup2 = selenium_work("https://nft.wazirx.org"+token_link)
    # nft_token = soup2.find('main', attrs= {'class':'ant-layout-content'})
    # print(soup2.prettify())
    try:
        img_link = soup2.find('img', attrs= {'class':'asset-img-wrapper bid-token__asset-wrapper--asset-fit'})['src']
    except:
        img_link = 'unable to fetch'
    print(img_link)
    creator = soup2.findAll('a', attrs= {'class':'avatar'})[0].find('div', class_='avatar__info--title-wrapper').get_text()
    owner = soup2.findAll('a', attrs= {'class':'avatar'})[1].find('div', class_='avatar__info--title-wrapper').get_text()
    # creator = soup2.find('a', attrs= {'class':'avatar', 'alt':'Creator'}).find('div', class_='avatar__info--title-wrapper').get_text()
    
    print('CREATOR - '+creator, 'OWNER - '+owner)

    print(' TRADE HISTORY - ')
    historyList = []
    token_history_list = soup2.find('div', attrs= {'class':'token-history--list'})
    for history in token_history_list.findAll('div', attrs= {'class':'token-list-item'}):
        trade = history.find('div', class_='token-list-item--transaction-details').get_text() + ' for ' + history.find('div', class_='token-list-item--amount').get_text() 
        print(trade)
        historyList.append(trade)
    # plist.append({'RANK':rank, 'NAME':name, 'NETWORTH':networth})

    desc = soup2.find('div', class_='token-history--content').get_text()

    plist.append({'TITLE':title, 'PRICE':price, 'CREATOR':creator, 'OWNER':owner, 'IMAGE':img_link, 'DESCRIPTION':desc, 'HISTORY':historyList, 'LINK':"https://nft.wazirx.org"+token_link})


#TO WRITE LIST ON EXCEL

with open('NFT_list_NEW.csv','w') as f: #open file to write

    details = ['TITLE','PRICE','CREATOR','OWNER','IMAGE','DESCRIPTION','HISTORY','LINK'] #field names
    writer = csv.DictWriter(f,fieldnames= details) #to write dict to csv
    writer.writeheader() 
    for j in plist : 
        writer.writerow(j) #iterate through each map in plist and write that map in csv
    print('DONE')


    