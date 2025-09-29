<?php
require 'vendor/autoload.php'; // Charger Firebase JWT

use Firebase\JWT\JWT;
use Firebase\JWT\Key;


$keyPrivate = file_get_contents('/private.key');
$keyPublic = file_get_contents('public.key');

function decode_jwt(){
	$keyPrivate = file_get_contents('/private.key');
	$keyPublic = file_get_contents('public.key');

	try {
		$decoded = JWT::decode($_COOKIE['PHP_SESSION'], new Key($keyPublic, 'RS256'));

		return $decoded->username;
	} catch (Exception $e) {
		return null;
	}
}

function getPdoParamType($value) {
    return match (gettype($value)) {
        'integer' => PDO::PARAM_INT,
        'boolean' => PDO::PARAM_BOOL,
        'NULL'    => PDO::PARAM_NULL,
        default   => PDO::PARAM_STR
    };
}

