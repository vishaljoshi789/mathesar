from django.db import transaction
from django.conf import settings

from db import install
from mathesar.models.base import Server, Database, Role, UserDatabaseRoleMap
from mathesar.models.deprecated import Connection
from mathesar.models.users import User
from mathesar.utils.connections import BadInstallationTarget

INTERNAL_DB_KEY = 'default'


@transaction.atomic
def migrate_connection_for_user(connection_id, user_id):
    """Move data from old-style connection model to new models."""
    conn = Connection.current_objects.get(id=connection_id)
    server, database, role = _setup_connection_models(
        conn.host, conn.port, conn.db_name, conn.username, conn.password
    )
    return UserDatabaseRoleMap.objects.create(
        user=User.objects.get(id=user_id),
        database=database,
        role=role,
        server=server
    )


@transaction.atomic
def set_up_new_database_on_internal_server(database_name):
    """Create a database on the internal server, install Mathesar."""
    conn_info = settings.DATABASES[INTERNAL_DB_KEY]
    if database_name == conn_info["NAME"]:
        raise BadInstallationTarget(
            "Mathesar can't be installed in the internal database."
        )
    _setup_connection_models(
        conn_info["HOST"],
        conn_info["PORT"],
        conn_info["NAME"],
        conn_info["USER"],
        conn_info["PASSWORD"],
    )
    install.install_mathesar(
        database_name,
        conn_info["USER"],
        conn_info["PASSWORD"],
        conn_info["HOST"],
        conn_info["PORT"],
        True,
        root_db=conn_info["NAME"],
    )



def _setup_connection_models(host, port, db_name, role_name, password):
    server, _ = Server.objects.get_or_create(host=host, port=port)
    database, _ = Database.objects.get_or_create(name=db_name, server=server)
    role, _ = Role.objects.get_or_create(
        name=role_name,
        server=server,
        defaults={"password": password},
    )
    return server, database, role
