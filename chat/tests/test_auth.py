from chat_server.auth import hash_password, verify_password


def test_hash_returns_string():
    result = hash_password("secret123")
    assert isinstance(result, str)
    assert result != "secret123"


def test_hash_diff_each_time():
    hash1 = hash_password("secret123")
    hash2 = hash_password("secret123")

    assert hash1 != hash2


def test_verify_correct_password():
    hash1 = hash_password("secret123")
    assert verify_password("secret123", hash1) == True


def test_verify_wrong_password():
    hash1 = hash_password("secret123")
    assert verify_password("wrong_password", hash1) == False
