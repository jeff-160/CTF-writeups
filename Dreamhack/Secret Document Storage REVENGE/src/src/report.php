<?php
require("db.php");
if ($_SERVER['REQUEST_METHOD'] == 'POST' and $_POST['title'] and $_POST['content']) {
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        if (isset($_FILES['file']) && $_FILES['file']['error'] == 0) {
            $allowedTypes = ['image/png' => 'png', 'image/jpeg' => 'jpg'];
            $fileType = $_FILES['file']['type'];

            if (array_key_exists($fileType, $allowedTypes)) {
                $uploadPath = './uploads/';
                $randomFileName = uniqid() . '.' . $allowedTypes[$fileType];

                if (!is_dir($uploadPath)) {
                    mkdir($uploadPath, 0777, true);
                }

                if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadPath . $randomFileName)) {
                    try {
                        $title = addslashes($_POST['title']);
                        $content = $_POST['content'];
                        $stmt = $conn->prepare("INSERT INTO document (title, content,filename) VALUES (?, ?, ?)");
                        $stmt->bind_param('sss', $title, $content, $randomFileName);

                        $stmt->execute();
                    } catch (mysqli_sql_exception $e) {
                        echo "Query failed: " . $e->getMessage();
                    }
                    echo "<script>alert('$randomFileName')</script>";
                    echo "<script>alert('The file has been uploaded successfully.');</script>";
                    echo "<script>location.href='/index.php'</script>";
                } else {
                    echo "<script>alert('Error. Please Contact admin.');</script>";
                    echo "<script>location.href='/index.php'</script>";
                }
            }
            else {
                echo "<script>alert('Only PNG and JPG files are allowed.');</script>";
                echo "<script>location.href='/index.php'</script>";
            }
        }
        else {
            echo "<script>alert('Please upload an image as well. Only png and jpg are allowed.');</script>";
            echo "<script>location.href='/index.php'</script>";
        }
    }

} else if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    include "./templates/report.html";
} else {
    echo "BLOCKED";
}
?>

