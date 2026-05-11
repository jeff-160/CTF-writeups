import { readFileSync } from 'fs';
import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import morgan from 'morgan';
import recipesRouter from './routes/recipes.js';
import { seed } from './seed.js';

// Read flag
function readFlag() {
    try {
        const f = readFileSync('/flag.txt', 'utf-8').trim();
        if (f) return f;
    } catch {}
    if (process.env.FLAG) return process.env.FLAG;
    return 'flag{placeholder_for_testing_do_not_submit}';
}

const flag = readFlag();
console.log(`Flag loaded (${flag.length} chars)`);

// MongoDB
const mongoURI = process.env.MONGO_URI || 'mongodb://localhost:27017/silverflask';
mongoose.set('sanitizeProjection', true);

await mongoose.connect(mongoURI);
console.log(`Connected to MongoDB at ${mongoURI}`);

// Seed
await seed(flag);

// Express
const app = express();
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.use('/api/recipes', recipesRouter);

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on :${port}`));
