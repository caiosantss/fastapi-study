from jwt import decode

from app.security import create_access_token, settings


def test_token():
    data = {'test': 'test'}

    token = create_access_token(data=data)
    decoded = decode(
        jwt=token,
        algorithms=settings.ALGORITHM,
        key=settings.SECRET_KEY,
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded.keys()
