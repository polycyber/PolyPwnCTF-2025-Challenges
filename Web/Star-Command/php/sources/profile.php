<?php
require 'vendor/autoload.php'; // Include Firebase JWT library

use Firebase\JWT\JWT;

$keyPrivate = file_get_contents('/private.key');


include("cookie_decode.php");



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


if (ISSET($_COOKIE['PHP_SESSION'])){
	$username = decode_jwt($_COOKIE['PHP_SESSION']);
	$stmt = $pdo->prepare('SELECT * FROM users WHERE username = :username and is_admin=1');
    $stmt->bindValue( ':username',$username,getPdoParamType($username));
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

	if ($user){
		$role = "Administrator";
		$photoPath = $user['profile_picture'];
		$displayName = $user['username'] . ' Lightyear';
	} else if (!is_null($username)){
		$role = "Space Ranger";
		$photoPath = "assets/space_ranger.png";
		$displayName = $username . ' Lightyear';
	} else {
		unset($_COOKIE['PHP_SESSION']);
		header('Location: login.php');
		die();
	}
	
} else {
	unset($_COOKIE['PHP_SESSION']);
	header('Location: login.php');
	die();
}


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	
	$img_size = getimagesize($_POST['img_url']);
	if ($img_size !== false) {
		if ($img_size[0]!=300 or $img_size[1]!=300){
			echo "<script>alert('Sorry, your profile picture must be 300x300 px')</script>";	
		} else {
			echo "<script>alert('The function is not implemented yet!')</script>";
		}
	} else {
		echo "<script>alert('Error, this is not an image')</script>";
	}
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Command - Profile</title>
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
        <h1>Your profile</h1>

		<h2>Work in progress...</h2>
		<p>Star command has suffered big damage since its last fight against Zurg... Currently most of the options are unavailable</p>
		
		<h1>Your Space ranger ID card</h1>

		<div class="center-content">
    <!-- Space Ranger ID Card -->
		<div class="space-ranger-card">
			<div class="ranger-photo">

				<img src="<?php echo $photoPath; ?>" alt="Space Ranger Photo">
			</div>
			<div class="ranger-info">
				<h2 class="ranger-name"><?php echo $displayName; ?></h2>
				<p class="ranger-role"><?php echo $role; ?></p>
				<?php
				if ($user){
					echo '<p class="ranger-role">';
					$stmt = $pdo->prepare('SELECT flag FROM flag');
					$stmt->execute();
					$flag = $stmt->fetch(PDO::FETCH_ASSOC);
					echo $flag['flag'];
					echo '</p>';
				}
				?>
			</div>
		</div>

		<!-- Form Section -->

		<h2 class="form-title">Change your ID picture</h2>
		<form method="POST" class="form-container">
			<label>
				Picture's URL: 
				<input type="url" name="img_url" placeholder="https://example.com/image.jpg" required>
			</label>
			<br>
			<button type="submit" class="update-button">Update</button>
		</form>

	</div>
	</div>
	</body>
	</html>