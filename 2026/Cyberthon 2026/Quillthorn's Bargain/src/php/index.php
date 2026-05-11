<?php
require_once 'config.php';
if (is_registered()) {
    header('Location: /shop.php');
    exit;
}
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['customer_name'] ?? '');
    if ($name === '') {
        $error = 'Please enter your name.';
    } elseif (mb_strlen($name) > 50) {
        $error = 'Name must be 50 characters or fewer.';
    } else {
        register(htmlspecialchars($name, ENT_QUOTES, 'UTF-8'));
        header('Location: /shop.php');
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quillthorn's Emporium</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body class="page-register">
    <div class="register-wrapper">
        <div class="register-card">
            <div class="register-icon">&
            <h1 class="register-title">Quillthorn's Emporium</h1>
            <p class="register-subtitle">Finest Wands in the Eastern Realms</p>
            <div class="promo-banner">
                <span class="promo-badge">&
                New customers receive <strong>100 Gold</strong> free credit!
            </div>
            <?php if ($error): ?>
                <div class="alert error"><?= htmlspecialchars($error) ?></div>
            <?php endif; ?>
            <form method="POST" action="/">
                <label class="register-label" for="customer_name">What shall we call you?</label>
                <input type="text" id="customer_name" name="customer_name" class="register-input" placeholder="Enter your name..." maxlength="50" required autofocus>
                <button type="submit" class="btn btn-register">Enter the Emporium</button>
            </form>
        </div>
    </div>
</body>
</html>
