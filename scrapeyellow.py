
import sqlite3
import requests
from bs4 import BeautifulSoup

# Define lists of cities and states
cities = {
    'Mississippi': ['Jackson', 'Gulfport', 'Southaven', 'Biloxi', 'Hattiesburg'],
    'Kansas': ['Wichita', 'Overland Park', 'Kansas City', 'Olathe', 'Topeka'],
    'Nebraska': ['Omaha', 'Lincoln', 'Bellevue', 'Grand Island', 'Kearney'],
    'West Virginia': ['Charleston', 'Huntington', 'Morgantown', 'Parkersburg', 'Wheeling'],
    'New Hampshire': ['Manchester', 'Nashua', 'Concord', 'Derry', 'Rochester'],
    'Montana': ['Billings', 'Missoula', 'Great Falls', 'Bozeman', 'Butte'],
    'Rhode Island': ['Providence', 'Warwick', 'Cranston', 'Pawtucket', 'East Providence'],
    'South Dakota': ['Sioux Falls', 'Rapid City', 'Aberdeen', 'Brookings', 'Mitchell'],
    'Wyoming': ['Cheyenne', 'Casper', 'Laramie', 'Gillette', 'Sheridan'],
    'Vermont': ['Burlington', 'South Burlington', 'Rutland', 'Essex Junction', 'Barre']
}
specialities = ['Surgeon', 'Nurse', 'Lawyer', 'Accountant', 'Marketing', 'Engineer', 'Finance', 'Software', 'Physical+Therapist', 'Architect', 'Construction', 'Non-Profit']

# Function to generate URLs
def generate_urls(states, specialities):
    urls = []
    for state, city_list in states.items():
        for city in city_list:
            for speciality in specialities:
                url = f"https://www.yellowpages.com/search?search_terms={speciality}&geo_location_terms={city}%2C+{state}"
                urls.append(url)
    return urls

# Function to scrape data and save to SQLite database
def scrape_and_save_to_db(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    # Connect to SQLite database (creates if not exists)
    conn = sqlite3.connect('server/businesses.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS businesses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  address TEXT,
                  phone TEXT,
                  website TEXT,
                  category TEXT)''')

    listings = soup.find_all('div', class_='result')

    for listing in listings:
        name = listing.find('a', class_='business-name').text.strip()
        address_parts = listing.find_all(['div', 'p'], class_='adr')
        address = ' '.join(' '.join(part.stripped_strings) for part in address_parts)
        phone_tag = listing.find('div', class_='phones phone primary')
        phone = phone_tag.text.strip() if phone_tag else 'Phone number not available'
        website_tag = listing.find('a', class_='track-visit-website')
        website = website_tag.get('href') if website_tag else None

        # Determine category from URL
        category = [spec for spec in specialities if spec in url]
        category = category[0] if category else 'Unknown'

        # Insert data into the database
        c.execute('''INSERT INTO businesses (name, address, phone, website, category)
                     VALUES (?, ?, ?, ?, ?)''', (name, address, phone, website, category))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Scraping and saving to SQLite database completed.")

# Execute the scraping and saving function
if __name__ == "__main__":
    urls = generate_urls(cities, specialities)
    for url in urls:
        scrape_and_save_to_db(url)
