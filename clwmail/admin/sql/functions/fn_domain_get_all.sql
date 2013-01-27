/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_everyone.sql
	Function description:  . get everyone who is active
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/


CREATE OR REPLACE FUNCTION 
	fn_domain_get_all (varchar) RETURNS domain_type 
AS '
DECLARE
	in_domain       ALIAS for $1;
	resulter        domain_type%rowtype;
BEGIN

    SELECT INTO 
		resulter
		* 
	FROM
		domains	
	WHERE
		domain = lower(in_domain);

	RETURN  resulter;


END;'
    LANGUAGE plpgsql;

