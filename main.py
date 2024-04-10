import sqlite3
import time

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Define the SQL queries
sql_query1 = '''
SELECT R1.x1, R1.x2, R2.x3
FROM R1
JOIN R2 ON R1.x2 = R2.x2  -- Step 1: Compute R1 JOIN R2
EXCEPT
SELECT R1_prime.x1, R1_prime.x2, R2_prime.x3
FROM R1_prime
JOIN R2_prime ON R1_prime.x2 = R2_prime.x2;  -- Step 2: Compute R1_prime JOIN R2_prime
'''

sql_query2 = '''
SELECT R1_minus_R1_prime.x1, R1_minus_R1_prime.x2, R2.x3
FROM (
    SELECT R1.x1, R1.x2
    FROM R1
    EXCEPT
    SELECT R1_prime.x1, R1_prime.x2
    FROM R1_prime
) AS R1_minus_R1_prime  -- Step 1: Compute R1 - R1_prime
JOIN R2 ON R1_minus_R1_prime.x2 = R2.x2  -- Step 3: Compute (R1 - R1_prime) JOIN R2
UNION -- Step 5: Union of resulting two tables
SELECT R1.x1, R1.x2, R2_minus_R2_prime.x3
FROM R1
JOIN (  -- Step 4: Compute R1 JOIN (R2 - R2_prime)
    SELECT R2.x2, R2.x3
    FROM R2
    EXCEPT
    SELECT R2_prime.x2, R2_prime.x3
    FROM R2_prime
) AS R2_minus_R2_prime ON R1.x2 = R2_minus_R2_prime.x2;  -- Step 2: Compute R2 - R2_prime
'''

# Run each query multiple times and measure execution time
num_runs = 10000
total_time_query1 = 0
total_time_query2 = 0

print("Results of Query 1:")
cursor.execute(sql_query1)
results_query1 = cursor.fetchall()
for row in results_query1:
    print(row)

print("\nResults of Query 2:")
cursor.execute(sql_query2)
results_query2 = cursor.fetchall()
for row in results_query2:
    print(row)

for _ in range(num_runs):
    start_time = time.time()
    cursor.execute(sql_query1)
    end_time = time.time()
    total_time_query1 += end_time - start_time

    start_time = time.time()
    cursor.execute(sql_query2)
    end_time = time.time()
    total_time_query2 += end_time - start_time

# Calculate average time taken for each query
avg_time_query1 = total_time_query1 / num_runs
avg_time_query2 = total_time_query2 / num_runs

# Calculate the relative speedup of Query 2 over Query 1
speedup_factor = avg_time_query1 / avg_time_query2

print(f"\nAverage time taken for Query 1: {avg_time_query1:.9f} seconds")
print(f"Average time taken for Query 2: {avg_time_query2:.9f} seconds")

if speedup_factor > 1:
    print(f"Query 2 was {speedup_factor:.2f} times faster than Query 1.")
elif speedup_factor < 1:
    print(f"Query 1 was {1/speedup_factor:.2f} times faster than Query 2.")
else:
    print("Both queries had similar execution times.")

# Close the database connection
conn.close()