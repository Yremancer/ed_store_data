from exceptions import AdminCreationError
from superset import db
from superset.app import create_app
from superset.extensions import appbuilder
from superset.utils.database import get_or_create_db
from superset_config import settings


def main() -> None:
    clickhouse_uri = settings.clickhouse_url.render_as_string(hide_password=False)

    app = create_app()
    with app.app_context():
        security = appbuilder.sm
        username = settings.SUPERSET_ADMIN_USER
        if security.find_user(username=username) is None:
            admin = security.add_user(
                username=username,
                first_name=settings.SUPERSET_ADMIN_FIRST_NAME,
                last_name=settings.SUPERSET_ADMIN_LAST_NAME,
                email=settings.SUPERSET_ADMIN_EMAIL,
                role=security.find_role(app.config["AUTH_ROLE_ADMIN"]),
                password=settings.SUPERSET_ADMIN_PASSWORD.get_secret_value(),
            )
            if not admin:
                raise AdminCreationError(
                    f"Could not create the Superset administrator {username!r}"
                )

        connection = get_or_create_db("ClickHouse", clickhouse_uri)
        connection.expose_in_sqllab = True
        db.session.commit()


if __name__ == "__main__":
    main()
