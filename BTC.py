import requests
import json
import time
import logging
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import smtplib
from datetime import datetime
import email.message


# informations
URL = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'
FILE = 'BTC_price.json'
GRAPH_FILE = 'BTC_graph.png'
EMAIL = 'optional' # The src email  
PASSWORD = 'optional' # an passcode app key to login with    
DST_EMAIL = 'weaamasad9@gmail.com' #The dst email
LOGGER = "./BTC_logger.log"

# Remove existing handlers if there is
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
#Logger Setup 
logging.basicConfig(
    filename=LOGGER,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)   

#Fetch Bitcoin price from API
def fetch_price():
    """
    Fetch the current Bitcoin price in USD from the  API.
    Returns: The current BTC price if successful, otherwise None.
    """
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            price = float(response.json()['data']['amount'])
            logging.info("BTC price: " + str(price) ) #write info to the log
            return price
    except Exception as e:  # if there is an error throw exception
        logging.error("Error fetching BTC price: " + str(e)) #write info to the log
        return 

#save data to JSON
def save_data(data):
    """
    Save the collected BTC price data to a JSON file.

    Args:
        data (list): List of dictionaries with 'time' and 'price' keys.
    """
    try:
        with open(FILE, 'w') as f:
            json.dump({"data": data}, f, indent=4)
        logging.info("Saved data to JSON file")  #write info to the log
    except Exception as e:
        logging.error("Error saving data: " + str(e)) #write error to the log


#Create basic graph using pyplot
def create_graph(data):
    """
   Creates a time-series graph of BTC price and saves it as an image.

   Args: data: A list of dictionaries with 'time' and 'price' keys.
   """
    try:
        # Extract time and price values from data
        times = [datetime.strptime(extract['time'], '%Y-%m-%d %H:%M:%S') for extract in data]
        prices = [extract['price'] for extract in data]
        
        # Plot setup with normal size 16, 8 it can be anything similar
        plt.figure(figsize=(16, 8))
        plt.plot(times, prices, marker='o', linestyle='-' , color='black')
        
        # Graph labels and title
        plt.title('(BPI)')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        
        #Format X and Y axes
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=3))
        plt.ticklabel_format(style='plain', axis='y') # Show full numbers (not scientific)
        plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')) # Add commas to large numbers
        
        # Final layout and save
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(GRAPH_FILE)
        plt.close()  # Close the plot to free memory
        logging.info("Graph created and saved") #write info to the log
        
    except Exception as e:
        logging.error("Error creating graph: " + str(e)) #write error to the log


def send_email(max_price):
    """
    Send an email with the graph and the maximum BTC price.

    Args: max_price: The highest BTC price recorded.
    """
    try:
        # Create the email message with subject and text body
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Max BTC Price - Last Hour'
        msg['From'] = EMAIL
        msg['To'] =  DST_EMAIL
        msg.set_content("He its me weaam,\nThe maximum BTC price in the last hour was " + str(round(max_price, 2)) + '$.')

        # Attach graph image
        with open(GRAPH_FILE, 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='png', filename=GRAPH_FILE)

        # Send the email using Gmail SMTP with port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        logging.info("Email with graph and the MAX BTC price sent")  #write info to the log
        
    except Exception as e:
        logging.error("Failed to send email: " + str(e)) #write error to the log

def main():
    """
    Main function to fetch BTC prices every minute for one hour,
    save the data, and save every operation in a log file,
    generate a graph, and send a summary email with the MAX price include the graph.
    """
    data = []
    for i in range(60):  # Run for 1 hour (1 fetch per minute)
        price = fetch_price()
        if price is not None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append({'time': timestamp, 'price': price})
        time.sleep(60)  

    #run the save data function to save the info to a JSON file
    save_data(data)
    #run the create graph to genrate it with the current info in the end
    create_graph(data)

    # Find max price
    max_price = -1
    for check in data:
        if check['price'] > max_price:
            max_price = check['price']
    send_email(max_price)
    logging.shutdown()  # Ensure all logs are written before exit

if __name__ == '__main__':
    main()

