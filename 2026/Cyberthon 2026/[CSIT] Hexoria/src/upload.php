<?php
require_once 'config.php';
require_login();

header('Content-Type: application/json');

class ArtifactUploader
{
    private string $username;
    private array $file;
    private string $userDir;

    public function __construct(array $file)
    {
        $this->username = $_SESSION['username'] ?? 'guest';
        $this->file = $file;
        $this->userDir = __DIR__ . '/' . sanitizeUsername($this->username);
    }

    public function handleUpload(): void
    {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            $this->fail('Invalid method.');
        }

        if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
            $this->fail('Invalid protective ward (CSRF).');
        }

        if (!$this->validateFile()) {
            return; 
        }

        $this->ensureUserDir();
        $safeFilename = sanitizeFilename($this->file['name']);
        $destination = $this->userDir . '/' . $safeFilename;

        if (file_exists($destination)) {
            $this->fail('An artifact with that name already exists in your realm.');
        }

        try{
            $imgck = new Imagick($this->file['tmp_name']);
            $imgck->thumbnailImage(55, 55, true, true);
            $imgck->writeImage($destination);
            $imgck->clear();
            $imgck->destroy();

            echo json_encode(['success' => true, 'filename' => $safeFilename]);
        
        } catch (Exception $e) {
            $this->fail('Failed to anchor the artifact.');
        }
        
    }

    private function validateFile(): bool
    {
        if (!isset($this->file) || $this->file['error'] !== UPLOAD_ERR_OK) {
            $this->fail('Image corruption during summon.');
            return false;
        }

        if ($this->file['size'] > 2 * 1024 * 1024) {
            $this->fail('The artifact is too heavy for the magic.');
            return false;
        }

        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $mime = $finfo->file($this->file['tmp_name']);
        if ($mime !== 'image/png') {
            $this->fail('Only authentic PNG artifacts are accepted.');
            return false;
        }

        $ext = strtolower(pathinfo($this->file['name'], PATHINFO_EXTENSION));
        if ($ext !== 'png') {
            $this->fail('The artifact essence must end in .png');
            return false;
        }

        return true;
    }

    private function ensureUserDir(): void
    {
        if (!is_dir($this->userDir)) {
            if (!mkdir($this->userDir, 0755, true)) {
                $this->fail('Failed to create personal realm.');
            }
            file_put_contents(
                $this->userDir . '/.htaccess',
                "php_flag engine off\nRemoveHandler .php .phtml .php3\nAddType text/plain .php"
            );
        }
    }


    private function fail(string $message): void
    {
        echo json_encode(['success' => false, 'error' => $message]);
        exit;
    }
}

$uploader = new ArtifactUploader($_FILES['magic_image'] ?? []);
$uploader->handleUpload();