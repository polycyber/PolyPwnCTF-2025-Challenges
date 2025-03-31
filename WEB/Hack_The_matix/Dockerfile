FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    mysql-server \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get remove --purge -y --allow-remove-essential apt && rm -rf /var/lib/apt/lists/*

# Copy website files
COPY ./main-site/ /var/www/html/
COPY ./secret-site/ /var/www/secret/

# Copy Apache configuration files
COPY ./apache-config/000-default.conf /etc/apache2/sites-available/
COPY ./apache-config/secret.conf /etc/apache2/sites-available/

# Copy SQL initialization script
COPY ./sql-init.sql /docker-entrypoint-initdb.d/

# Enable Apache modules and sites
RUN a2enmod vhost_alias && \
    a2ensite 000-default.conf && \
    a2ensite secret.conf

# Fix MySQL permissions and directories
RUN mkdir -p /var/run/mysqld && \
    mkdir -p /var/lib/mysql && \
    chown -R mysql:mysql /var/lib/mysql && \
    chown -R mysql:mysql /var/run/mysqld && \
    chmod 777 /var/run/mysqld

# Fix www-data user home
RUN usermod -d /var/www www-data

# Set proper permissions for web files
RUN chown -R www-data:www-data /var/www/

EXPOSE 80

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"] 