from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


if __name__ == "__main__":
    Base = declarative_base()

    # Define a class that maps to the users table.
    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        name = Column(String)

    # Create an SQLite database in memory.
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    # Create a session used to interact with the database.
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a new user.
    new_user = User(name="Ahmed")
    session.add(new_user)
    session.commit()

    # Query the database.
    user = session.query(User).first()
    if user:
        print(f"User ID: {user.id}")
        print(f"User name: {user.name}")
