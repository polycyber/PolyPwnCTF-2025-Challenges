#!/bin/bash

# Initialize MySQL data directory if needed
if [ ! -d "/var/lib/mysql/mysql" ]; then
    mysqld --initialize-insecure --user=mysql
fi

# Start MySQL
service mysql start

# Wait for MySQL to be ready
until mysqladmin ping -h localhost --silent; do
    echo "Waiting for MySQL..."
    sleep 1
done

# Create database and setup permissions
mysql -e "CREATE DATABASE IF NOT EXISTS ctf;"
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';"
mysql -e "FLUSH PRIVILEGES;"

# Initialize database
mysql < /docker-entrypoint-initdb.d/sql-init.sql

# Fix socket permissions
chmod 777 /var/run/mysqld/mysqld.sock
chown -R mysql:mysql /var/run/mysqld/mysqld.sock

# Start Apache in foreground
apache2ctl -D FOREGROUND 