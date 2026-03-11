const express = require('express');
const app = express();
const port = 3333;

app.get('/h', (req, res) => {
	res.json(req.headers);
});

app.get('/f', (req, res) => {
	res.send(process.env.FLAG);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

