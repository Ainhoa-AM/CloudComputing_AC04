from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL,
    "password" VARCHAR(100) NOT NULL,
    "mail" VARCHAR(50) NOT NULL,
    "year_of_birth" INT
);
CREATE TABLE IF NOT EXISTS "files" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "filename" VARCHAR(200) NOT NULL,
    "user" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
