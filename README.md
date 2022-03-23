# Learning Some SQL

Repository used to learn a little about SQL, SQLModel, and FastAPI.

## Getting Started

If you would like to test this out or clone it to create your own, make sure to download the requirements!

```shell
sudo apt update
sudo apt install sqlite3
git clone https://github.com/JulioPDX/sql-ne.git
cd sql-ne
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Introduction to Relational Databases for Network Engineers

The `create_db.py` script was used in the initial blog post featured on [Packet Pushers](https://packetpushers.net/introduction-to-relational-databases-for-network-engineers/).

## SQLModel for Network Engineers

If you would like to mess with SQLModel, head over to the project directory and run the `app.py` script. Make sure to have sqlite3 installed!

```shell
cd project
python app.py
```

The script will create the database and all of the schema in the database. It will also create the device, platform, and VRF entries. Feel free to modify that script for the devices in your lab. This could lead to writing a script to query the database and connect to devices or configure VRFs!
