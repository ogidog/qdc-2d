create language c
	validator pg_catalog.fmgr_c_validator;

comment on language c is 'dynamically-loaded C functions';

