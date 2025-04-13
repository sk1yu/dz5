import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def create_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            temperature REAL
        )
    ''')
    conn.commit()
    conn.close()


def get_temperature():
    url = 'https://example-weather-site.com'  
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    temp_element = soup.find('span', class_='current-temp')
    if temp_element:
        temperature = float(temp_element.text.replace('°C', '').strip())
        return temperature
    else:
        return None


def insert_data(temperature):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO weather (datetime, temperature) VALUES (?, ?)', (current_time, temperature))
    conn.commit()
    conn.close()


def main():
    create_db()
    try:
        while True:
            temperature = get_temperature()
            if temperature is not None:
                insert_data(temperature)
                print(f"{datetime.now()}: Температура {temperature}°C добавлена в БД.")
            else:
                print("Не удалось получить температуру.")
            time.sleep(1800)  
    except KeyboardInterrupt:
        print("Программа остановлена пользователем.")

if __name__ == "__main__":
    main()
