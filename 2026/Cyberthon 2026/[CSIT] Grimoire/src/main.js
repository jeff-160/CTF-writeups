// Arcane Grimoire - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initSpellForm();
    loadAvailableSpells();
    loadGrimoireVersion();
    initRuneHandlers();
});

function initSpellForm() {
    const form = document.getElementById('spellForm');
    const resultSection = document.getElementById('spellResult');
    const resultContent = document.getElementById('resultContent');
    const closeBtn = document.getElementById('closeResult');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = document.getElementById('spellName').value;
        const formula = document.getElementById('spellFormula').value;
        const rune = document.getElementById('spellRune').value;

        const btn = form.querySelector('.compile-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span class="loading">⚡ Compiling...</span>';
        btn.disabled = true;

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    formula: formula
                })
            });

            const data = await response.json();

            if (data.success) {
                resultContent.innerHTML = '<div class="success-message">' +
                    data.compilation +
                    '</div>';
            } else {
                resultContent.innerHTML = '<div class="error-message">' +
                    data.error +
                    (data.hint ? '<div class="hint">' + data.hint + '</div>' : '') +
                    '</div>';
            }
        } catch (error) {
            resultContent.innerHTML = '<div class="error-message">' +
                'The arcane pathways are disrupted. ' +
                'Please try again.' +
                '</div>';
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
            resultSection.style.display = 'block';
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }
    });

    closeBtn.addEventListener('click', function() {
        resultSection.style.display = 'none';
    });
}

async function loadAvailableSpells() {
    try {
        const response = await fetch('/spells');
        const data = await response.json();
        document.getElementById('availableSpells').textContent =
            data.spells.join(', ');
    } catch (error) {
        document.getElementById('availableSpells').textContent =
            'Unable to retrieve spells from the grimoire.';
    }
}

async function loadGrimoireVersion() {
    document.getElementById('grimoireVersion').textContent = GRIMOIRE_VERSION;
}

function initRuneHandlers() {
    const runeItems = document.querySelectorAll('.rune-item');

    runeItems.forEach(function(item) {
        item.addEventListener('click', async function() {
            const runeName = this.getAttribute('data-rune');
            try {
                const response = await fetch(`/rune/${runeName}`);
                const data = await response.json();
                document.getElementById('spellRune').value = runeName;

                const hint = document.querySelector('.formula-hint');
                const originalHint = hint.textContent;
                hint.textContent =
                    data.description + ' ' + originalHint;

                setTimeout(() => {
                    hint.textContent = originalHint;
                }, 3000);
            } catch (error) {
                console.error('Error fetching rune:', error);
            }
        });
    });
}