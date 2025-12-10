const db = Object.create(null)
db.memo = Object.create(null)
db.nonce = null

const createMemo = (id, content, sourceEncoding) =>{
    db.memo[id] = Object.create(null);
    db.memo[id].content = content;
    db.memo[id].sourceEncoding = sourceEncoding;
}

module.exports = {
    db,
    createMemo
}