for (let i = 0; i < 1000; i++) {
    try {
        const char = String.fromCodePoint(i);

        if (char == '.')
            continue;

        const parsed = require("querystring").unescape(`%ff${char}`);
        
        if (parsed.includes("."))
            console.log(i.toString(16), parsed);
    } catch {}
}