DROP TYPE alias_type CASCADE;

CREATE TYPE alias_type as (
    aliasname VARCHAR,
    domainname VARCHAR,
    created  TIMESTAMP,
    notes  	 VARCHAR
);

