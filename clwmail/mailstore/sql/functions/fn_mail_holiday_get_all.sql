CREATE OR REPLACE FUNCTION fn_mail_holiday_get_all(integer, character varying, character
varying) RETURNS user_holidays
    AS $_$
DECLARE

    in_id       ALIAS for $1;
    in_userid       ALIAS for $2;
    in_domain       ALIAS for $3;

    resulter        user_holidays%rowtype;

BEGIN

    SELECT INTO resulter
        id           as holid,
        holidaystart as holstart,
        holidayend   as holend,
        message      as holmsg,
           extract(hour from holidaystart)      as holstart_hour,
           extract(minute from holidaystart)    as holstart_min,
           extract(day from holidaystart)       as holstart_day,
           extract(month from holidaystart)     as holstart_mon,
           extract(year from holidaystart)      as holstart_yr,
           extract(hour from holidayend)        as holend_hour,
           extract(minute from holidayend)      as holend_min,
           extract(day from holidayend)         as holend_day,
           extract(month from holidayend)       as holend_mon,
           extract(year from holidayend)        as holend_yr
    FROM
       holidays
    WHERE
        id = in_id
        AND
        userid = lower(in_userid)
        AND
        domain = lower(in_domain) ;


    RETURN resulter;

END;$_$
    LANGUAGE plpgsql;
