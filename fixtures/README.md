# mock-data

This is a directory to support local development with postgres.

The .sql files in this directory will be executed upon first startup of the postgres image in docker-compose. It must be mounted to /docker-entrypoint-initdb.d, and the database must be completely empty for this to take effect.

For more information see https://github.com/docker-library/docs/blob/master/postgres/README.md

**If you have a postgres instance to connect the app too, change DATABASE_URL to point to the database and disregard this directory.**
