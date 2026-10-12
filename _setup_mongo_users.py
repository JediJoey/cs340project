"""One-time MongoDB user bootstrap for the CS-340 project.

Run while mongod is started WITHOUT access control. Creates an admin
root user and the 'aacuser' account (readWrite on the 'aac' database).
This script is for local setup only and is not part of the deliverable.
"""

from pymongo import MongoClient
from pymongo.errors import OperationFailure


def ensure_user(db, user, pwd, roles):
    try:
        db.command("createUser", user, pwd=pwd, roles=roles)
        print(f"Created user '{user}' on db '{db.name}'.")
    except OperationFailure as err:
        if "already exists" in str(err):
            print(f"User '{user}' already exists on db '{db.name}'.")
        else:
            raise


def main():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    # Admin root account for database administration.
    ensure_user(
        client["admin"],
        "admin",
        "adminpass",
        [{"role": "root", "db": "admin"}],
    )
    # Application account used by the CRUD module / test notebook.
    ensure_user(
        client["aac"],
        "aacuser",
        "SNHU1234",
        [{"role": "readWrite", "db": "aac"}],
    )
    print("User setup complete.")


if __name__ == "__main__":
    main()
