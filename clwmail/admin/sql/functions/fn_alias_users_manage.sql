/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_alias_users_manage.sql
	Function description:  . add or remove a user to an alias
							 mode 1: add
							 mode 3: remove
	Date started:          . 27 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_alias_users_manage (integer, varchar, varchar, varchar) RETURNS integer
AS '
DECLARE
	
	mode               ALIAS for $1;
	in_userid          ALIAS for $2;
	in_alias           ALIAS for $3;
	in_domain          ALIAS for $4;

	useridcheck        VARCHAR := '''';
	wasfound           BOOLEAN  := false;
	
	function_name      VARCHAR := ''fn_alias_users_manage'';
	
BEGIN

-- Authentication checks

	IF mode IS NULL THEN
		RAISE EXCEPTION ''usr_alias_users_a : No mode provided'';
		RETURN 0;
	END IF;

	IF in_userid IS NULL THEN
		RAISE EXCEPTION ''usr_alias_users_b : No userid provided'';
		RETURN 0;
	END IF;

	IF in_alias IS NULL AND NOT mode = 4 THEN
		RAISE EXCEPTION ''usr_alias_users_c : No alias provided'';
		RETURN 0;
	END IF;

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''usr_alias_users_d : No domain provided'';
		RETURN 0;
	END IF;

	SELECT INTO useridcheck
		userid
	FROM
		alias_users
	WHERE
		userid = lower(in_userid)
		AND
		alias = lower(in_alias)
		AND
		domain = lower(in_domain);

	IF FOUND THEN
		wasfound := true;
	END IF;

	-- add an alias
	IF mode = 1 THEN

		IF wasfound = true THEN
			-- dont need to do anything as already exists
			RETURN 1;
		END IF;

		INSERT INTO alias_users
			(domain, alias, userid)
		VALUES
			(lower(in_domain), lower(in_alias), lower(in_userid));

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_alias_users_e : could not add user to alias'';
			RETURN 0;
		END IF;
			
	ELSIF mode = 3 THEN

		IF wasfound = false THEN
			-- dont need to do anything as userid does not exist 
			RETURN 1;
		END IF;

		DELETE FROM 
			alias_users
		WHERE
			domain = lower(in_domain)
			AND
			alias = lower(in_alias)
			AND
			userid = lower(in_userid);

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_alias_users_f : could not delete user from alias'';
			RETURN 0;
		END IF;

	-- deletes userid and domain --
	-- from all aliases --
	ELSIF mode = 4 THEN
		DELETE FROM 
			alias_users
		WHERE
			domain = lower(in_domain)
			AND
			userid = lower(in_userid);
	ELSE

		RAISE EXCEPTION ''usr_alias_users_h : Invalid mode given'';
		RETURN 0;

	END IF;

	RETURN 1;

END;'
    LANGUAGE plpgsql;

