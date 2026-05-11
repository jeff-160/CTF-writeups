import mongoose from 'mongoose';

const recipeSchema = new mongoose.Schema({
    owner:         { type: String, required: true },
    name:          { type: String, required: true },
    description:   { type: String },
    ingredients:   { type: String, required: true },
    secretFormula: { type: String, select: false },
});

export default mongoose.model('Recipe', recipeSchema);
