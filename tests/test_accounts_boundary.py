"""Additional request-level checks for the implemented account boundary."""

from app import database
from contracts.test_accounts import csrf, login, register


def test_expired_database_session_denies_api_and_redirects_html(client, settings):
    """A still-signed cookie cannot override server-side session expiry."""
    register(client)
    login(client)
    assert client.get("/api/me").status_code == 200
    with database.connect(settings) as connection:
        connection.execute("UPDATE sessions SET expires_at = 0")
    assert client.get("/api/me").status_code == 401
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_html_signup_rejects_role_input(client, settings):
    """The HTML path also rejects attempts to choose an administrative role."""
    token = csrf(client)["X-CSRF-Token"]
    response = client.post(
        "/signup",
        data={
            "username": "html_member",
            "password": "a disposable test password",
            "role": "admin",
            "csrf_token": token,
        },
    )
    assert response.status_code == 422
    with database.connect(settings) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
