import requests
from bs4 import BeautifulSoup
import smtplib
import time
#URL for what we want to scrape
URL = 'https://www.amazon.com/nuphy-Halo65-Bluetooth%E3%80%812-4G-Connection%EF%BC%8CCompatible-Windows-White/dp/B0BJTS6VC7/ref=sr_1_4?crid=2YZJ3Y9UH6FN4&keywords=nuphy%2Bhalo65&qid=1679023863&sprefix=nuphy%2Bhalo6%2Caps%2C147&sr=8-4&th=1'
#google user-agent
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
priceCheck = 150

#pulls all the data from the website

def checkPrice():
    page = requests.get(URL,headers = headers)
    soup= BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id = "productTitle").get_text()
    #this value is a string
    price = soup.find(id = "priceblock_ourprice").get_text()

    convertedPrice = float(price[-3:])
    if (convertedPrice < priceCheck):
        sendMail()
        

def sendMail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('myricktaylor@gmail.com','Dollylulu!1')
    
    subject = 'Price Fell Down!'
    body = 'Check the amazon link' + URL
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail('myricktaylor@gmail.com','taylormyrick@gmail.com'
                ,msg)
    print('email sent!')
    
    server.quit()    
    
    

def main():
    while(1):
        checkPrice()
        time.sleep(86400)
if __name__ == '__main__':
    main()