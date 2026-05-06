import pymysql
pymysql.install_as_MySQLdb()

import django.db.backends.mysql.base as mysql_base
mysql_base.DatabaseWrapper.check_database_version_supported = lambda self: None