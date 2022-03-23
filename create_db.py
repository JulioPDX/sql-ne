#!/usr/bin/env python

import sqlite3
from napalm import get_network_driver
from rich import print
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn = sqlite3.connect(":memory:")

cursor = conn.cursor()

tables = [
    "CREATE TABLE platforms(id INTEGER NOT NULL PRIMARY KEY, platform_name TEXT NOT NULL)",
    "CREATE TABLE devices(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, mgmt_v4 TEXT, platform_id INTEGER, FOREIGN KEY(platform_id) REFERENCES platforms(id) ON UPDATE CASCADE ON DELETE SET NULL)",
]

devices = [
    "INSERT INTO devices(name, mgmt_v4, platform_id) VALUES('eos1', '192.168.10.143', 2)",
    "INSERT INTO devices(name, mgmt_v4, platform_id) VALUES('eos2', '192.168.10.151', 2)",
    "INSERT INTO devices(name, mgmt_v4, platform_id) VALUES('cx', '192.168.10.30', 3)",
]

platforms = (
    "INSERT INTO platforms(platform_name) VALUES ('srlinux'), ('eos'), ('aoscx')"
)

# Creating tables
for table in tables:
    cursor.execute(table)

# Creating devices and platforms
for device in devices:
    cursor.execute(device)

cursor.execute(platforms)

# Simple search on created data
all_platforms = cursor.execute("SELECT * FROM platforms").fetchall()
print(all_platforms)

all_devices = cursor.execute(
    "SELECT * FROM devices JOIN platforms ON devices.platform_id = platforms.id"
).fetchall()
print(all_devices)

# Commit before closing to save
conn.commit()
conn.close()

### Sample connection to devices

for device in all_devices:
    driver = get_network_driver(device[5])
    conn = driver(hostname=device[2], username="admin", password="admin")
    conn.open()
    facts = conn.get_facts()
    conn.close()
    print(facts)