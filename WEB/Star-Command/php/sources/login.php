<?php
require 'vendor/autoload.php'; // Include Firebase JWT library

use Firebase\JWT\JWT;

$keyPrivate = file_get_contents('/private.key');


include("cookie_decode.php");


if (ISSET($_COOKIE['PHP_SESSION']) && !is_null(decode_jwt($_COOKIE['PHP_SESSION']))){
    header('Location: profile.php');
    die();
}

// MySQL connection settings
$dbHost = 'mysql'; // Docker Compose MySQL service name
$dbName = 'starcommand';
$dbUser = 'definitelynotzurg';
$dbPassword = 'BuzzLighyearToStarCommand!DoYouReceiveMe?';

try {
    $pdo = new PDO("mysql:host=$dbHost;dbname=$dbName", $dbUser, $dbPassword,[PDO::ATTR_EMULATE_PREPARES => false,PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,]);
} catch (PDOException $e) {
    die("Database connection error: " . $e->getMessage());
}

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? null;
    $password = $_POST['password'] ?? null;

    if (!$username || !$password) {
        echo "Please provide both username and password.";
        exit;
    }

    // Check user credentials
    $stmt = $pdo->prepare('SELECT password FROM users WHERE username = :username');
    $stmt->bindValue( ':username',$username,getPdoParamType($username));
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$user || !password_verify($password, $user['password'])) {
        echo "Invalid username or password.";
        exit;
    }

    // Generate JWT
    $payload = [
        'username' => $username,
        'exp' => time() + 360000 // JWT expires in 100 hour
    ];
    $jwt = JWT::encode($payload, $keyPrivate, 'RS256');

    // Set JWT in a cookie
    setcookie('PHP_SESSION', $jwt, [
        'expires' => time() + 3600,
        'httponly' => false,
        'secure' => false, // Use HTTPS in production
        'samesite' => 'Lax'
    ]);

    header('Location: profile.php');
    die();
}

// HTML form
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Command - Log In</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Menu Section -->
    <div class="menu-container">
        <img src="assets/star_command.png" alt="Star Command Ship" class="star-command">
        <ul class="menu">
            <li><a href="/">Home</a></li>
            <li><a href="/about.php">Our mission</a></li>
            <?php
            if (ISSET($_COOKIE['PHP_SESSION']) && !is_null(decode_jwt($_COOKIE['PHP_SESSION']))){
                echo '<li><a href="/profile.php">Your profile</a></li>';
                echo '<li><a href="/logout.php">Log out</a></li>';
            } else {
                echo '<li><a href="/login.php">Log In</a></li>';
            }
            ?>
        </ul>
    </div>

    <!-- Main Content -->
    <div class="content">
        <h1>Log in</h1>
        <div class="form-container">
            <form method="POST">
                <label>Username:</label>
                <input type="text" name="username" required><br>
                <label>Password:</label>
                <input type="password" name="password" required><br>
                <div class="form-bottom">
                    <!-- Left Oblique Buttons -->
                    <div class="left-buttons">
                        <div class="oblique-button blue"></div>
                        <div class="oblique-button green"></div>
                        <div class="oblique-button red"></div>
                    </div>
                    <button type="submit">Login</button>
                    <!-- Right Round Button -->
                    <div class="round-button"></div>
                </div>
            </form>
        </div>
    <p><a href="register.php">Create an account</a></p>
    </div>
</body>
</html>

