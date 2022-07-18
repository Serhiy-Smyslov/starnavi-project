from pydantic import AnyUrl


class PostgresAsync(AnyUrl):
    allowed_schemes = {'postgresql+asyncpg', }
    user_required = True
