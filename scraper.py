# Program to track prices from retailers and send email when price drops occur
# Author: Daniel Hirt

# TODO:
# Simply HTML scraping process to allow for easy integration of other retail websites.
# Create functionality to set frequency of price drop to check against (i.e send email when price drops $50 and check current price against this), rather
# than hard code values in if statement. 
# Provide support for other email servers. 

# SETUP:
# (1) Add desired products to 'URLs" variable.
# (2) Set value to check 'converted_price' against.
# (3) Provide email to send alerts to, along with Google app password to let applications access your email (can be found in gmail account/privacy settings).
# (4) Set frequency to check for price drops - currently checking daily.

import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {"User-Agent "  :  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36', 'Cache-Control': 'no-cache', "Pragma": "no-cache"}

def check_price():

# Array of URls to check prices for
  URLs = ['https://amzn.to/2T1C8gy', 'https://amzn.to/2MCFTYG']
  

# Iterate over URls and check prices for each
  for url in URLs:
          
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'lxml')

    # Find product title HTML as defined by Amazon
    title = soup.find(id="productTitle").get_text()
    # Find price for product HTML as defined by Amazon
    price = soup.find(id="priceblock_ourprice").get_text()
    parsedPrice = price.replace(',', '.')
    # Current price of product recieved from HTML tag
    converted_price = float(parsedPrice[1:6])

    print(f"Price of item: {converted_price}")

# Send email if price has dropped below desired price
    if (converted_price < 1.200 or converted_price < 600.00):
        send_mail(title, url)

# Send email functionality        
def send_mail(title, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Set email address (your email) and generated password
    server.login('EMAIL', 'GOOGLE APP PASSWORD')
    subject = f"Price fell down for: {title}"
    body = f"Check the Amazon link: {url}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'EMAIL',
        'EMAIL',
        msg
    )
    print('EMAIL SENT')

    server.quit()

# Execute the code daily to check for price drops
while(True):
    check_price()
    time.sleep(86400)
