import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from mock import patch

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

@pytest.fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

@patch('loguru.logger.info')
def test_insert_user(mock_logger, in_memory_db):
    logger.info("Inserting a new user")
    new_user = User(name='John Doe')
    in_memory_db.add(new_user)
    in_memory_db.commit()

    user = in_memory_db.query(User).filter_by(name='John Doe').first()

    # Test the inserted user
    assert user is not None
    assert user.name == 'John Doe'

    # Ensure logger.info was called with the correct message
    mock_logger.assert_called_with("Inserting a new user")
