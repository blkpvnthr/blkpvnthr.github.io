<?php
// list-images.php
// Usage: /list-images.php?dir=/assets/images/LOGIC
// Returns JSON array of { src, alt, title, description }

header('Content-Type: application/json; charset=utf-8');

// Basic whitelist base directory (adjust to your site's images root)
$baseRoot = realpath(__DIR__); // site root where this script lives
// optionally set to a specific images directory:
// $baseRoot = realpath(__DIR__ . '/public'); 

$dir = isset($_GET['dir']) ? $_GET['dir'] : '';
// Prevent traversal and require a leading slash or relative safe path:
$dir = preg_replace('#\.\.+#', '', $dir);
$dir = trim($dir);

// Resolve path
$target = realpath($baseRoot . DIRECTORY_SEPARATOR . ltrim($dir, '/\\'));

// security checks
if ($target === false || strpos($target, $baseRoot) !== 0 || !is_dir($target)) {
    http_response_code(400);
    echo json_encode([]);
    exit;
}

// optional captions file: dir/captions.json or dir/index.json
$captions = [];
$captionsFileCandidates = [
    $target . DIRECTORY_SEPARATOR . 'captions.json',
    $target . DIRECTORY_SEPARATOR . 'index.json'
];
foreach ($captionsFileCandidates as $f) {
    if (is_file($f)) {
        $c = json_decode(@file_get_contents($f), true);
        if (is_array($c)) {
            $captions = $c;
            break;
        }
    }
}

// allowed image extensions (lowercase)
$exts = ['jpg','jpeg','png','gif','webp','avif','svg'];

// Collect files
$files = scandir($target);
$out = [];
foreach ($files as $name) {
    if ($name === '.' || $name === '..') continue;
    $path = $target . DIRECTORY_SEPARATOR . $name;
    if (!is_file($path)) continue;
    $info = pathinfo($name);
    $ext = isset($info['extension']) ? strtolower($info['extension']) : '';
    if (!in_array($ext, $exts)) continue;

    // Build public URL path relative to document root.
    // If $dir was given starting with '/', we want to respect that for URLs.
    // We'll construct the URL using the original $dir param.
    // If $dir started with '/', use it; otherwise construct a relative path.
    $dirParam = '/' . ltrim($dir, '/\\');
    $url = $dirParam . '/' . rawurlencode($name);

    // caption lookup (by filename)
    $key = $name;
    $caption = null;
    if (isset($captions[$key])) {
        $caption = $captions[$key];
    } elseif (isset($captions[$info['filename']])) {
        $caption = $captions[$info['filename']];
    }

    $title = $caption['title'] ?? $info['filename'];
    $description = $caption['description'] ?? '';

    $out[] = [
        'src' => $url,
        'alt' => $caption['alt'] ?? $info['filename'],
        'title' => $title,
        'description' => $description
    ];
}

// sort by filename (optional) - you can change to natural sort if you want
usort($out, function($a,$b){ return strcmp($a['src'],$b['src']); });

echo json_encode($out);
