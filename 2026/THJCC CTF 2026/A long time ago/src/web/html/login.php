<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $_SESSION['perms'] = [];

    if ($_POST['username'] === 'admin') {
        die("Admin login is permanently disabled.");
    }

    $perm_key = $_POST['username'];
    $_SESSION['perms'][$perm_key] = 'guest_access';

    $_SESSION['username'] = $_POST['username'];
    header('location: /index.php');
    die();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container">
        <div class="row justify-content-center align-items-center vh-100">
            <div class="col-md-6 col-lg-4">
                <div class="card shadow">
                    <div class="card-body">
                        <h1 class="card-title text-center mb-4">Login</h1>
                        <p class="text-center text-muted">Admin login is disabled. Only guests are allowed to sign in.</p>
                        <form action="/login.php" method="post">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username:</label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">Login as Guest</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>