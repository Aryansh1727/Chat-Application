import sqlite3

conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages")

print(f"{'ID':<5} | {'Sender':<10} | {'Message':<20} | {'Timestamp'}")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:<5} | {row[1]:<10} | {row[2]:<20} | {row[3]}")

conn.close()