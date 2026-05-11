<?php
session_start();
$wands = [
    'wand_apprentice'       => ['name' => "Apprentice's Practice Wand",  'icon' => "\xE2\x9C\xA8"],
    'wand_minor_sparks'     => ['name' => 'Wand of Minor Sparks',        'icon' => "\xE2\x9A\xA1"],
    'wand_oakwood'          => ['name' => 'Oakwood Channeling Rod',      'icon' => "\xF0\x9F\x8C\xBF"],
    'wand_gentle_breezes'   => ['name' => 'Wand of Gentle Breezes',      'icon' => "\xF0\x9F\x92\xA8"],
    'wand_silverthread'     => ['name' => 'Silverthread Focus',          'icon' => "\xF0\x9F\x94\xAE"],
    'wand_embertip'         => ['name' => 'Embertip Casting Wand',       'icon' => "\xF0\x9F\x94\xA5"],
    'wand_starlight'        => ['name' => 'Wand of Starlight',           'icon' => "\xE2\xAD\x90"],
    'wand_prismatic_fury'   => ['name' => 'Wand of Prismatic Fury',      'icon' => "\xF0\x9F\x8C\x88"],
];
$full_prices = [
    'wand_apprentice'       => 10,
    'wand_minor_sparks'     => 20,
    'wand_oakwood'          => 35,
    'wand_gentle_breezes'   => 50,
    'wand_silverthread'     => 75,
    'wand_embertip'         => 90,
    'wand_starlight'        => 100,
    'wand_prismatic_fury'   => 200,
];
function get_name(): string {
    return $_SESSION['customer_name'] ?? '';
}
function set_name(string $name): void {
    $_SESSION['customer_name'] = $name;
}
function is_registered(): bool {
    return isset($_SESSION['registered']) && $_SESSION['registered'] === true;
}
function register(string $name): void {
    $_SESSION['registered'] = true;
    $_SESSION['customer_name'] = $name;
    $_SESSION['balance'] = 100;
    $_SESSION['inventory'] = [];
}
function clear_session(): void {
    session_destroy();
}
function get_balance(): int {
    return $_SESSION['balance'] ?? 0;
}
function set_balance(int $amount): void {
    $_SESSION['balance'] = $amount;
}
function deduct_balance(int $amount): void {
    $_SESSION['balance'] -= $amount;
}
function add_to_inventory(string $item): void {
    if (!isset($_SESSION['inventory'])) {
        $_SESSION['inventory'] = [];
    }
    $_SESSION['inventory'][] = $item;
}
function get_inventory(): array {
    return $_SESSION['inventory'] ?? [];
}
