from dataclasses import asdict

from sqlalchemy import select

from app.models import User


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='email@email.com', password='secret'
        )

        session.add(instance=new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'email@email.com',
        'password': 'secret',
        'updated_at': time,
        'created_at': time,
    }
