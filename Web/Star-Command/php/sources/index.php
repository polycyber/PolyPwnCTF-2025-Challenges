<?php

include("cookie_decode.php");

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Command - Home</title>
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
        <h1>Welcome to Star Command</h1>
        <p>Explore the universe, defend the galaxy, and go beyond infinity!</p>
        <img src="assets/Star_Command_symbol.png"/>
    </div>

    
</body>
</html>