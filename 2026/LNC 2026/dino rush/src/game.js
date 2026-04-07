// Google Dino Game Engine v2.3.1

(function(_0x4e2a, _0x3b1f) {
    const _0x2c8d = function(_0x5a1b) {
        while (--_0x5a1b) { _0x4e2a.push(_0x4e2a.shift()); }
    };
    _0x2c8d(++_0x3b1f);
}(["d1n0","_s3c","r3t_","k3y_","2403"], 0x2));

const _cfg = (function() {
    const _d = ["_s3c","2403","d1n0","k3y_","r3t_"];
    const _k = [_d[2], _d[0], _d[4], _d[3], _d[1]].join('');
    const _s = { threshold: 0x270F, version: "2.3.1" };
    return { _k, _s };
})();

async function _hmac(key, message) {
    const enc = new TextEncoder();
    const cryptoKey = await crypto.subtle.importKey(
        "raw", enc.encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
    );
    const sig = await crypto.subtle.sign("HMAC", cryptoKey, enc.encode(message));
    return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function buildScoreToken(score) {
    const ts = Math.floor(Date.now() / 1000);
    const sig = await _hmac(_cfg._k, `${score}:${ts}`);
    const payload = JSON.stringify({ score, ts, sig });
    return btoa(payload).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

const S          = 3;
const GROUND_Y   = 230;
const DINO_ROWS  = 16;
const DINO_COLS  = 18;
const GRAVITY    = 1800;
const JUMP_FORCE = -600; 
const BASE_SPEED = 360;
const SCORE_RATE = 10; 

function makeDinoSprite(legFrame) {
    return function drawDino(ctx, x, y) {
        ctx.fillStyle = '#535353';

        const head = [
            [10,0],[11,0],[12,0],[13,0],[14,0],[15,0],[16,0],
            [9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],
            [9,2],[10,2],[11,2],[12,2],[13,2],[14,2],[16,2],[17,2],
            [9,3],[10,3],[11,3],[12,3],[13,3],[14,3],[15,3],[16,3],[17,3],
            [9,4],[10,4],[11,4],[12,4],[13,4],[14,4],[15,4],[16,4],
            [10,5],[11,5],[12,5],[14,5],[15,5],[16,5],
            [11,6],[12,6],[13,6],
        ];

        const body = [
            [8,5],[9,5],[8,6],[9,6],[10,6],[11,6],
            [3,7],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7],[10,7],[11,7],
            [3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8],[11,8],
            [3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],
            [2,10],[3,10],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],
            [2,11],[3,11],[4,11],[5,11],[6,11],[7,11],[8,11],
            [0,9],[1,9],[2,9],[0,10],[1,10],[0,11],
        ];

        let legs = [];
        if (legFrame === 2) {
            legs = [[4,12],[5,12],[7,12],[8,12],[4,13],[5,13],[7,13],[8,13],[4,14],[5,14],[7,14],[8,14]];
        } else if (legFrame === 0) {
            legs = [[3,12],[4,12],[7,12],[8,12],[3,13],[4,13],[7,13],[3,14],[4,14],[8,14],[9,14]];
        } else if (legFrame === 1) {
            legs = [[3,12],[4,12],[7,12],[8,12],[4,13],[7,13],[8,13],[4,15],[5,15],[7,14],[8,14]];
        } else {
            legs = [[2,12],[3,12],[4,12],[7,12],[8,12],[9,12],[2,13],[3,13],[8,13],[9,13],[2,14],[3,14],[8,14],[9,14]];
        }

        for (const [c, r] of [...head, ...body, ...legs]) {
            ctx.fillRect(x + c * S, y + r * S, S, S);
        }
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x + 15 * S, y + 2 * S, S, S);

        if (legFrame === 3) {
            ctx.fillStyle = '#535353';
            for (const [c,r] of [[13,1],[15,1],[14,2],[13,3],[15,3]])
                ctx.fillRect(x + c*S, y + r*S, S, S);
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x + 15 * S, y + 2 * S, S, S);
        }
    };
}

const DINO_RUN_A = makeDinoSprite(0);
const DINO_RUN_B = makeDinoSprite(1);
const DINO_JUMP  = makeDinoSprite(2);
const DINO_DEAD  = makeDinoSprite(3);
const DINO_HIT   = { x1: 3, y1: 1, x2: 17, y2: 15 };

function drawCactusTall(ctx, x, y) {
    ctx.fillStyle = '#535353';
    for (let r = 0; r <= 12; r++) ctx.fillRect(x + 2*S, y + r*S, S*2, S);
    for (let r = 2; r <= 7;  r++) ctx.fillRect(x + 0*S, y + r*S, S*2, S);
    for (let r = 1; r <= 6;  r++) ctx.fillRect(x + 4*S, y + r*S, S*2, S);
}
function drawCactusDouble(ctx, x, y) {
    ctx.fillStyle = '#535353';
    for (let i = 0; i < 2; i++) {
        const ox = x + i * 9 * S;
        for (let r = 3; r <= 10; r++) ctx.fillRect(ox + 2*S, y + r*S, S*2, S);
        for (let r = 3; r <= 7;  r++) ctx.fillRect(ox + 0*S, y + r*S, S*2, S);
        for (let r = 3; r <= 7;  r++) ctx.fillRect(ox + 4*S, y + r*S, S*2, S);
    }
}
function drawCactusTriple(ctx, x, y) {
    ctx.fillStyle = '#535353';
    for (let i = 0; i < 3; i++) {
        const ox = x + i * 7 * S;
        for (let r = 4; r <= 9; r++) ctx.fillRect(ox + 2*S, y + r*S, S*2, S);
        for (let r = 4; r <= 7; r++) ctx.fillRect(ox + 0*S, y + r*S, S*2, S);
        for (let r = 4; r <= 7; r++) ctx.fillRect(ox + 4*S, y + r*S, S*2, S);
    }
}

const CACTUS_TYPES = [
    { draw: drawCactusTall,   h: 13, w: 6  },
    { draw: drawCactusDouble, h: 11, w: 15 },
    { draw: drawCactusTriple, h: 10, w: 20 },
];

const GAME = {
    score:      0,
    scoreAccum: 0, 
    speed:      BASE_SPEED,
    running:    false,
    over:       false,
    obstacles:  [],
    clouds:     [],
    dino:       { offsetY: 0, vy: 0, grounded: true },
    canvas:     null,
    ctx:        null,
    lastTime:   null,
    legTime:    0,
    legFrame:   0,
    cloudTimer: 0,
    spawnTimer: 0,
};

let hiScore = 0;

function dinoGroundY() { return GROUND_Y - DINO_ROWS * S; }

function spawnObstacle() {
    GAME.obstacles.push({ x: GAME.canvas.width + 40, type: Math.floor(Math.random() * 3) });
}
function spawnCloud() {
    GAME.clouds.push({ x: GAME.canvas.width + 60, y: 30 + Math.random() * 70 });
}

function reset() {
    GAME.score      = 0;
    GAME.scoreAccum = 0;
    GAME.speed      = BASE_SPEED;
    GAME.running    = true;
    GAME.over       = false;
    GAME.obstacles  = [];
    GAME.clouds     = [];
    GAME.dino       = { offsetY: 0, vy: 0, grounded: true };
    GAME.lastTime   = null;
    GAME.legTime    = 0;
    GAME.legFrame   = 0;
    GAME.cloudTimer = 0;
    GAME.spawnTimer = 0;
    updateScoreDisplay(0);
    requestAnimationFrame(loop);
}

function jump() {
    if (GAME.dino.grounded && GAME.running && !GAME.over) {
        GAME.dino.vy = JUMP_FORCE;
        GAME.dino.grounded = false;
    }
}

function updateScoreDisplay(s) {
    GAME.score = s;
    document.getElementById('score-display').textContent = String(s).padStart(5, '0');
    if (s > hiScore) {
        hiScore = s;
        document.getElementById('hi-display').textContent = String(hiScore).padStart(5, '0');
    }
}

function loop(timestamp) {
    if (!GAME.running || GAME.over) return;

    if (GAME.lastTime === null) GAME.lastTime = timestamp;
    const dt = Math.min((timestamp - GAME.lastTime) / 1000, 0.1);
    GAME.lastTime = timestamp;

    const ctx = GAME.ctx;
    const W   = GAME.canvas.width;

    ctx.clearRect(0, 0, W, GAME.canvas.height);

    GAME.cloudTimer += dt;
    if (GAME.cloudTimer > 1.5) { spawnCloud(); GAME.cloudTimer = 0; }
    ctx.fillStyle = '#cccccc';
    for (let i = GAME.clouds.length - 1; i >= 0; i--) {
        const cl = GAME.clouds[i];
        cl.x -= 90 * dt;
        ctx.fillRect(cl.x,      cl.y,     46, 6);
        ctx.fillRect(cl.x + 6,  cl.y - 5, 24, 5);
        ctx.fillRect(cl.x + 14, cl.y - 9, 12, 4);
        if (cl.x + 46 < 0) GAME.clouds.splice(i, 1);
    }

    ctx.fillStyle = '#535353';
    ctx.fillRect(0, GROUND_Y, W, 2);

    GAME.dino.vy      += GRAVITY * dt;
    GAME.dino.offsetY += GAME.dino.vy * dt;
    if (GAME.dino.offsetY >= 0) {
        GAME.dino.offsetY = 0;
        GAME.dino.vy      = 0;
        GAME.dino.grounded = true;
    }

    if (GAME.dino.grounded) {
        GAME.legTime += dt;
        if (GAME.legTime >= 0.1) { GAME.legFrame ^= 1; GAME.legTime = 0; }
    }

    const dinoX = 60;
    const dinoY = dinoGroundY() + GAME.dino.offsetY;
    const sprite = GAME.dino.grounded
        ? (GAME.legFrame === 0 ? DINO_RUN_A : DINO_RUN_B)
        : DINO_JUMP;
    sprite(ctx, dinoX, dinoY);

    const spawnInterval = Math.max(0.9, 1.8 - GAME.score * 0.00015);
    GAME.spawnTimer += dt;
    if (GAME.spawnTimer >= spawnInterval) { spawnObstacle(); GAME.spawnTimer = 0; }

    for (let i = GAME.obstacles.length - 1; i >= 0; i--) {
        const o  = GAME.obstacles[i];
        o.x -= GAME.speed * dt;

        const ct      = CACTUS_TYPES[o.type];
        const cactusY = GROUND_Y - ct.h * S;
        ct.draw(ctx, o.x, cactusY);

        const dLeft   = dinoX + DINO_HIT.x1 * S;
        const dRight  = dinoX + DINO_HIT.x2 * S;
        const dTop    = dinoY  + DINO_HIT.y1 * S;
        const dBottom = dinoY  + DINO_HIT.y2 * S;
        const oLeft   = o.x;
        const oRight  = o.x + ct.w * S;
        const oTop    = cactusY;
        const oBottom = GROUND_Y;

        if (dRight - 3 > oLeft && dLeft + 3 < oRight &&
            dBottom - 3 > oTop  && dTop < oBottom) {
            doGameOver(dinoX, dinoY);
            return;
        }

        if (o.x + ct.w * S + 10 < 0) GAME.obstacles.splice(i, 1);
    }

    GAME.scoreAccum += SCORE_RATE * dt;
    if (GAME.scoreAccum >= 1) {
        const gained = Math.floor(GAME.scoreAccum);
        GAME.scoreAccum -= gained;
        updateScoreDisplay(GAME.score + gained);
    }

    GAME.speed = BASE_SPEED + Math.floor(GAME.score / 200) * 40;

    if (GAME.score >= _cfg._s.threshold) {
        doGameOver(dinoX, dinoY);
        return;
    }

    requestAnimationFrame(loop);
}

async function doGameOver(dinoX, dinoY) {
    GAME.over    = true;
    GAME.running = false;
    const ctx    = GAME.ctx;
    const W      = GAME.canvas.width;
    const won    = GAME.score >= _cfg._s.threshold;

    ctx.clearRect(dinoX, dinoY, DINO_COLS * S, DINO_ROWS * S);
    if (won) DINO_JUMP(ctx, dinoX, dinoY);
    else     DINO_DEAD(ctx, dinoX, dinoY);

    if (won) {
        ctx.fillStyle = '#1a7a0a';
        ctx.font = 'bold 20px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('S C O R E  R E A C H E D  —  TOKEN GENERATED', W / 2, GROUND_Y - 90);
        ctx.font = '13px "Courier New"';
        ctx.fillStyle = '#535353';
        ctx.fillText('paste the token below and submit', W / 2, GROUND_Y - 64);
        ctx.fillText('▶▶  SPACE / CLICK to play again', W / 2, GROUND_Y - 44);
    } else {
        ctx.fillStyle = '#535353';
        ctx.font = 'bold 20px "Courier New"';
        ctx.textAlign = 'center';
        ctx.fillText('G A M E  O V E R', W / 2, GROUND_Y - 90);
        ctx.font = '14px "Courier New"';
        ctx.fillStyle = '#999';
        ctx.fillText('▶▶  SPACE / CLICK to restart', W / 2, GROUND_Y - 62);
    }

    if (won) {
        const token = await buildScoreToken(GAME.score);
        const inp   = document.getElementById('token-input');
        if (inp) {
            inp.value = token;
            inp.style.borderColor = '#39ff14';
            inp.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
}

function init() {
    GAME.canvas = document.getElementById('dino-canvas');
    GAME.ctx    = GAME.canvas.getContext('2d');

    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space' || e.code === 'ArrowUp') {
            e.preventDefault();
            if (!GAME.running || GAME.over) reset();
            else jump();
        }
    });
    GAME.canvas.addEventListener('click', () => {
        if (!GAME.running || GAME.over) reset();
        else jump();
    });

    const ctx = GAME.ctx;
    const W   = GAME.canvas.width;
    ctx.fillStyle = '#535353';
    ctx.fillRect(0, GROUND_Y, W, 2);
    DINO_JUMP(ctx, 60, dinoGroundY());
    ctx.font = 'bold 16px "Courier New"';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#999';
    ctx.fillText('press SPACE or click to start', W / 2, GROUND_Y - 70);
}

window.addEventListener('load', init);