create or replace view sogo_auth as (
    select 
        userid || '@' || domain as c_uid
        ,userid || '@' || domain as c_name
        ,password as c_password
        ,fullname as  c_cn
        ,userid || '@' || domain as mail 
    from 
        users 
    where 
        status in (1 ,2)
);
