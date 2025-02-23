from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///blog.db", echo=True)
Base = declarative_base()

# Session for queries
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    posts = relationship("Post", backref="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(engine)

# # Add a user
# new_user = User(name="Alice", email="alice@example.com")
# session.add(new_user)
# session.commit()

# # Add a post for that user
# new_post = Post(title="Hello World", content="My first post", user_id=new_user.id)
# session.add(new_post)
# session.commit()

# users = session.query(User).all()
# for user in users:
#     print(user.name, user.email)

# user = session.query(User).filter_by(id=1).first()
# print(user.name)

# posts = session.query(Post).filter_by(user_id=user.id).all()
# for post in posts:
#     print(post.title, post.content)

# # Update user records
# user = session.query(User).filter_by(id=1).first()
# user.name = "Alicia"
# session.commit()

# # Delete a record
# post = session.query(Post).filter_by(id=2).first()
# session.delete(post)
# session.commit()

user = User(name="Bob", email="bob@example.com")
user.posts.append(Post(title="Bob's Post", content="Hi there!!!"))
session.add(user)
session.commit()

# Access related data
user = session.query(User).filter_by(id=1).first()
for post in user.posts:
    print(post.title)

post = session.query(Post).filter_by(id=1).first()
print(post.user.name)

# Like django's filter(name__startswith="A")
users = session.query(User).filter(User.name.startswith("A")).all()

# Like django's order_by("name")
users = session.query(User).order_by(User.name).all()

# Like djangos count()
user_count = session.query(User).count()
print(user_count)
