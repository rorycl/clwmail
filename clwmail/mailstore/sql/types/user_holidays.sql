DROP TYPE user_holidays CASCADE;

CREATE TYPE user_holidays as (
	holid    INTEGER,
	holstart timestamp,
	holend   timestamp,
	holmsg   VARCHAR
);
