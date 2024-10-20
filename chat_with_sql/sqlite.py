import sqlite3

#connect to sqlite
connection = sqlite3.connect('chat_with_sql/student.db')

#create a cursor object to insert record, create table
cursor = connection.cursor()

#create table
table_info = """
CREATE TABLE student(
    name VARCHAR(255),
    class VARCHAR(25),
    section VARCHAR(25),
    marks INT
)
"""

cursor.execute(table_info)

#Insert some more records
cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

#display all records
print('The inserted records are:')
data = cursor.execute('SELECT * FROM student')
for row in data:
    print(row)
    
#commit changes in the database
connection.commit()
connection.close()