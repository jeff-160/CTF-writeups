const express = require('express');
const fs = require('fs');
const app = express();

app.use(express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf.toString();
  }
}));

let FLAG;
try {
  FLAG = fs.readFileSync('/app/flag.txt', 'utf8').trim();
} catch {
  FLAG = 'CTF{test_flag_duplicate_key_canonicalization}';
}
const SECRET_CODEWORD = process.env.SECRET_CODEWORD || 'unguessable-32-char-codeword-xyz';
const PORT = process.env.PORT || 3002;

const DESTINATIONS = {
  'PLAINS_OUTPOST': {
    name: 'Plains Outpost',
    description: 'A humble trading post on the windswept plains.',
    coordinates: '42.3601° N, 71.0589° W',
    threat_level: 'Minimal',
    restricted: false,
    flag: null
  },
  'FOREST_RELAY': {
    name: 'Forest Relay Station',
    description: 'A waypoint deep in the ancient woods.',
    coordinates: '47.6062° N, 122.3321° W',
    threat_level: 'Low',
    restricted: false,
    flag: null
  },
  'MOUNTAIN_PEAK': {
    name: 'Crystal Mountain Peak',
    description: 'A breathtaking summit where crystalline formations pierce the sky.',
    coordinates: '39.7392° N, 104.9903° W',
    threat_level: 'Moderate',
    restricted: false,
    flag: null
  },
  'DESERT_OASIS': {
    name: 'Mirage Desert Oasis',
    description: 'A mysterious sanctuary hidden in the endless sands.',
    coordinates: '31.2304° N, 121.4737° E',
    threat_level: 'Moderate',
    restricted: false,
    flag: null
  },
  'SANCTUM_OF_THE_VOID': {
    name: 'Sanctum of the Void',
    description: 'A forbidden realm where reality fractures. Rank S clearance required.',
    coordinates: '??? (Classified)',
    threat_level: 'EXTREME',
    restricted: true,
    flag: FLAG
  }
};

let nonceCounter = 1000;

function generateNonce() {
  nonceCounter++;
  return `nonce_${nonceCounter}`;
}

app.post('/api/rune/issue', (req, res) => {
  try {
    const { destination } = req.body;

    if (!destination) {
      return res.status(400).json({ error: 'Destination not specified' });
    }

    if (!DESTINATIONS[destination]) {
      return res.status(404).json({ error: 'Unknown destination' });
    }

    if (DESTINATIONS[destination].restricted) {
      return res.status(403).json({
        error: 'Destination restricted. Rank S clearance required.',
        message: 'For S-Rank access, use /api/rune/issue_s_rank'
      });
    }

    const payload = JSON.stringify({
      destination: destination,
      nonce: generateNonce()
    });

    console.log(`[ARCANUM] Issuing rune for: ${destination}`);

    res.json({
      payload: payload,
      destination: destination,
      message: `Travel rune issued for ${DESTINATIONS[destination].name}`
    });

  } catch (error) {
    console.error('Error issuing rune:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/rune/issue_s_rank', (req, res) => {
  try {
    const { codeword } = req.body;

    if (!codeword) {
      return res.status(400).json({ error: 'Codeword required' });
    }

    if (codeword !== SECRET_CODEWORD) {
      console.log(`[ARCANUM] Failed S-Rank attempt with invalid codeword`);
      return res.status(403).json({
        error: 'Invalid codeword. Only S-Rank travelers may access this endpoint.'
      });
    }

    const payload = JSON.stringify({
      destination: 'SANCTUM_OF_THE_VOID',
      nonce: generateNonce()
    });

    console.log(`[ARCANUM] Issuing S-Rank rune for Sanctum`);

    res.json({
      payload: payload,
      message: 'S-Rank travel rune issued for Sanctum of the Void'
    });

  } catch (error) {
    console.error('Error issuing S-Rank rune:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/portal/warp', (req, res) => {
  try {
    if (req.rawBody && req.rawBody.includes('SANCTUM_OF_THE_VOID')) {
      console.log(`[ARCANUM] ⚠️  Blocked S-Rank warp attempt`);
      return res.status(403).json({ error: 'Warp failed' });
    }

    const { destination, nonce } = req.body;

    if (!destination) {
      return res.status(400).json({ error: 'Destination not specified' });
    }

    if (!nonce) {
      return res.status(400).json({ error: 'Nonce not specified' });
    }

    const destinationData = DESTINATIONS[destination];

    if (!destinationData) {
      return res.status(404).json({
        error: 'Unknown destination',
        message: `The destination "${destination}" does not exist.`
      });
    }

    console.log(`[ARCANUM] Processing warp to: ${destination}`);

    const response = {
      success: true,
      destination: destination,
      name: destinationData.name,
      description: destinationData.description,
      coordinates: destinationData.coordinates,
      threat_level: destinationData.threat_level,
      nonce: nonce
    };

    if (destinationData.flag) {
      response.flag = destinationData.flag;
      console.log(`[ARCANUM] ⚠️  FLAG REVEALED for ${destination}!`);
    }

    res.json(response);

  } catch (error) {
    console.error('Error processing warp:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'arcanum' });
});

app.listen(PORT, () => {
  console.log(`Arcanum listening on port ${PORT}`);
});
