create extension plpgsql
schema pg_catalog
version '1.0';

comment on extension plpgsql is 'PL/pgSQL procedural language';

create trusted language plpgsql
	handler pg_catalog.plpgsql_call_handler
	inline pg_catalog.plpgsql_inline_handler
	validator pg_catalog.plpgsql_validator;

comment on language plpgsql is 'PL/pgSQL procedural language';

