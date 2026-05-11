<?php
require_once 'config.php';
require_login();
header('Content-Type: application/json');

$lines = file($file_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

if (empty($lines)) {
    echo json_encode(['message' => 'No magical waves received.']);
    exit;
}

$id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);

if($id === null){
	echo json_encode(['message' => '........']);
	exit;
}

$message = $lines[$id];
echo json_encode(['message' => $message]);

