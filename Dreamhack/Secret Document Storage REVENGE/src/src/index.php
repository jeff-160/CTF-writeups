<?php
require("db.php");
session_start();
if($conn) {
    include "./templates/index.html";
    $stmt = $conn->prepare("SELECT * FROM document;");
    $stmt->execute();

    $result = $stmt->get_result();

    $results = [];
    while ($row = $result->fetch_assoc()) {
        $results[] = $row;
    }
    $count = 1;
    echo '<div class="gallery-container">';
    foreach ($results as $row) {
        echo '<div class="gallery-item item' . $count . '">';
        echo '<div class="image-blur"></div>';
        echo '<a href="view.php?title=' . $row['title'] . '" class="gallery-text">' . $row['title'] . '</a>';
        echo '</div>';
        $count += 1;
    }
    echo '</div>
          </body>
          </html>';

    echo '<style>';
    $count = 1;
    foreach ($results as $row) {
        echo ".item" . $count . " .image-blur { background-image: url('./uploads/" . $row['filename'] . "'); }";
        $count += 1;
    }
    $stmt->close();

}
else {
    echo "Failed";
}

?>
