const express = require('express');
const app = express();
const redis = require('redis');
const { Curl } = require('node-libcurl');

const FLAG = process.env.FLAG || 'DH{sample_flag}';
const PIE = 314159265;
const KEY_PREFIX = 'itz_super@key!!>';

const PORT = 5000;
const client = redis.createClient({
	url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`
});

client.connect();
app.use(express.static('./public'));
app.use(express.urlencoded({ extended: true }));

function filterUrl(url) {
	const parsedUrl = new URL(url);

	if (parsedUrl.protocol === 'file:') {
		return false;
	}

	if (/[\s%_@!><~*]/.test(url)) {
		return false;
	}

	return true;
}

app.post('/handshake', async (req, res) => {
	const url = req.body.url || 'https://www.google.com';

	try {
		if (!filterUrl(url)) {
			return res.status(400).send('Forbidden');
		}

		const response = await new Promise((resolve, reject) => {
			const curl = new Curl();

			curl.setOpt('URL', url);

			curl.on('end', function (statusCode, data) {
				resolve(data);
				this.close();
			});

			curl.on('error', function (err) {
				reject(err);
				this.close();
			});

			curl.perform();
		});

		return res.status(200).send(response);
	} catch (error) {
		return res.status(400).send('Something Wrong');
	}
});

app.get('/flag', async (req, res) => {
	const key = req.query.key;
	const secret = Math.floor(Math.random() * PIE);
	console.log(secret);
	let score = 0;
	try {
		if (key === `${KEY_PREFIX}${secret.toString()}`) {
			score = await client.get(key);
			console.log(score);
		}
	} catch (error) {
		return res.status(400).send('Something Wrong');
	}

	if (score === '99') {
		res.send(FLAG);
	} else {
		res.send(`Failed... key is ${KEY_PREFIX}${secret.toString()}`);
	}
});

app.listen(PORT, () => {
	console.log(`Listening on port ${PORT}`);
});
