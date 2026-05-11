import { Router } from 'express';
import Recipe from '../models/Recipe.js';

const router = Router();

router.get('/', async (req, res) => {
    try {
        const query = Recipe.find();
        if (req.query.fields) {
            query.select(req.query.fields);
        }
        res.json(await query);
    } catch (err) {
        res.status(500).json({ error: 'internal error' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const query = Recipe.findById(req.params.id);
        if (req.query.fields) {
            query.select(req.query.fields);
        }
        const recipe = await query;
        if (!recipe) return res.status(404).json({ error: 'not found' });
        res.json(recipe);
    } catch (err) {
        res.status(500).json({ error: 'internal error' });
    }
});

export default router;
