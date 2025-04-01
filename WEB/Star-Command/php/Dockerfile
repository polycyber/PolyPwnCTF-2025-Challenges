# Utiliser une image officielle de PHP avec Apache
FROM php:8.2-apache

RUN apt update
RUN apt install -y git
# Activer les extensions nécessaires pour SQLite
RUN docker-php-ext-install mysqli pdo_mysql opcache
RUN a2enmod rewrite headers


ENV COMPOSER_ALLOW_SUPERUSER 1
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer


WORKDIR /var/www/html

# Copier les fichiers de l'application dans le dossier par défaut d'Apache
COPY ./sources /var/www/html/

RUN composer install

# Assurer les bons droits sur le répertoire
#RUN php /var/www/html/init_db.php && rm /var/www/html/init_db.php
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html
RUN chmod 644 /var/www/html/public.key
RUN mv /var/www/html/private.key / && chmod 600 /private.key

# Exposer le port par défaut d'Apache
EXPOSE 80

# Lancer Apache en tant que processus principal
CMD ["apache2-foreground"]

