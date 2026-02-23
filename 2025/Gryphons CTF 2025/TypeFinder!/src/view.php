<?php
// view.php - debug file viewer (intentionally allows path traversal)
$f = $_GET['f'] ?? '';

if ($f === '') {
    echo "<h1>Debug File Viewer</h1>";
    echo "<p>Internal tool to view server files.";
    echo "<p>Hint: JSON files contain important data. I do have a folder named 'private' but surely no one gets in there and finds any user data :P</p>";
    exit;
}

// Basic security checks
if (strpos($f, "\0") !== false) {
    die("Invalid filename");
}

// Whitelist of viewable files (still vulnerable to path traversal!)
$allowed_files = [
    'users.json',     // Allow reading users.json through path traversal
    'index.php',      // Allow viewing source of public files
    'login.php',
    'forgor.php',
    'view.php'
];

// Get the base filename without path
$basename = basename($f);
if (!in_array($basename, $allowed_files)) {
    die("Access denied. Only certain files can be viewed.");
}

// Vulnerable path building (intentional)
if (str_starts_with($f, '/')) {
    $path = $f;  // Allow absolute paths
} else {
    $path = __DIR__ . '/' . $f;  // Relative paths from current directory
}

if (!file_exists($path)) {
    http_response_code(404);
    echo "File not found: " . htmlspecialchars($path);
    exit;
}

// Set content type based on extension
$ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));
if ($ext === 'json') {
    header('Content-Type: application/json');
    echo file_get_contents($path);
} else {
    echo "<h2>Contents of: " . htmlspecialchars($path) . "</h2>";
    echo "<pre>" . htmlspecialchars(file_get_contents($path)) . "</pre>";
}