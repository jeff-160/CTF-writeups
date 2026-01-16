<?php
require('ticket.php');

$ticket_exist = false;

if (isset($_COOKIE['ticket'])) {
    $ticket_exist = true;
} else {
    $ticket = new Ticket();
    $ticket->issue();
    setcookie('ticket', base64_encode(serialize($ticket)));
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
    <h2>Draw ticket</h2>
    <?php
    if ($ticket_exist)
        echo "You already have a ticket!<br>";
    else
        echo "Issued a ticket!<br>Check your numbers: " . implode(', ', $ticket->numbers) . "<br>";
    ?>
    <br>
    <a href="/index.php">Click here to return to main page</a>
</body>

</html>