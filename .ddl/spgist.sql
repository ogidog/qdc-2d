create access method spgist
type index
handler pg_catalog.spghandler;

comment on access method spgist is 'SP-GiST index access method';

