CREATE DATABASE IF NOT EXISTS starcommand;

DROP TABLE IF EXISTS starcommand.users;

CREATE USER IF NOT EXISTS 'definitelynotzurg'@'%' IDENTIFIED BY 'BuzzLighyearToStarCommand!DoYouReceiveMe?' ;

FLUSH PRIVILEGES;



CREATE TABLE IF NOT EXISTS starcommand.users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            profile_picture VARCHAR(255) DEFAULT NULL,
            is_admin TINYINT DEFAULT 0
);


GRANT SELECT ON starcommand.* TO 'definitelynotzurg'@'%';
FLUSH PRIVILEGES;
GRANT SELECT, INSERT, UPDATE ON starcommand.users TO 'definitelynotzurg'@'%';
FLUSH PRIVILEGES;

INSERT INTO starcommand.users (username, password, profile_picture, is_admin)
VALUES ('TrulyNotZurgIPromiseThatIAmAnAdmin','OMGThisPasswordCannotBeGuessed!','assets/space_admin.png',1);


DROP TABLE IF EXISTS starcommand.flag;

CREATE TABLE IF NOT EXISTS starcommand.flag (
    flag VARCHAR(255)
);

INSERT INTO starcommand.flag (flag)
VALUES ("polycyber{BuzzLightyear_to_Star_Command!I_found_a_type_juggling!}");

