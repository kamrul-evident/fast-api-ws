from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


# Define a base class for all the ORM models to inherit from.
class Base(DeclarativeBase):
    pass


# Define the User class representing the 'users' table in the database.
class User(Base):
    __tablename__ = "users"  # Table name in the database

    # Define the columns in the 'users' table
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )  # Primary key and index on 'id'
    name: Mapped[str] = mapped_column(
        String(30), index=True
    )  # 'name' is a string with a max length of 30
    fullname: Mapped[Optional[str]]  # Optional 'fullname' (could be NULL)

    # Define the relationship with the Address model (one-to-many relationship)
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete, delete-orphan"
    )

    # String representation of the User instance
    def __repr__(self):
        return f"<User(name={self.name!r}, fullname={self.fullname!r})>"


# Define the Address class representing the 'address' table in the database.
class Address(Base):
    __tablename__ = "address"  # Table name in the database

    # Define the columns in the 'address' table
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )  # Primary key and index on 'id'
    email: Mapped[str]  # 'email' is a string field
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id")
    )  # Foreign key to 'users' table
    user: Mapped[User] = relationship(
        back_populates="addresses"
    )  # One-to-many relationship with User

    # String representation of the Address instance
    def __repr__(self):
        return f"<Address(email={self.email!r})>"


# Create an SQLite in-memory database for this example
engine = create_engine("sqlite://", echo=True)

# Create the tables in the database based on the defined models
Base.metadata.create_all(engine)

# Start a session to interact with the database
with Session(engine) as session:
    # Create two user instances with their respective addresses
    kamrul = User(
        name="Kamrul",
        fullname="Kamrul Hasan",
        addresses=[
            Address(email="kamrul@example.com"),
            Address(email="kamrul@evidentbd.com"),
        ],
    )

    john = User(
        name="John", fullname="John Doe", addresses=[Address(email="john@example.com")]
    )

    # Add both user instances to the session (queue them for database insertion)
    session.add_all([kamrul, john])

    # Commit the session to persist the data in the database
    session.commit()

    # Query and print the users and their addresses from the database
    for user in session.query(User):  # Loop through all users
        print(user)  # Print the user instance
        for address in user.addresses:  # Loop through each user's addresses
            print(address)  # Print each address

# Select data using a simple select query
print("Get data using Simple Select")
# Create a select statement to filter users by name
session = Session(engine)
stmt = select(User).where(
    User.name.in_(["Kamrul", "john"])
)  # Filter users with names 'Kamrul' or 'John'

# Execute the query and print the results
for user in session.scalars(stmt):  # Iterate over the selected users
    print(user)  # Print the user

# Select with a join to get an address associated with a user
# The join is made between Address and User based on the foreign key
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "Kamrul")
    .where(Address.email == "kamrul@example.com")
)
kamrul_address = session.scalars(stmt).first()  # Get the first matching address
print(kamrul_address)  # Print the address

# Query a single user by name 'John'
stmt = select(User).where(User.name == "John")
john = session.scalars(
    stmt
).one()  # Get exactly one result (or raise an error if there are not exactly one)
print(john)  # Print the user

# Add a new address for 'John'
john.addresses.append(
    Address(email="john1@example.com")
)  # Append a new address to the 'addresses' list
session.commit()  # Commit the transaction to persist the change

# Fetch the updated 'John' user from the database (with ID 2, assuming ID starts from 1)
john = session.get(User, 2)  # Retrieve the user with ID=2
john.addresses.remove(john.addresses[0])  # Remove the first address from John's list
session.flush()  # Flush the changes to the database (but don't commit yet)

# Delete the user 'john' from the database
session.delete(john)  # Delete the 'john' instance
session.commit()  # Commit the transaction to permanently delete the user
