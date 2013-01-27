alter table users ADD column b_isadmin boolean default False; 
alter table users add column default_message text ;

\i type_loader.sql
\i function_loader.sql
 


