from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    # One to one relationshop with profile
    profile = relationship("Profile", uselist=False, back_populates="user")
    # One to many relationship with posts
    posts = relationship("Post", back_populates="user")
    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    bio = Column(String)

    # Defines a relationship to the User class
    user = relationship("User", back_populates="profile")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    user = relationship("User", back_populates="posts")


engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)


# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create an instance of the User
user = User(
    name="Kamrul Hasan",
    age=30,
    profile=Profile(bio="I am a software engineer")
)


session.add(user)
session.commit()

# Get all users
users = session.query(User).all()
for user in users:
    print(user.name, user.age)

# Get a single user by ID
user = session.query(User).filter_by(id=1).first()
print(user)

# Using relationships
user_profile = session.query(User).filter_by(id=1).first().profile
print(user_profile.bio)

# Create a new user record
new_user = User(name="John Doe", age=25)
# Create posts associated with the user
post1 = Post(title="Alice's first post", user=new_user)
post2 = Post(title="Kamrul's first post", user_id=user.id)

session.add(new_user)
session.add(post1)
session.add(post2)
session.commit()

# Update an existing record
user = session.query(User).filter_by(id=1).first()
user.name = "Md. Kamrul Hasan"
session.commit()

# Delete a record
user = session.query(User).filter_by(id=5).first()
session.delete(user)
session.commit()


session.close()