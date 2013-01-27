/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_active_manage.sql
	Function description:  . manage leave status for a user
							 mode 1: set user as a leaver
							 mode 2: turn off leaver status
							 (probably because a mistake has been made)
							 mode 3: finish leaver status
							 Returns <1 failure, 1 success on delete
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_user_leaver_manage (integer, varchar, varchar, date, varchar) RETURNS integer
AS '
DECLARE
	
	mode               ALIAS for $1;
	in_userid		   ALIAS for $2;
	in_domain          ALIAS for $3;
	in_leavedate       ALIAS for $4;
	in_leavemsg        ALIAS for $5;

	usercheck          VARCHAR := '''';
	
	function_name	VARCHAR := ''fn_user_leaver_manage'';
	
BEGIN

-- Data verification

	IF in_userid IS NULL THEN
		RAISE EXCEPTION ''usr_leaver_manage_a : No userid provided'';
		RETURN 0;
	END IF;

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''usr_leaver_manage_b : No domain provided'';
		RETURN 0;
	END IF;

	IF mode = 1 THEN

		IF in_leavedate IS NULL THEN
			RAISE EXCEPTION ''usr_leaver_manage_c : No leavedate provided'';
			RETURN 0;
		END IF;

		IF in_leavemsg IS NULL THEN
			RAISE EXCEPTION ''usr_leaver_manage_d : No leave message provided'';
			RETURN 0;
		END IF;

	END IF;

	-- make a leaver record
	IF mode = 1 THEN

		SELECT INTO usercheck
			userid
		FROM
			users
		WHERE
			userid = lower(in_userid) 
			AND 
			domain = lower(in_domain)
			AND
			b_isadmin IS FALSE;

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_leaver_manage_e : user not found'';
			RETURN 0;
		END IF;

		UPDATE 
			users
		SET
			status = 3,
			leavedate = in_leavedate,
			leavemsg = in_leavemsg
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain)
			AND
			b_isadmin IS FALSE;

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_leaver_manage_f : setting leave status failed'';
			RETURN 0;
		END IF;
		
	-- unset leave status
	ELSIF mode = 2 THEN

		UPDATE 
			users
		SET
			status = 1
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain)
			AND
			b_isadmin IS FALSE;

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_leaver_manage_g : unsetting leave status failed'';
			RETURN 0;
		END IF;

	-- remove leave status
	ELSIF mode = 3 THEN

		UPDATE 
			users
		SET
			status = 9
		WHERE
			userid = lower(in_userid)
			AND
			domain = lower(in_domain)
			AND
			b_isadmin IS FALSE;

		IF NOT FOUND THEN
			RAISE EXCEPTION ''usr_leaver_manage_h : could not end leave status'';
			RETURN 0;
		END IF;
		
	ELSE

		RAISE EXCEPTION ''usr_leaver_manage_i : fall through error'';
		RETURN 0;

	END IF;

	RETURN 1;

END;'
    LANGUAGE plpgsql;

