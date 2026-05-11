<?php
require_once 'config.php';
require_login();

class ArtifactValidator
{
    private string $csrfToken;
    private string $filename;
    private string $userDir;

    public function __construct() {
        $this->csrfToken = $_POST['csrf_token'] ?? '';
        $this->filename = $_POST['filename'] ?? '';
        $this->userDir = __DIR__ . '/' . sanitizeUsername($_SESSION['username']);
    }

	private function findPos(string $file, string $split): int {
	    $lower = mb_strtolower($file, 'UTF-8');
	    $idx = strpos($lower, strtolower($split));

	    if ($idx === false) {
	        return -1;
	    }
	    return $idx + strlen($split);
	}
    
    public function handleRequest(): void {
        header('Content-Type: application/json');

        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            $this->respond(false, 'Invalid method.');
            return;
        }

        if (!$this->verifyCsrfToken()) {
            $this->respond(false, 'Invalid protective ward (CSRF).');
            return;
        }

        if (empty($this->filename)) {
            $this->respond(false, 'No artifact provided for validation.');
            return;
        }

        $this->validate($this->filename);
    }

    private function verifyCsrfToken(): bool {
        return verify_csrf_token($this->csrfToken);
    }

    private function validate(string $file): void {
    	global $sigil;
        $safeFilename = sanitizeFilename($file);
        $file = $this->userDir . '/' . $safeFilename;
        
        if (!file_exists($file)) {
            $this->respond(false,'Artifact does not exsit in Repository.');
        	return;
        }

        $data = file_get_contents($file);
        
        if (!str_contains($data, $sigil) || !$this->spell_checkv2($safeFilename)) {
        	$this->respond(false,'Something is missing in this artifact.');
       		return;
   		}

        $this->respond(true, file_get_contents(WELCOME_FILE));

        return;
    }

	private function spell_checkv2(string $filename): bool {
	    global $URI;
	    if (is_null($filename) || $filename === '') {
	        return false;
	    }

	    $pos = $this->findPos($filename, ".spell");
	    if ($pos === -1) {
	        return false;
	    }

	    $ext = substr($filename, $pos);
	    $ext = mb_strtolower($ext, 'UTF-8');

	    $URI = substr($filename, 0, $pos);

	    return $ext == null;
	}


    private function respond(bool $status, string $message): void {
        echo json_encode([
            'status' => $status,
            $status ? 'message' : 'error' => $message
        ]);
        exit;
    }
}

$validator = new ArtifactValidator();
$validator->handleRequest();
