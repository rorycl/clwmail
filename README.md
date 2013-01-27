# CLWMail

CLWMail is a simple database and web application for managing users and
groups for use for mail and related services. CLWMail also deals with
out-of-office and leaver messages and can be used to authenticate SOGo
groupware calendaring and contacts.

CLWMail was developed by Campbell-Lange Workshop Ltd. 

CLWMail has been in use since about 2006 and has been open sourced with
the support of Hopkins Architects.

## Documents

The `docs` folder has some material to help in understanding and setting
up CLWMail:

* README
  General README and instructions on how to setup the database and web
  application
* Screenshots : the login, users and groups pages (login.png, users.png,
  groups.png) of the Django webapp
* Integration notes for Dovecot (`dovecot_integration.txt`), Exim
  (`exim_integration.txt`) and SOGo (`sogo_integration.txt`).

## Improvements

CLWMail works for its current target services (Exim, Dovecot and SOGo)
but could be easily extended to other applications.

Email: it would be useful to more easily support callouts and external
aliases (i.e. for people not managed by the user database in CLWMail).
Aliases (or groups in CLWMail) are also not presently possible
between domains.

IMAP: it might be useful to drive shared mailboxes and similar features
through the groups facility in CLWMail.

Encrypted passwords should be incorporated. At present all services
should be run through TLS.

## Licence

This software is provided without any warranty under the GPLv3 licence.
