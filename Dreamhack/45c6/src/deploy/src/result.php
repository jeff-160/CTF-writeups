<?php
require('ticket.php');

$cookie_ticket = null;

if (isset($_COOKIE['ticket'])) {
    $cookie_ticket = $_COOKIE['ticket'];
    setcookie('ticket', '', time() - 1);
}

function validate($cookie_ticket) {
    if ($cookie_ticket == NULL) {
        echo "Get a ticket first!<br>";
        return;
    }

    if (!($d = base64_decode($cookie_ticket))) {
        echo "Not a valid ticket!<br>";
        return;
    }

    if (!($ticket = unserialize($d))) {
        echo "Not a valid ticket!<br>";
        return;
    }

    if (!($ticket instanceof Ticket)) {
        echo "Not a valid ticket!<br>";
        return;
    }

    if (!is_array($ticket->numbers)) {
        echo "No cheating!<br>";
        return;
    }


    $results = draw(45, 6);

    for ($i = 0; $i < 6; $i++) {
        $ticket->results[$i] = $results[$i];
    }

    $win = true;

    for ($i = 0; $i < 6; $i++) {
        if ($ticket->results[$i] !== $ticket->numbers[$i]) {
            $win = false;
        }
    }

    echo "Lucky numbers: " . implode(', ', $ticket->results) . "<br>";
    echo "Your numbers: " . implode(', ', $ticket->numbers) . "<br>";

    if ($win) {
        echo "You win! get the flag: ";
        $fp = fopen("/flag.txt", "r");
        echo fgets($fp) . "<br>";
        fclose($fp);
    } else {
        echo "Too bad.. maybe next time<br>";
    } 
}

?>

<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Lottery system</title>
</head>

<body>
    <h1>Lottery system</h1>
    <h2>Check result</h2>
    <?php validate($cookie_ticket); ?>
    <br>
    <a href="/index.php">Click here to return to main page</a>
</body>

</html>