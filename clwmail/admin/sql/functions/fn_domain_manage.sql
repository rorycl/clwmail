/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_domain_manage.sql
	Function description:  . manages a domain 
	Date started:          . 12 December 2007
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_domain_manage (integer, varchar, varchar) RETURNS INTEGER 
AS '
DECLARE
	mode ALIAS FOR $1;
	in_domain ALIAS FOR $2;
	new_domain ALIAS FOR $3;

	function_name	VARCHAR := ''fn_domain_manage'';

	name_check VARCHAR;	
	user_count INTEGER;
BEGIN

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''No domain provided'';
	END IF;
	
	-- add --
	IF mode =1 THEN

		SELECT INTO 
				name_check
				domain
		FROM 
			domains
		WHERE
			domain = lower(in_domain);
	
		IF FOUND THEN
			RAISE EXCEPTION ''This domain already exists'';
			RETURN 0;

		ELSE
			INSERT INTO 
					domains	(domain) 
			VALUES 
					(lower(in_domain));
			
			RETURN 1;
		
		END IF;

	-- edit
	ELSIF mode =2 THEN
		IF new_domain IS NULL THEN
			RAISE EXCEPTION ''No new domain provided'';
		END IF;

		UPDATE 
			domains
		SET 
			domain = lower(new_domain)
		WHERE
			 domain = lower(in_domain);

		IF FOUND THEN
			RETURN 1;
		ELSE
			RETURN 0;
		END IF;
		

	-- delete 
	ELSIF mode =3 THEN
		SELECT INTO
				user_count
				count (*) 
		FROM 
			users 
		WHERE
			users.domain = lower(in_domain);

		IF user_count >0 THEN
			RAISE EXCEPTION ''This domain is referenced by users of the system and cannot be deleted.'';
			RETURN 0;
		ELSE
			DELETE FROM domains where domain = lower(in_domain);

			IF FOUND THEN
				RETURN 1;
			ELSE
				RETURN 0;
			END IF;
		END IF;

		
	END IF;
		

END;'
    LANGUAGE plpgsql;
