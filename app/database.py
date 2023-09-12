import sqlite3

# Connect to the fitBot.db database
conn = sqlite3.connect("app/fitBot.db")

# Create a cursor object to execute SQL statements
c = conn.cursor()

# Create DimUser table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS DimUser (
UserID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(100),
PasswordValue VARCHAR(100),
Email VARCHAR(100)
);"""
)

# Create DimProfile table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS DimProfile (
ProfileID INTEGER PRIMARY KEY AUTOINCREMENT,
UserID INTEGER,
Gender VARCHAR(100),
WeightValue FLOAT,
Height FLOAT,
Goal VARCHAR(100),
Diet VARCHAR(100),
WorkOutDays INTEGER,
WorkOutMin INTEGER,
AccessGym VARCHAR(3),
TimeValue TIMESTAMP NOT NULL,
FOREIGN KEY (UserID) REFERENCES DimUser(UserID)
);"""
)

# Create FactConversation table if it doesn't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS FactConversation (
MessageID INTEGER PRIMARY KEY AUTOINCREMENT,
UserID INTEGER,
Role VARCHAR(20) NOT NULL,
Content VARCHAR(5000) NOT NULL,
TimeValue TIMESTAMP NOT NULL,
MessageType INTEGER DEFAULT 0,
FOREIGN KEY (UserID) REFERENCES DimUser(UserID)
);"""
)


# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
