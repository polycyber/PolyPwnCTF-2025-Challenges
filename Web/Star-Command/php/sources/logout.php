<?php

unset($_COOKIE['PHP_SESSION']);
setcookie("PHP_SESSION","",-1,"/");
header('Location: index.php');

/* OMG You found this hidden comment ! What a boss !
You lost the game BTW */

?>