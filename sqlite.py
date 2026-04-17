import sqlite3

# connect to sqlite
connection=sqlite3.connect("student.db")

# create a cursor object to insert record,delete rcecord ,create table
cursor=connection.cursor()

# create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),
CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

cursor.execute("insert into STUDENT values('John','10th','A',85)")
cursor.execute("insert into STUDENT values('Alice','10th','B',90)")
cursor.execute("insert into STUDENT values('Bob','10th','A',78)")
cursor.execute("insert into STUDENT values('Eve','10th','B',92)")
cursor.execute("insert into STUDENT values('Charlie','10th','A',88)")

# Displaying all records
print("The inserted records are:")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
    
# commit chabgs in database
connection.commit()
connection.close()