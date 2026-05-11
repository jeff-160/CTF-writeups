<?php
require_once 'config.php';
if (!is_registered()) {
    header('Location: /');
    exit;
}
$message = $_GET['msg'] ?? '';
$error = $_GET['err'] ?? '';
$inventory = get_inventory();
$normal_wands = array_filter($wands, fn($k) => $k !== 'wand_prismatic_fury', ARRAY_FILTER_USE_KEY);
$legendary_key = 'wand_prismatic_fury';
$legendary_wand = $wands[$legendary_key];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quillthorn's Emporium - Shop</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body class="page-shop">
    <header class="shop-header">
        <div class="header-inner">
            <h1 class="header-title">Quillthorn's Emporium</h1>
            <div class="header-right">
                <span class="header-welcome">Welcome, <strong><?= htmlspecialchars(get_name()) ?></strong></span>
                <span class="header-divider">|</span>
                <span class="header-balance">Balance: <strong class="balance-amount"><?= get_balance() ?></strong> Gold</span>
                <span class="header-divider">|</span>
                <a href="/logout.php" class="btn btn-logout">Logout</a>
            </div>
        </div>
    </header>
    <main class="shop-main">
        <?php if ($message): ?>
            <div class="alert success"><?= htmlspecialchars($message) ?></div>
        <?php endif; ?>
        <?php if ($error): ?>
            <div class="alert error"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>
        <div class="sale-banner">
            <p>&#x2728; The <strong>QUILLTHORN50</strong> promo has ended! Huge thanks to everyone who grabbed half-price wands while it lasted. Quillthorn says he's "emotionally recovering" from the discounts. Normal pricing has resumed.</p>
        </div>
        <section class="shop-section">
            <h2 class="section-title">Wand Collection</h2>
            <div class="wand-grid">
                <?php $i = 0; foreach ($normal_wands as $key => $wand): ?>
                    <div class="wand-card" style="--card-index: <?= $i ?>">
                        <div class="wand-icon"><?= $wand['icon'] ?></div>
                        <h3 class="wand-name"><?= htmlspecialchars($wand['name']) ?></h3>
                        <p class="wand-price"><?= $full_prices[$key] ?> Gold</p>
                        <form method="POST" action="/buy.php" enctype="multipart/form-data">
                            <input type="hidden" name="promo_code" value="NONE">
                            <input type="hidden" name="item" value="<?= htmlspecialchars($key) ?>">
                            <button type="submit" class="btn btn-buy">Purchase</button>
                        </form>
                    </div>
                <?php $i++; endforeach; ?>
            </div>
        </section>
        <section class="shop-section legendary-section">
            <div class="legendary-card">
                <div class="legendary-card-inner">
                    <span class="legendary-badge">LEGENDARY</span>
                    <div class="wand-icon wand-icon-legendary"><?= $legendary_wand['icon'] ?></div>
                    <h3 class="wand-name wand-name-legendary"><?= htmlspecialchars($legendary_wand['name']) ?></h3>
                    <p class="wand-price wand-price-legendary"><?= $full_prices[$legendary_key] ?> Gold</p>
                    <form method="POST" action="/buy.php" enctype="multipart/form-data">
                        <input type="hidden" name="promo_code" value="NONE">
                        <input type="hidden" name="item" value="<?= htmlspecialchars($legendary_key) ?>">
                        <button type="submit" class="btn btn-buy btn-buy-legendary">Purchase</button>
                    </form>
                </div>
            </div>
        </section>
        <?php if (!empty($inventory)): ?>
        <section class="shop-section inventory-section">
            <h2 class="section-title">Your Wands</h2>
            <div class="inventory-list">
                <?php foreach ($inventory as $item): ?>
                    <span class="inventory-badge">
                        <?= htmlspecialchars($wands[$item]['icon'] ?? '') ?>
                        <?= htmlspecialchars($wands[$item]['name'] ?? $item) ?>
                    </span>
                <?php endforeach; ?>
            </div>
        </section>
        <?php endif; ?>
    </main>
    <div class="modal-overlay" id="modal-overlay">
        <div class="modal-card" id="modal-card"></div>
    </div>
    <script>
    document.querySelectorAll('form[action="/buy.php"]').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showModal('loading');
            fetch('/buy.php', {
                method: 'POST',
                headers: { 'Accept': 'application/json' },
                body: new FormData(form)
            })
            .then(function(resp) { return resp.json(); })
            .then(function(data) {
                if (data.success) {
                    document.querySelector('.balance-amount').textContent = data.new_balance;
                    showModal(data.legendary ? 'legendary' : 'success', data);
                    if (data.legendary || data.wand_name) {
                        addInventoryBadge(data.icon, data.wand_name);
                    }
                } else {
                    showModal('error', data);
                }
            })
            .catch(function() {
                form.submit();
            });
        });
    });
    function addInventoryBadge(icon, name) {
        var section = document.querySelector('.inventory-section');
        if (!section) {
            section = document.createElement('section');
            section.className = 'shop-section inventory-section';
            section.innerHTML = '<h2 class="section-title">Your Wands</h2><div class="inventory-list"></div>';
            document.querySelector('.shop-main').appendChild(section);
        }
        var list = section.querySelector('.inventory-list');
        var badge = document.createElement('span');
        badge.className = 'inventory-badge';
        badge.textContent = icon + ' ' + name;
        list.appendChild(badge);
    }
    function showModal(type, data) {
        data = data || {};
        var overlay = document.getElementById('modal-overlay');
        var card = document.getElementById('modal-card');
        overlay.classList.remove('active', 'modal-legendary');
        card.className = 'modal-card';
        if (type === 'loading') {
            card.innerHTML =
                '<div class="modal-icon modal-spin">&#x2728;</div>' +
                '<p class="modal-text">Casting purchase spell...</p>';
        } else if (type === 'success') {
            card.innerHTML =
                '<div class="modal-icon modal-success-icon">&#x2705;</div>' +
                '<h3 class="modal-heading">Wand Acquired!</h3>' +
                '<p class="modal-text">You purchased <strong>' + escapeHtml(data.wand_name) + '</strong> for ' + data.cost + ' Gold.</p>' +
                '<p class="modal-subtext">Remaining balance: ' + data.new_balance + ' Gold</p>' +
                '<button class="btn btn-modal-close" onclick="closeModal()">Continue Shopping</button>';
        } else if (type === 'error') {
            card.innerHTML =
                '<div class="modal-icon modal-error-icon">&#x274C;</div>' +
                '<h3 class="modal-heading">Purchase Failed</h3>' +
                '<p class="modal-text">' + escapeHtml(data.message || 'Unknown error') + '</p>' +
                '<button class="btn btn-modal-close" onclick="closeModal()">Dismiss</button>';
        } else if (type === 'legendary') {
            overlay.classList.add('modal-legendary');
            card.classList.add('modal-card-legendary');
            card.innerHTML =
                '<div class="modal-icon modal-legendary-icon">&#x1F308;</div>' +
                '<h3 class="modal-heading modal-heading-legendary">Legendary Wand Acquired!</h3>' +
                '<p class="modal-text">The <strong>Wand of Prismatic Fury</strong> crackles with energy!</p>' +
                '<div class="modal-flag" id="modal-flag"></div>' +
                '<button class="btn btn-modal-close" onclick="closeModal()">Close</button>';
            if (data.flag) {
                typewriterFlag(data.flag);
            }
        }
        requestAnimationFrame(function() {
            overlay.classList.add('active');
        });
    }
    function typewriterFlag(text) {
        var el = document.getElementById('modal-flag');
        if (!el) return;
        var i = 0;
        el.textContent = '';
        var interval = setInterval(function() {
            if (i < text.length) {
                el.textContent += text[i];
                i++;
            } else {
                clearInterval(interval);
            }
        }, 30);
    }
    function closeModal() {
        var overlay = document.getElementById('modal-overlay');
        overlay.classList.remove('active');
    }
    document.getElementById('modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });
    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }
    </script>
</body>
</html>
