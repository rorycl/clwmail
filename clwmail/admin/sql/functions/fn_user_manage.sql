/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_manage.sql
	Function description:  . Create, modify or delete users
							 Returns <1 failure, 1 success on delete
							 mode 1: create
							 mode 2: modify user details
							 mode 3: delete
							 mode 5: active
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_user_manage (
		integer,
		varchar, varchar, varchar, varchar,
		integer, integer, 
		varchar, varchar, varchar, varchar,
		integer
		) RETURNS integer
AS '
DECLARE
	
	mode               ALIAS for $1;
	in_userid		   ALIAS for $2;
	in_domain          ALIAS for $3;
	in_password        ALIAS for $4;
	in_home            ALIAS for $5;
	in_uid             ALIAS for $6;
	in_gid             ALIAS for $7;
	in_typer           ALIAS for $8;
	in_role            ALIAS for $9;
	in_fullname        ALIAS for $10;
	in_notes           ALIAS for $11;
	in_status          ALIAS for $12;

	usercheck          VARCHAR := '''';
	
	function_name	VARCHAR := ''fn_user_manage'';
	
BEGIN

-- Authentication checks

	IF in_userid IS NULL THEN
		RAISE EXCEPTION ''usr_manage_a : No userid provided on create'';
		RETURN 0;
	END IF;

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''usr_manage_b : No domain provided on create/modify'';
		RETURN 0;
	END IF;

	IF in_status IS NULL THEN
		RAISE EXCEPTION ''usr_manage_c : No status provided on create/modify'';
		RETURN 0;
	END IF;

	IF mode = 1 or mode = 2 THEN

		IF in_password IS NULL THEN
			RAISE EXCEPTION ''usr_manage_d : No password provided on create/modify'';
			RETURN 0;
		END IF;

		IF in_home IS NULL THEN
			RAISE EXCEPTION ''usr_manage_e : No home provided on create/modify'';
			RETURN 0;
		END IF;


		IF in_uid IS NULL or in_gid IS NULL THEN
			RAISE EXCEPTION ''usr_manage_f : No uid or gid provided on create/modify'';
			RETURN 0;
		END IF;

		IF lower(in_typer) NOT IN (''person'', ''project'') THEN
			RAISE EXCEPTION ''usr_manage_g : type not specified as person or project on create/modify'';
			RETURN 0;
		END IF;

		IF in_role IS NULL THEN
			RAISE EXCEPTION ''usr_manage_h : role not specified on create/modify'';
			RETURN 0;
		END IF;

		IF in_fullname IS NULL THEN
			RAISE EXCEPTION ''usr_manage_i : role not specified on create/modify'';
			RETURN 0;
		END IF;

	END IF;

	-- add a user
	IF mode = 1 THEN

		SELECT INTO usercheck
			userid
		FROM
			users
		WHERE
			userid = lower(in_userid) 
			AND 
			domain = lower(in_domain);

		IF FOUND THEN
			RAISE EXCEPTION ''usr_manage_k : user already exists'';
			RETURN 0;
		END IF;
		
		INSERT INTO users
			(userid, password, home, domain, uid, gid, status,
			 typer, role, fullname, notes) 
		VALUES
			(lower(in_userid), in_password, in_home, lower(in_domain),
			 in_uid, in_gid, 1, in_typer, in_role, in_fullname, in_notes);
		
	-- modify a user 
	ELSIF mode = 2 THEN

		UPDATE 
			users
		SET
			password = in_password,
			home     = in_home,
			uid      = in_uid,
			gid      = in_gid,
			status   = in_status,
			typer    = in_typer,
			role     = in_role,
			notes     = in_notes,
			fullname = in_fullname
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain);

	-- delete a user
	ELSIF mode = 3 THEN
		
		DELETE FROM
			users
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain);

	-- in active switch
	ELSIF mode = 4 THEN

		UPDATE
			users
		SET
			status = 9 
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain);

	-- active switch
	ELSIF mode = 5 THEN

		UPDATE
			users
		SET
			status = 1
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain);
	ELSE

		RAISE EXCEPTION ''s_usr01_t : Invalid mode given'';
		RETURN 0;

	END IF;

	RETURN 1;

END;'
    LANGUAGE plpgsql;

