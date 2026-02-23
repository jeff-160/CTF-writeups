<?php
require '../indexController.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Welcome, <?php echo $username_display; ?></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout.php">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <?php if ($is_admin): ?>
            <div class="alert alert-success" role="alert">
                <h4 class="alert-heading text-center">Welcome, Admin!</h4>
                <p class="text-center">Congratulations! You have successfully accessed the admin dashboard.</p>
                <hr>
                <p class="mb-0 text-center">Your flag is: <code><?php echo $flag; ?></code></p>
            </div>
        <?php else: ?>
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading text-center">Access Denied</h4>
                <p class="text-center">You do not have the necessary permissions to view this page. The user '<strong><?php echo $username_display; ?></strong>' is not an administrator.</p>
                <hr>
                <div class="d-flex justify-content-center align-items-center gap-3">
                    <p class="mb-0">FLAG: <?php echo substr($flag, 0, 6);?></p>
                    <img src="/cat.png" alt="Access Denied" class="img-fluid" style="max-width: 150px;">
                </div>
                <p class="text-center">Oh no! flag was eaten by admin's cat!</p>
            </div>
        <?php endif; ?>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
