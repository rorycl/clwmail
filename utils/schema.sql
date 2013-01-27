CREATE TABLE alias_users (
    id serial NOT NULL,
    "domain" character varying(128) NOT NULL,
    alias character varying(128) NOT NULL,
    userid character varying(128) NOT NULL
);

CREATE TABLE aliases (
    alias character varying(128) NOT NULL,
    "domain" character varying(128) NOT NULL,
    created timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    notes text
);

CREATE TABLE django_content_type (
    id serial NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);

CREATE TABLE django_site (
    id serial NOT NULL,
    "domain" character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);

CREATE TABLE domains (
    created timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    "domain" character varying(128) NOT NULL
);

CREATE TABLE holidays (
    id serial NOT NULL,
    created timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    userid character varying(128) NOT NULL,
    "domain" character varying(128) NOT NULL,
    holidaystart timestamp without time zone NOT NULL,
    holidayend timestamp without time zone NOT NULL,
    message text
);

CREATE TABLE log (
    n_id serial NOT NULL,
    dt_created timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    t_message_date character varying,
    t_message_id character varying,
    t_orig_id character varying,
    t_recipients character varying,
    t_subject character varying,
    n_size integer,
    t_from character varying,
    t_to character varying,
    t_cc character varying,
    t_md5sum character varying,
    dt_processed timestamp without time zone,
    b_processed boolean DEFAULT false
);

CREATE TABLE users (
    userid character varying(128) NOT NULL,
    created timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone,
    "password" character varying(64) NOT NULL,
    home character varying(256) NOT NULL,
    "domain" character varying(128) NOT NULL,
    uid integer NOT NULL,
    gid integer NOT NULL,
    status integer DEFAULT 1 NOT NULL,
    typer character varying(12),
    "role" character varying(64),
    fullname character varying(64),
    notes text,
    holidaymsg text,
    holidayend timestamp without time zone,
    leavedate date,
    leavemsg text,
    b_isadmin boolean DEFAULT false,
    default_message text,
    CONSTRAINT users_status CHECK (((((status = 1) OR (status = 2)) OR (status = 3)) OR (status = 9)))
);

ALTER TABLE ONLY users
    ADD CONSTRAINT userid_ukey UNIQUE (userid);

ALTER TABLE ONLY alias_users
    ADD CONSTRAINT alias_users_pkey PRIMARY KEY ("domain", alias, userid);

ALTER TABLE ONLY aliases
    ADD CONSTRAINT aliases_pkey PRIMARY KEY ("domain", alias);

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);

ALTER TABLE ONLY domains
    ADD CONSTRAINT domains_pkey PRIMARY KEY ("domain");

ALTER TABLE ONLY holidays
    ADD CONSTRAINT holidays_pkey PRIMARY KEY (id);

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (n_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("domain", userid);

ALTER TABLE ONLY users
    ADD CONSTRAINT "$1" FOREIGN KEY ("domain") REFERENCES domains("domain") ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY holidays
    ADD CONSTRAINT "$1" FOREIGN KEY ("domain", userid) REFERENCES users("domain", userid) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY aliases
    ADD CONSTRAINT "$1" FOREIGN KEY ("domain") REFERENCES domains("domain") ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY alias_users
    ADD CONSTRAINT "$1" FOREIGN KEY ("domain", userid) REFERENCES users("domain", userid) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY alias_users
    ADD CONSTRAINT "$2" FOREIGN KEY ("domain", alias) REFERENCES aliases("domain", alias) ON UPDATE CASCADE ON DELETE CASCADE;

