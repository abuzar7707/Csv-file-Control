import csv
import requests
from bs4 import BeautifulSoup

def write_csv():
    lim = int(input("How many rows you want: "))
    cols = int(input("How many columns you want: "))
    data = []
    headers = []
    for i in range(cols):
        col_name = input(f"Enter name for column {i + 1}: ")
        headers.append(col_name)
    data.append(headers)  # Add headers as first row

    # Get data for each row
    for row_num in range(lim):
        row_data = []
        print(f"\nEnter data for row {row_num + 1}:")
        for col in range(cols):
            value = input(f"Enter value for {headers[col]}: ")
            row_data.append(value)
        data.append(row_data)

    fname = input("\nEnter File Name (without extension): ")
    filename = fname + '.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"\nFile '{filename}' created successfully with {lim} rows and {cols} columns!")
    print("Thank You For Using!")


def append_to_csv():
    fname = input("\nEnter File Name (without extension): ").strip()
    filename = fname + '.csv'

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_columns = next(reader)  # Get header row
            num_columns = len(existing_columns)

            print("\nExisting columns in the CSV file:")
            for i, col in enumerate(existing_columns, 1):
                print(f"{i}. {col}")

        print("\nEnter new row data (comma separated values):")
        print(f"Format should match columns above: {', '.join(existing_columns)}")
        new_data_input = input("> ").strip()

        new_data = [item.strip() for item in new_data_input.split(',')]

        if len(new_data) != num_columns:
            raise ValueError(f"Error: Expected {num_columns} values, got {len(new_data)}")

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)

        print("\nSuccessfully appended new row:")
        for col, val in zip(existing_columns, new_data):
            print(f"{col}: {val}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please check the filename.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def scrape_bikes():
    keyword = input("Enter bike keyword to search: ").strip().lower()
    url = "https://www.pakwheels.com/new-bikes/pricelist"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Pakwheels bike price tables have class "table"
    tables = soup.find_all('table', class_='table')

    if not tables:
        print("No tables found on the page.")
        return

    results = []

    # Loop through all tables (each bike brand has its own table)
    for table in tables:
        rows = table.find_all('tr')
        # Skip header row (first row)
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                bike_name = cols[0].get_text(strip=True)
                bike_price = cols[1].get_text(strip=True)
                if keyword in bike_name.lower():
                    results.append([bike_name, bike_price])

    if results:
        with open('bikes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Bike Name', 'Price'])
            writer.writerows(results)

        print(f"Found {len(results)} bikes matching '{keyword}'. Data saved to bikes.csv")
    else:
        print(f"No bikes found matching '{keyword}'.")



while True:
    print("\nMenu:")
    print("1. Write a CSV file")
    print("2. Append in existing CSV file")
    print("3. Web Scraper (Bikes)")
    print("4. Exit")
    menu = input("Enter your choice: ").strip()

    if menu == '1':
        write_csv()
    elif menu == '2':
        append_to_csv()
    elif menu == '3':
        scrape_bikes()
    elif menu == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
