import Recipe from './models/Recipe.js';

const decoys = [
    {
        owner: 'Brenna the Brewmaster',
        name: 'Healing Salve',
        description: 'A staple of every field medic\'s kit, this balm knits torn flesh and soothes burns when applied directly to the wound. Brenna learned the recipe from her grandmother, a battlefield herbalist who served in the Thornwall Campaign. The original formula called for dried Moonpetal, but Brenna discovered that fresh petals produce a salve three times as potent.\n\nBest prepared in small batches, as the mixture loses efficacy after a fortnight even in a cool cellar. The salve turns a faint silver when properly mixed — if it stays green, the Spring Water was too warm and the batch should be discarded.\n\nBrenna recommends testing each batch on a small scratch before trusting it with anything serious, as potency varies with the season of harvest. She marks her best batches with a blue ribbon and charges double for them.',
        ingredients: 'Silverleaf, Moonpetal, Spring Water',
        secretFormula: 'Basic herbal mixture',
    },
    {
        owner: 'Old Grint',
        name: 'Fire Resistance Draught',
        description: 'Grants the drinker temporary immunity to mundane flame for roughly half a bell, long enough to walk through a burning building or handle molten metal barehanded. Blacksmiths swear by it, and more than one dragon hunter owes their life to a swig of Grint\'s brew before battle.\n\nThe Volcanic Ash must be sourced from Mount Cinderhollow specifically — Grint claims the mineral composition of other volcanoes produces an inferior ward that fails at the worst possible moment. He once lost an apprentice to an Ashpeak batch and has refused to use anything else since.\n\nThe draught tastes like scorched earth and leaves the tongue numb for an hour afterward, a side effect Grint considers a feature rather than a flaw. He says if you can still taste it, the batch is too weak to trust your life to.',
        ingredients: 'Firebloom, Iron Shavings, Volcanic Ash',
        secretFormula: 'Standard fire ward',
    },
    {
        owner: 'Mira Softpetal',
        name: 'Sleeping Tonic',
        description: 'A gentle draught that eases the restless into dreamless slumber within minutes of consumption, without the groggy aftermath of cruder sedatives. Mira insists on honey from the Whispering Meadows — no substitute will produce the same gentle descent into sleep.\n\nShe developed the formula after years of insomnia following the Siege of Glassbarrow, and now supplies it to half the city\'s physicians. An overdose merely extends the sleep rather than deepening it, making it remarkably safe compared to its competitors on the market.\n\nMira keeps a journal of over three hundred variations she tested before settling on this particular blend. She says the secret is not in any one ingredient but in the precise order of addition — the Chamomile must touch the honey before the Lavender Root, never after.',
        ingredients: 'Lavender Root, Chamomile Essence, Honey',
        secretFormula: 'Gentle sedative blend',
    },
    {
        owner: 'Tormund Ashforge',
        name: 'Strength Elixir',
        description: 'Doubles the drinker\'s raw physical strength for roughly one hour, turning even a scrawny apprentice into a force capable of bending iron bars. The crash afterward is brutal — Tormund recommends a full meal and a long nap once the effects fade, lest the drinker collapse wherever they stand.\n\nHe discovered the formula by accident while experimenting with Ogre\'s Blood as a metallurgical additive. A spill, a cut finger, and a sneeze later, he found himself able to lift his entire workbench with one hand. The Red Ginseng must be aged at least three years for full potency.\n\nTormund personally tests every batch by attempting to lift his anvil, which weighs as much as a small horse. If it comes off the ground with one hand, the elixir is ready. He has broken two floorboards this way and considers the repair costs a necessary expense.',
        ingredients: "Ogre's Blood, Iron Bark, Red Ginseng",
        secretFormula: 'Brute force infusion',
    },
    {
        owner: 'Sylvara Windwhisper',
        name: 'Invisibility Potion',
        description: 'Bends light around the drinker, rendering them completely unseen for a quarter-hour. The effect breaks immediately upon any aggressive action — a safeguard Sylvara deliberately built into the formula after an unfortunate incident involving a jealous suitor and a butter knife.\n\nShe warns against sneezing while invisible, as the partial shimmer that results is deeply unsettling for onlookers. The Ghostcap Mushrooms must be harvested under a new moon and kept in complete darkness until brewing — even a moment of sunlight renders them useless.\n\nSylvara also notes that the potion does not muffle sound or mask scent, a limitation that has tripped up more than one overconfident thief. She sells it primarily to stage performers and the occasional private investigator, and asks no questions about the latter.',
        ingredients: 'Ghostcap Mushroom, Moonstone Dust, Dew',
        secretFormula: 'Simple refraction formula',
    },
    {
        owner: 'Durgan Ironbrew',
        name: 'Antidote',
        description: 'A broad-spectrum remedy effective against most common poisons found in the Glassbarrow region, including Thornvine sap, Bog Adder venom, and the notorious Pallid Mushroom toxin. Durgan keeps a flask on his belt at all times — an old habit from his adventuring days.\n\nHe learned the hard way that poison rarely announces itself. During a delve beneath the Ashen Crypts, three of his companions fell to a trapped chest before anyone thought to check for coated needles. Durgan has carried the antidote every day since.\n\nThe formula neutralizes toxins within minutes, though it leaves a bitter taste of charcoal that lingers for hours. Durgan sources his Milk Thistle exclusively from the banks of the Clearrun River, claiming the soil there produces plants with twice the detoxifying strength of those grown elsewhere.',
        ingredients: 'Charcoal, Milk Thistle, Purified Water',
        secretFormula: 'Universal toxin binder',
    },
    {
        owner: 'Elara Nightshade',
        name: 'Poison Blade Oil',
        description: 'Applied to a weapon\'s edge, this viscous oil delivers a numbing toxin on the first cut that spreads through the bloodstream within seconds. The victim\'s extremities go cold and clumsy, making it nearly impossible to fight back or flee effectively.\n\nElara sells it only to licensed hunters and guild-contracted pest controllers — officially. In practice, she exercises her own judgment about who deserves access to her work, and has been known to refuse payment from customers she finds distasteful.\n\nThe Viper Venom must be fresh, no more than three days old, and the Nightshade harvested at the peak of its flowering cycle. She applies the oil wearing thick leather gloves and a cloth mask, and strongly advises her customers do the same. One careless drop on bare skin is enough to numb an entire hand for a day.',
        ingredients: 'Nightshade Extract, Viper Venom, Wax',
        secretFormula: 'Concentrated contact toxin',
    },
    {
        owner: 'Pip Tinkerton',
        name: 'Mana Restoration Philter',
        description: 'Replenishes spent arcane reserves over the course of several minutes, allowing a depleted spellcaster to return to the fight without the usual hours of meditation required for natural recovery. Tastes faintly of copper and ozone.\n\nPip has tried dozens of flavoring agents to make it more palatable, but none survive the brewing process intact. He once added raspberry extract and produced something that tasted like a thunderstorm in a fruit market, which he considered worse than the original.\n\nHe advises against drinking more than two in a single day; the headaches from arcane overchannel are legendary among his regular customers, and three doses have been known to cause temporary blindness and an unsettling ringing in the ears that sounds like distant chanting in a language no one can identify.',
        ingredients: 'Arcane Crystal, Blue Lotus, Ether',
        secretFormula: 'Mana channel realignment',
    },
    {
        owner: 'Hagatha Moorfen',
        name: 'Swamp Gas Bomb',
        description: 'A thrown alchemical weapon that bursts into a choking cloud of nauseating yellow-green fumes on impact, covering a space roughly ten paces across and lingering for several minutes in still air.\n\nHagatha originally developed it to clear a nest of Bograts from her cellar, but it proved to have broader applications in crowd dispersal, siege warfare, and discouraging unwanted visitors. The city guard has placed three standing orders this year alone.\n\nThe Toad Mucus acts as a binding agent that keeps the gas cloud low to the ground rather than dissipating upward. She recommends holding your breath and throwing from upwind, and notes with some pride that no one has ever visited her cottage uninvited twice. The smell clings to clothing for days.',
        ingredients: 'Bog Sulfur, Toad Mucus, Dried Peat',
        secretFormula: 'Volatile gas compound',
    },
    {
        owner: 'Caelan Brightwater',
        name: 'Purification Draught',
        description: 'Cleanses the body of disease, minor curses, and lingering magical afflictions that resist conventional treatment. The ritual of preparation is as important as the ingredients themselves.\n\nCaelan brews each batch at dawn under open sky, reciting the Litany of Clear Waters passed down through six generations of Brightwater healers. The Silver Dust must be consecrated beforehand, and the White Sage burned rather than steeped, releasing its essence through sacred smoke that is captured in the liquid.\n\nCaelan has never sold the draught for profit, offering it freely to those in genuine need, though he accepts donations of rare herbs in return. He says the Litany loses its power if spoken with a merchant\'s heart, and he believes this completely.',
        ingredients: 'Holy Water, Silver Dust, White Sage',
        secretFormula: 'Sacred cleansing ritual',
    },
    {
        owner: 'Nyx Shadowmere',
        name: 'Darkvision Tincture',
        description: 'Grants perfect sight in total darkness for several hours, rendering even the deepest cavern as clear as a sunlit meadow. The tincture is popular among miners, sewer workers, and those whose business is best conducted after dark.\n\nSide effects include extreme light sensitivity — stepping into daylight while the tincture is active causes searing pain behind the eyes — and an unnerving reflective sheen to the pupils that tends to frighten small children and animals alike. Best taken well after sunset with no plans to surface before dawn.\n\nThe Cat\'s Eye Gem must be ground to a powder finer than flour for proper absorption, a process that takes Nyx the better part of a day using a mortar she inherited from her mentor, a Drow alchemist whose name she has never shared with anyone.',
        ingredients: "Cat's Eye Gem, Bat Guano, Ink",
        secretFormula: 'Pupil dilation extract',
    },
    {
        owner: 'Rufus Copperkettle',
        name: 'Hangover Cure',
        description: 'Rufus\'s most popular product by a considerable margin, accounting for nearly half his annual revenue and the entirety of his reputation in Glassbarrow\'s tavern district. Eliminates headache, nausea, and the existential dread that follows a night at the Brass Tankard.\n\nThe cure takes effect within minutes of consumption. He brews it in batches of fifty every Restday morning, and still runs out by midday. The queue outside his shop on Restday is a landmark the locals point out to tourists.\n\nThe secret is in the Willow Bark, which must be stripped from living trees during the first frost — dried bark from the apothecary shelf simply will not do. Rufus has considered raising his prices but fears the wrath of the city\'s barkeeps, who consider his cure an essential public service and have made this opinion known in no uncertain terms.',
        ingredients: 'Ginger Root, Lemon Zest, Willow Bark',
        secretFormula: 'Morning after remedy',
    },
];

export async function seed(flag) {
    const count = await Recipe.countDocuments();
    if (count > 0) {
        console.log('Database already seeded, skipping');
        return;
    }

    console.log('Seeding database...');

    await Recipe.insertMany(decoys);

    const target = await Recipe.create({
        owner: 'Archmage Veldris',
        name: 'Elixir of Astral Convergence',
        description: 'The most sought-after formula in the known realm, and the subject of more failed imitations than any other recipe in the Silver Flask\'s long history. Said to open the drinker\'s mind to the space between stars, granting visions of distant planes and knowledge that transcends mortal comprehension.\n\nThe experience lasts only minutes but leaves the drinker permanently changed — wiser, most agree, though others whisper of those who saw too much and never fully returned to themselves. The Archmage himself is said to have brewed it only seven times in his long life.\n\nOnly Veldris has ever successfully produced it, and he guards the formula with enchantments that would make a dragon think twice. Those who have attempted to reverse-engineer the elixir from its ingredients alone have produced nothing but expensive headaches and, in one memorable case, a small fire that burned for three days without consuming anything.',
        ingredients: 'Ancient herbs, Starlight essence, [SECRET FORMULA REQUIRED]',
        secretFormula: flag,
    });
    console.log(`Target recipe ID: ${target._id}`);

    console.log('Seeding complete');
}
