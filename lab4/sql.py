import sqlite3

# Create a new database if the database doesn't already exist
with sqlite3.connect('userstest.db') as conn:
    # Get a cursor object
    cursor = conn.cursor()

# Create the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id int AUTO_INCREMENT PRIMARY KEY,
        username varchar(255) NOT NULL,
        password varchar(255) NOT NULL,
        salt varchar(255) NOT NULL
    );
''')
# Commit the change
conn.commit()

commands = ["INSERT INTO users (username, password, salt) VALUES ('bsea', 'PANDAS!', 'BAMBOO');",
            "INSERT INTO users (username, password, salt) VALUES ('hubbard', 'Gully', 'Battle');",
            "INSERT INTO users (username, password, salt) VALUES ('cantwell', 'HCIwoot', 'mices');",
            "INSERT INTO users (username, password, salt) VALUES ('happer', 'ateapples', 'mooses');"]
for command in commands:
    cursor.execute(command)
conn.commit()

res = cursor.execute('SELECT * FROM users')
conn.commit()
print(len(res.fetchall()))

res = cursor.execute('''
CREATE TABLE IF NOT EXISTS profiles (
	id int AUTO_INCREMENT PRIMARY KEY,
   	userid int NOT NULL,
	color varchar(255) NOT NULL,
	hand varchar(255) NOT NULL,
	dept varchar(255) NOT NULL,
	[group] int NOT NULL DEFAULT 5
);
''')
conn.commit()

commands = ["insert into profiles(userid, color, hand, dept) values ((SELECT rowid FROM users WHERE username='happer'),'red', 'left', 'science');",
            "insert into profiles(userid, color, hand, dept, [group]) values ((SELECT rowid FROM users WHERE username='hubbard'),'red', 'right', 'math', 20);",
            "insert into profiles(userid, color, hand, dept, [group]) values ((SELECT rowid FROM users WHERE username='bsea'),'green', 'right', 'ecs', 22);",
            "insert into profiles(userid, color, hand, dept, [group]) values ((SELECT rowid FROM users WHERE username='cantwell'),'purple', 'ambi', 'humanities', 12);"]
for command in commands:
    cursor.execute(command)
conn.commit()

'''
SELECT color, dept FROM profiles;

8.
SELECT * FROM profiles WHERE hand='right';

9. 
SELECT * FROM profiles INNER JOIN users ON profiles.userid = users.rowid WHERE length(password) > 6 AND hand='right';

10.
SELECT username FROM profiles INNER JOIN users ON profiles.userid = users.rowid WHERE substr(salt,1,1)='B' AND [group] > 10 ORDER BY username ASC;
'''
res = cursor.execute('SELECT color, dept FROM profiles')
print(res.fetchall())
res = cursor.execute('SELECT * FROM profiles WHERE hand="right"')
print(res.fetchall())
res = cursor.execute('SELECT * FROM profiles INNER JOIN users ON profiles.userid = users.rowid WHERE length(password) > 6 AND hand="right"')
print(res.fetchall())
res = cursor.execute('SELECT username FROM profiles INNER JOIN users ON profiles.userid = users.rowid WHERE substr(salt,1,1)="B" AND [group] > 10 ORDER BY username ASC')
print(res.fetchall())
conn.close()dbcommands.txt 
