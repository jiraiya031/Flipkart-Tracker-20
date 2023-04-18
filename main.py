# Importing libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import time
from keep_alive import keep_alive
import pytz
from matplotlib.pyplot import plot, draw, show
import matplotlib.pyplot as plt


recorded_prices_black = []
recorded_prices = []
recorded_prices_blue = []
time_stamps = []

keep_alive()
# Setting up a list of products to track
products = [
    {
        "name": "SONY WH-XB910N Black",
        "url": "https://www.flipkart.com/sony-wh-xb910n-active-noise-cancellation-enabled-bluetooth-headset/p/itmd6a2096146f4d?pid=ACCGBHRAFRJAPTSX&lid=LSTACCGBHRAFRJAPTSXYCZHWT&marketplace=FLIPKART&sattr[]=color&st=color",
        "target_price": 12000
    },
    {
        "name": "SONY WH-XB910N Blue",
        "url": "https://www.flipkart.com/sony-wh-xb910n-active-noise-cancellation-enabled-bluetooth-headset/p/itm668d0bbb72e6b?pid=ACCGBHRANHMKRMDP&lid=LSTACCGBHRANHMKRMDPVSEZMG&marketplace=FLIPKART&sattr[]=color&st=color",
        "target_price": 12000
    }
    
]

# Setting up email details
sender_email = "satyam1005@yahoo.in"
sender_password = "xpgpnszxnsbwfslw"
receiver_email = "gsatyam1005@gmail.com"

# Creating an email message object
msg = EmailMessage()
msg["Subject"] = "Price Drop Alert"
msg["From"] = sender_email
msg["To"] = receiver_email

# Creating a function to send email
def send_email(product):
    # Setting up the email content
    msg.set_content(f"The price of {product['name']} has dropped below {product['target_price']}. Here is the link: {product['url']}")
    # Sending the email using SMTP and TLS
    with smtplib.SMTP("smtp.mail.yahoo.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    # Printing a confirmation message
    print(f"Email sent for {product['name']}")

# Creating a function to check price
def check_price(product,n):
    count = n
    # Getting the product page using requests
    response = requests.get(product["url"])
    # Parsing the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())
    # Finding the price element using class name
    price_element = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text(strip=True)

    # Extracting the price text and removing commas and rupee symbol
    price_element = price_element.replace(",", "").replace("₹", "")
    # Converting the price text to a float value
    price_value = float(price_element.replace(",", ""))
    # Comparing the price value with the target price
    if price_value < product["target_price"]:
        # Sending an email if the price is lower than the target
        send_email(product)
        # Returning True to indicate that the email was sent
        return True
    else:
        # Printing a message if the price is higher than the target
        print(f"The price of {product['name']} is still {price_value}")
        
       
        tz_IN = pytz.timezone('Asia/Calcutta') 

        # Get the current time in New York
        datetime_IN = datetime.now(tz_IN)

        # Format the time as a string and print it
        print("Time:", datetime_IN.strftime("%H:%M:%S"))
        #recorded_prices.append(price_value)
        # Returning False to indicate that the email was not sent
        if (count%2) == 0:
          recorded_prices_blue.append(price_value)
         
          plt.plot(time_stamps, recorded_prices_blue, color = 'blue')
          #time_stamps.append(datetime.now())
          
        else :
         recorded_prices_black.append(price_value) 
         time_stamps.append(datetime_IN)
       
         plt.plot(time_stamps, recorded_prices_black, color = 'black')
 
        
        
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title("Recorded Prices over Time")
        plt.show(block=False)
        plt.pause(1)
        return False

n=0
# Creating a while loop to run the code repeatedly
while True:
    # Looping through each product in the list
    for product in products:
        n=n+1
        # Checking the price of the product and storing the result
        result = check_price(product,n)
        # Removing the product from the list if the email was sent
        if result:
            products.remove(product)
    time.sleep(1000)
    # Breaking the loop if there are no more products to check
    if len(products) == 0:
        print(len(products))
        print("no products")
        break