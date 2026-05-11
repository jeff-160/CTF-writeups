<?php
require_once 'config.php';
$wants_json = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /shop.php');
    exit;
}
$promo_code = $_POST['promo_code'] ?? 'NONE';
if (!is_string($promo_code)) {
    $promo_code = 'NONE';
}
$item = $_POST['item'] ?? '';
if (!isset($full_prices[$item])) {
    if ($wants_json) {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Unknown item.']);
        exit;
    }
    header('Location: /shop.php?err=' . urlencode('Unknown item.'));
    exit;
}
if ($promo_code === 'QUILLTHORN50') {
    $cost = (int)floor($full_prices[$item] * 0.5);
} else {
    $cost = $full_prices[$item];
}
$balance = get_balance();
if ($balance < $cost) {
    if ($wants_json) {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Insufficient Gold! You need ' . $cost . ' but only have ' . $balance . '.']);
        exit;
    }
    header('Location: /shop.php?err=' . urlencode('Insufficient Gold! You need ' . $cost . ' but only have ' . $balance . '.'));
    exit;
}
deduct_balance($cost);
add_to_inventory($item);
$is_legendary = ($item === 'wand_prismatic_fury');
$wand_name = $wands[$item]['name'] ?? $item;
$wand_icon = $wands[$item]['icon'] ?? '';
if ($is_legendary) {
    $flag = trim(file_get_contents('/flag.txt'));
}
if ($wants_json) {
    header('Content-Type: application/json');
    $response = [
        'success' => true,
        'wand_name' => $wand_name,
        'icon' => $wand_icon,
        'cost' => $cost,
        'new_balance' => get_balance(),
        'legendary' => $is_legendary,
    ];
    if ($is_legendary) {
        $response['flag'] = $flag;
    }
    echo json_encode($response);
    exit;
}
if ($is_legendary) {
    $msg = 'The Wand of Prismatic Fury crackles with energy and reveals a secret: ' . $flag;
} else {
    $msg = 'You purchased ' . $wand_name . ' for ' . $cost . ' Gold!';
}
header('Location: /shop.php?msg=' . urlencode($msg));
exit;
