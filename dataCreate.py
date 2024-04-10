import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create tables R1, R2, R1_prime, R2_prime if they don't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS R1 (
    x1 INT,
    x2 INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS R2 (
    x2 INT,
    x3 INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS R1_prime (
    x1 INT,
    x2 INT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS R2_prime (
    x2 INT,
    x3 INT
)""")

# Generate a pool of random x2 values
pool_of_x2_values = list(range(1, 1001))  # Assume x2 can range from 1 to 1000

# Generate random rows for R1 and R2 with overlapping x2 values
num_rows_r1 = random.randint(100, 200)
num_rows_r2 = random.randint(100, 200)
random.shuffle(pool_of_x2_values)  # Shuffle the pool of x2 values for randomness
for _ in range(num_rows_r1):
    x1 = random.randint(1, 1000)
    x2 = pool_of_x2_values.pop()  # Get a random x2 value from the pool
    cursor.execute("INSERT INTO R1 (x1, x2) VALUES (?, ?)", (x1, x2))
for _ in range(num_rows_r2):
    x2 = pool_of_x2_values.pop()  # Get another random x2 value from the pool
    x3 = random.randint(1, 1000)
    cursor.execute("INSERT INTO R2 (x2, x3) VALUES (?, ?)", (x2, x3))

# Generate random rows for R1_prime and R2_prime with some overlapping x2 values
num_rows_r1_prime = random.randint(50, 150)
num_rows_r2_prime = random.randint(50, 150)
random.shuffle(pool_of_x2_values)  # Reshuffle the pool for R1_prime and R2_prime
for _ in range(num_rows_r1_prime):
    x1 = random.randint(1, 1000)
    x2 = pool_of_x2_values.pop()  # Get a random x2 value from the shuffled pool
    cursor.execute("INSERT INTO R1_prime (x1, x2) VALUES (?, ?)", (x1, x2))
for _ in range(num_rows_r2_prime):
    x2 = pool_of_x2_values.pop()  # Get another random x2 value from the shuffled pool
    x3 = random.randint(1, 1000)
    cursor.execute("INSERT INTO R2_prime (x2, x3) VALUES (?, ?)", (x2, x3))

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()
