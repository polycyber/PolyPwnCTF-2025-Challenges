<?php
// MySQL connection settings
$dbHost = 'mysql'; // Docker Compose MySQL service name
$dbName = 'starcommand';
$dbUser = 'definitelynotzurg';
$dbPassword = 'BuzzLighyearToStarCommand!DoYouReceiveMe?';

try {
    $pdo = new PDO("mysql:host=$dbHost;dbname=$dbName", $dbUser, $dbPassword);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection error: " . $e->getMessage());
}

include("cookie_decode.php");

// Handle registration
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? null;
    $password = $_POST['password'] ?? null;

    if (!$username || !$password) {
        echo "Please provide both username and password.";
        exit;
    }

    // Check if user already exists
    $stmt = $pdo->prepare('SELECT COUNT(*) FROM users WHERE username = :username');
    $stmt->bindValue(':username',$username,getPdoParamType($username));
    $stmt->execute();
    if ($stmt->fetchColumn() > 0) {
        echo "This username is already taken.";
        exit;
    }

    // Insert user (hash the password)
    $hashedPassword = password_hash($password, PASSWORD_BCRYPT);
    $stmt = $pdo->prepare('INSERT INTO users (username, password) VALUES (:username, :password)');
    $stmt->bindValue(':username',$username,getPdoParamType($username));
    $stmt->bindValue(':password',$hashedPassword,getPdoParamType($hashedPassword));
    $stmt->execute();


    // Redirect to login page
    header("Location: login.php");
    exit;
}

// HTML form
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Command - Register</title>
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
            } else {
                echo '<li><a href="/login.php">Log In</a></li>';
            }
            ?>
        </ul>
    </div>

    <!-- Main Content -->
    <div class="content">
        <h1>Join Star Command !</h1>

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
                    <button type="submit">Create Account</button>
                    <!-- Right Round Button -->
                    <div class="round-button"></div>
                </div>
            </form>

            
                
        </div>
    <p><a href="login.php">Back to login</a></p>
    
    </div>
</body>
</html>

