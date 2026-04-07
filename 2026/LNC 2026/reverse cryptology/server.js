const express  = require('express');
const multer   = require('multer');
const path     = require('path');
const fs       = require('fs');
const { execFileSync } = require('child_process');

const app  = express();
const PORT = 3000;

// ── Static frontend
app.use(express.static(path.join(__dirname, 'public')));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage });

// ── POST /encode — run uploaded script with password as stdin, return stdout
app.post('/encode', upload.single('encoder'), (req, res) => {
  const password = req.body.password || '';

  if (!req.file) {
    return res.json({ error: 'No file uploaded.' });
  }

  const scriptPath = path.join(__dirname, 'uploads', req.file.originalname);
  const ext        = path.extname(req.file.originalname).toLowerCase();

  const runtimeMap = {
    '.py': 'python3',
    '.js': 'node',
    '.sh': 'bash',
    '.rb': 'ruby',
    '.pl': 'perl',
  };

  const runtime = runtimeMap[ext];
  if (!runtime) {
    return res.json({ error: `Unsupported file type: ${ext}` });
  }

  try {
    const output = execFileSync(runtime, [scriptPath], {
      input: password,
      timeout: 5000,
      maxBuffer: 1024 * 64,
      env: { PATH: process.env.PATH }
    });

    return res.json({ output: output.toString() });

  } catch (err) {
    const stderr = err.stderr ? err.stderr.toString() : err.message;
    return res.json({ error: stderr });
  }
});

app.listen(PORT, () => {
  console.log(`Reverse Cryptology running on port ${PORT}`);
});
