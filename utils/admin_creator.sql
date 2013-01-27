INSERT INTO users   
	(userid, created, password, home, domain, uid, gid, status, typer, role,
	fullname, b_isadmin)

VALUES 
	('admin', now(), 'admin','/var/mail/admin', 'example.com',
	 1000, 1000, 1, 'Person', 'Administrator','Administrator', true);
