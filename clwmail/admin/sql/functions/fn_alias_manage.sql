/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_alias_manage.sql
	Function description:  . Create, modify or delete aliases
							 Returns <1 failure, 1 success on delete
							 mode 1: create
							 mode 2: modify user details
							 mode 3: delete
	Date started:          . 27 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_alias_manage (integer, varchar, varchar, varchar, varchar) RETURNS integer
AS '
DECLARE
	
	mode               ALIAS for $1;
	in_alias   	   	   ALIAS for $2;
	in_domain          ALIAS for $3;
	in_alias_newname   ALIAS for $4;
	in_notes           ALIAS for $5;

	aliascheck         VARCHAR := '''';
	
	function_name	VARCHAR := ''fn_alias_manage'';
	
BEGIN

-- Authentication checks

	IF mode IS NULL THEN
		RAISE EXCEPTION ''usr_alias_a : No mode provided'';
		RETURN 0;
	END IF;

	IF in_alias IS NULL THEN
		RAISE EXCEPTION ''usr_alias_b : No alias provided'';
		RETURN 0;
	END IF;

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''usr_alias_c : No domain provided'';
		RETURN 0;
	END IF;

	IF mode = 2 THEN

		IF in_alias_newname IS NULL THEN
			RAISE EXCEPTION ''usr_alias_d : new name not provided'';
			RETURN 0;
		END IF;

	END IF;

	-- add an alias
	IF mode = 1 THEN

		SELECT INTO aliascheck
			alias
		FROM
			aliases
		WHERE
			alias = lower(in_alias)
			AND
			domain = lower(in_domain);

		IF FOUND THEN
			RAISE EXCEPTION ''usr_alias_e : alias already exists'';
			RETURN 0;
		END IF;
		
		INSERT INTO aliases
			(alias, domain, notes) 
		VALUES
			(lower(in_alias), lower(in_domain), in_notes);

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_alias_f : alias name could not be added'';
			RETURN 0;
		END IF;
		
	-- modify an alias
	ELSIF mode = 2 THEN

		UPDATE 
			aliases
		SET
			alias = lower(in_alias_newname),
			notes = in_notes
		WHERE
			alias = lower(in_alias)
			AND
			domain = lower(in_domain);

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_alias_g : alias name could not be changed'';
			RETURN 0;
		END IF;

	-- delete an alias
	ELSIF mode = 3 THEN
		
		DELETE FROM
			aliases
		WHERE
			alias = lower(in_alias)
			AND
			domain = lower(in_domain);

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_alias_g : alias could not be deleted'';
			RETURN 0;
		END IF;

	ELSE

		RAISE EXCEPTION ''usr_alias_h : Invalid mode given'';
		RETURN 0;

	END IF;

	RETURN 1;

END;'
    LANGUAGE plpgsql;

