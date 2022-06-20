create table qdc_2d.results
(
	user_id text not null
		constraint results_pkey
			primary key,
	task_id text not null,
	module_name varchar(256),
	images bytea[],
	briefs json[]
);

alter table qdc_2d.results owner to geodynamic_usr;

