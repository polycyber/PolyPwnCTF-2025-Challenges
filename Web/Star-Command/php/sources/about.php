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

    <div class="content">
        <h1>About Star Command</h1>
        <p>Star Command is the intergalactic organization dedicated to protecting the galaxy from evil forces and ensuring peace among the stars. With advanced technology, fearless Space Rangers, and a mission to go beyond infinity, Star Command represents the pinnacle of bravery and innovation.</p>
        <h2>Our Mission</h2>
        <p>To explore strange new worlds, to seek out new life and civilizations, and to boldly go where no Space Ranger has gone before. At Star Command, we believe in the values of courage, teamwork, and resilience in the face of challenges.</p>
        <h3>Join Us</h3>
        <p>Are you ready to take up the mantle of a Space Ranger and make a difference in the galaxy? Star Command is always looking for the brightest and bravest to join our ranks. Together, we can protect the universe and inspire generations to dream big!</p>
    
        <br/>
        <br/>
        <img src="assets/team_lightyear.webp"/>
    </div>

    
</body>
</html>
