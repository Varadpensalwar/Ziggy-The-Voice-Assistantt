import csv
import sqlite3

con = sqlite3.connect("ziggy.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 30]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

def add_sys_command(name, path):
    con = sqlite3.connect("ziggy.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (name.lower(), path))
    con.commit()
    con.close()
    print(f"Added sys_command: {name} -> {path}")

def add_web_command(name, url):
    con = sqlite3.connect("ziggy.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO web_command (name, url) VALUES (?, ?)", (name.lower(), url))
    con.commit()
    con.close()
    print(f"Added web_command: {name} -> {url}")

if __name__ == "__main__":
    add_sys_command('vs code', r'C:\Users\DELL\AppData\Local\Programs\Microsoft VS Code\Code.exe')
    add_sys_command('chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe')
    add_sys_command('notepad', r'C:\Windows\System32\notepad.exe')
    add_web_command('github', 'https://github.com')
    add_web_command('google', 'https://www.google.com')
    add_web_command('youtube', 'https://www.youtube.com')
    print('Common commands added!')