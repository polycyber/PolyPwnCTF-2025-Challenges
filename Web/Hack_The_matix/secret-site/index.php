<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$conn = new mysqli("localhost", "root", "", "ctf");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    // Vulnerable SQL query - but requires proper injection to work
    $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    
    $result = $conn->query($query);
    
    if (!$result) {
        echo "Error: " . $conn->error;
    }
    else if ($result->num_rows > 0) {
        $flag_query = "SELECT flag FROM flags LIMIT 1";
        $flag_result = $conn->query($flag_query);
        $flag = $flag_result->fetch_assoc()['flag'];
    } else {
        echo "<p>Invalid credentials!</p>";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>System Access</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)),
                            url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAG0lEQVQYV2NkYGD4z8DAwMgABXAGNgGwSgwVAFbmAgXQdISfAAAAAElFTkSuQmCC');
        }

        .login-container {
            background-color: rgba(0, 20, 0, 0.95);
            padding: 30px;
            border: 1px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            max-width: 400px;
            width: 90%;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        input {
            background-color: #000;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 10px;
            font-family: 'Courier New', monospace;
        }

        input:focus {
            outline: none;
            box-shadow: 0 0 5px #00ff00;
        }

        input[type="submit"] {
            background-color: #003300;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #004400;
        }

        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .error-message {
            color: #ff0000;
            text-align: center;
            margin-top: 10px;
        }

        .success-message {
            color: #00ff00;
            text-align: center;
            margin-top: 10px;
            padding: 10px;
            border: 1px dashed #00ff00;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>System Access</h1>
        <form method="POST" action="">
            <input type="text" name="username" placeholder="Enter your username" required>
            <input type="password" name="password" placeholder="Enter your password" required>
            <input type="submit" value="JACK IN">
        </form>
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            if (!$result) {
                echo '<div class="error-message">Error: ' . $conn->error . '</div>';
            }
            else if ($result->num_rows > 0) {
                echo '<div class="success-message">Congratulations! Here\'s your flag: ' . $flag . '</div>';
            } else {
                echo '<div class="error-message">Invalid credentials!</div>';
            }
        }
        ?>
    </div>

    <script>
        // Matrix rain effect
        const canvas = document.createElement('canvas');
        canvas.classList.add('matrix-rain');
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const chars = "01";
        const fontSize = 14;
        const columns = canvas.width/fontSize;
        const drops = [];

        for(let x = 0; x < columns; x++)
            drops[x] = 1;

        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#00ff00";
            ctx.font = fontSize + "px monospace";

            for(let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975)
                    drops[i] = 0;
                
                drops[i]++;
            }
        }

        setInterval(draw, 33);
    </script>
</body>
</html> 