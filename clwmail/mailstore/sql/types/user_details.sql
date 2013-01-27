DROP TYPE user_details CASCADE;

CREATE TYPE user_details as (
    userid VARCHAR,
    created TIMESTAMP,
    password VARCHAR,
    home VARCHAR,
    domain VARCHAR,
    uid INTEGER,
    gid INTEGER,
    status INTEGER,
    typer VARCHAR,
    role VARCHAR,
    fullname VARCHAR,
    notes VARCHAR,
    holidaymsg VARCHAR,
    holidayend VARCHAR,
    leavedate DATE,
    leavemsg TEXT,
    b_isadmin BOOLEAN,
    default_message TEXT
);

