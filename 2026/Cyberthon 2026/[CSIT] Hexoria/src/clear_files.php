<?php
require_once 'config.php';
require_login();

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'Invalid method.']);
    exit;
}

if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
    echo json_encode(['success' => false, 'error' => 'Invalid protective ward (CSRF).']);
    exit;
}

$username = $_SESSION['username'];
$safe_username = basename(preg_replace('/[^a-zA-Z0-9_-]/', '', $username));
$user_dir = __DIR__ . '/' . $safe_username;

$deleted = 0;

if (is_dir($user_dir)) {
    $files = scandir($user_dir);
    foreach ($files as $file) {
        if ($file === '.' || $file === '..' || $file === '.htaccess') {
            continue;
        }
        $filepath = $user_dir . '/' . $file;
        if (is_file($filepath)) {
            unlink($filepath);
            $deleted++;
        }
    }
}

echo json_encode(['success' => true, 'deleted' => $deleted]);
