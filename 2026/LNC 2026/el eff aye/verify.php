<?php
session_start();

$result = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $code = $_POST['code'] ?? '';

    /*
     * Expected format:
     *  - 3 uppercase letters
     *  - a dash
     *  - 4 digits
     * Example: ABC-1234
     */
    if (preg_match('/^[A-Z]{4}(_\d{4}){3}$/', $code)) {
      $flag = getenv('FLAG');
      $result = ['success', "Valid verification code. Here is the flag: $flag"];
    } else {
      $result = ['error', 'Invalid verification code. Please submit a valid code.'];
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verification</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            background: #020617;
            padding: 32px;
            border-radius: 10px;
            width: 100%;
            max-width: 400px;
        }

        h2 {
            margin-top: 0;
            text-align: center;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-top: 12px;
            background: #020617;
            color: #e5e7eb;
            border: 1px solid #334155;
            border-radius: 6px;
        }

        button {
            width: 100%;
            padding: 10px;
            margin-top: 16px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }

        button:hover {
            background: #1d4ed8;
        }

        .message {
            margin-top: 16px;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
        }

        .success {
            background: #064e3b;
            color: #a7f3d0;
        }

        .error {
            background: #7f1d1d;
            color: #fecaca;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>Verification</h2>
    <p>Please enter your verification code.</p>

    <form method="post">
        <input
            type="text"
            name="code"
            placeholder="Enter your verification code here."
            required
        >
        <button type="submit">Verify</button>
    </form>

    <?php if ($result): ?>
        <div class="message <?= $result[0] ?>">
            <?= htmlspecialchars($result[1]) ?>
        </div>
    <?php endif; ?>
</div>

</body>
</html>

