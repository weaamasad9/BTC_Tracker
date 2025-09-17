# BTC_Tracker
A simple python project that runs a script to gathering data about the BTC price each hour.

# 💰 Bitcoin Price Tracker (Python)

This project is a **Python automation tool** that tracks Bitcoin prices in real-time using the [Coinbase API](https://api.coinbase.com).  
It collects data every minute for one hour, saves it in JSON, generates a graph, and automatically emails the results with a summary report.  

---

## 🎯 Features
- Real-time **Bitcoin price fetching** via Coinbase API
- **Logging** of all actions with Python’s `logging` module
- **JSON storage** of collected data
- **Matplotlib** graph generation for visualization
- **Automated email reports** (using Gmail SMTP) with graph attachment
- Tracks BTC price **for 1 hour** and sends a summary 📧

---

## 🛠️ Technologies & Libraries
- `requests` → Fetching data from the API  
- `json` → Data serialization  
- `logging` → Action tracking  
- `matplotlib` → Graph plotting  
- `smtplib` & `email` → Gmail SMTP integration  

---

## 📂 Project Structure
bitcoin-tracker/
├── BTC.py # Main script
├── BTC_logger.log # Log file
├── BTC_price.json # Stored BTC price data
├── BTC_graph.png # Price graph

## 🧑‍💻 Skills Demonstrated
- **Python scripting & automation**
- **API integration** (REST, JSON)
- **Data visualization** with `matplotlib`
- **Email automation** using Gmail SMTP
- **Error handling & logging**
- Writing structured, maintainable code

The script will:
Collect BTC prices every minute for 60 minutes
Save them in BTC_price.json
Generate a graph BTC_graph.png
Send an email with the graph and the maximum price
