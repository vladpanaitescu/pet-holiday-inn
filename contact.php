<?php
// Trimite cererea de rezervare pe email. Setează adresa reală mai jos.
const TO = 'petholidayinn@gmail.com';
const FROM = 'no-reply@petholidayinn.ro'; // trebuie sa fie o adresa de pe domeniul site-ului, altfel Gmail poate respinge mesajul

date_default_timezone_set('Europe/Bucharest');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !empty($_POST['website'])) {
    http_response_code(400);
    exit(json_encode(['ok' => false]));
}

$f = fn($k) => trim(strip_tags($_POST[$k] ?? ''));
$data = [
    'Nume' => $f('nume'), 'Telefon' => $f('telefon'), 'Email' => $f('email'),
    'Animal' => $f('animal'), 'Nume animal' => $f('nume_animal'), 'Cabana' => $f('cabana'),
    'Check-in' => $f('checkin'), 'Check-out' => $f('checkout'), 'Pet Taxi' => $f('pet_taxi') ?: 'Nu',
    'Afectiuni / tratament' => $f('afectiuni') . ($f('afectiuni_detalii') ? ' - ' . $f('afectiuni_detalii') : ''),
    'Se intelege cu alti caini' => $f('sociabil') ?: '-',
    'Telefon urgente' => $f('telefon_urgenta') ?: '-',
    'Mesaj' => $f('mesaj'),
    'Regulament acceptat' => 'Da, la ' . date('d.m.Y H:i') . ' (IP ' . ($_SERVER['REMOTE_ADDR'] ?? '-') . ')',
];

if (!$data['Nume'] || !$data['Telefon'] || !filter_var($data['Email'], FILTER_VALIDATE_EMAIL) || !$data['Check-in'] || !$data['Check-out'] || empty($_POST['gdpr']) || empty($_POST['regulament']) || !$f('afectiuni') || ($f('afectiuni') === 'Da' && !$f('afectiuni_detalii'))) {
    http_response_code(422);
    exit(json_encode(['ok' => false, 'error' => 'Date incomplete.']));
}

$body = "Cerere noua de rezervare de pe site:\n\n";
foreach ($data as $k => $v) $body .= "$k: $v\n";

$headers = [
    'From: Pet Holiday <' . FROM . '>',
    'Reply-To: ' . str_replace(["\r", "\n"], '', $data['Email']),
    'Content-Type: text/plain; charset=utf-8',
];
$subject = '=?UTF-8?B?' . base64_encode('Rezervare: ' . $data['Nume'] . ' (' . $data['Check-in'] . ' - ' . $data['Check-out'] . ')') . '?=';

$ok = mail(TO, $subject, $body, implode("\r\n", $headers));
http_response_code($ok ? 200 : 500);
echo json_encode(['ok' => $ok]);
