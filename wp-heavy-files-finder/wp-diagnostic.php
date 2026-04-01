<?php
// ============================================================
//  WP HEAVY FILES FINDER v3
//  1. Uploader à la racine WordPress via FTP
//  2. Ouvrir : https://tonsite.com/wp-diagnostic.php
//  3. SUPPRIMER après utilisation !
// ============================================================

@ini_set('memory_limit', '256M');
@set_time_limit(120);
error_reporting(0);

// ── MOT DE PASSE ─────────────────────────────────────────
define('PASSWORD', 'ChangeMe123!'); // ← CHANGE ICI

session_start();
if (isset($_POST['p']) && $_POST['p'] === PASSWORD) {
    $_SESSION['ok'] = true;
}
if (empty($_SESSION['ok'])) {
    $err = isset($_POST['p']) ? 'Mot de passe incorrect.' : '';
    echo '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Diagnostic</title>
    <style>body{background:#111;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:sans-serif;}
    .b{background:#1e1e1e;border:1px solid #333;border-radius:10px;padding:2rem;min-width:300px;color:#eee;}
    h2{margin:0 0 1rem;color:#60a5fa;}input{width:100%;padding:.5rem;background:#111;border:1px solid #444;color:#fff;border-radius:6px;box-sizing:border-box;}
    button{width:100%;margin-top:.8rem;padding:.6rem;background:#2563eb;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:1rem;}
    .e{color:#f87171;margin-top:.5rem;font-size:.85rem;}</style></head><body>
    <div class="b"><h2>🔍 WP Diagnostic</h2>
    <form method="POST"><input type="password" name="p" placeholder="Mot de passe" autofocus>
    <button>Accéder</button></form>' . ($err ? '<p class="e">'.$err.'</p>' : '') . '</div></body></html>';
    exit;
}

// ── FONCTIONS DE BASE ────────────────────────────────────

function human($b) {
    if ($b >= 1073741824) {
        return round($b / 1073741824, 2) . ' GB';
    }
    if ($b >= 1048576) {
        return round($b / 1048576, 2) . ' MB';
    }
    if ($b >= 1024) {
        return round($b / 1024, 2) . ' KB';
    }
    return $b . ' B';
}

// Collecte récursive de tous les fichiers (opendir natif, plus stable)
function collect_files($dir, &$results, $min_bytes) {
    $dh = @opendir($dir);
    if (!$dh) {
        return;
    }
    while (($entry = readdir($dh)) !== false) {
        if ($entry === '.' || $entry === '..') {
            continue;
        }
        $path = $dir . DIRECTORY_SEPARATOR . $entry;
        if (is_link($path)) {
            continue;
        }
        if (is_dir($path)) {
            collect_files($path, $results, $min_bytes);
        } elseif (is_file($path)) {
            $size = @filesize($path);
            if ($size !== false && $size >= $min_bytes) {
                $results[] = array('path' => $path, 'size' => $size, 'mtime' => @filemtime($path));
            }
        }
    }
    closedir($dh);
}

// Taille d'un dossier (récursif)
function dir_size($dir) {
    $size = 0;
    $dh = @opendir($dir);
    if (!$dh) {
        return 0;
    }
    while (($entry = readdir($dh)) !== false) {
        if ($entry === '.' || $entry === '..') {
            continue;
        }
        $path = $dir . DIRECTORY_SEPARATOR . $entry;
        if (is_link($path)) {
            continue;
        }
        if (is_dir($path)) {
            $size += dir_size($path);
        } elseif (is_file($path)) {
            $size += (int) @filesize($path);
        }
    }
    closedir($dh);
    return $size;
}

// Liste des sous-dossiers immédiats avec leur taille
function immediate_dirs($dir) {
    $list = array();
    $dh = @opendir($dir);
    if (!$dh) {
        return $list;
    }
    while (($entry = readdir($dh)) !== false) {
        if ($entry === '.' || $entry === '..') {
            continue;
        }
        $path = $dir . DIRECTORY_SEPARATOR . $entry;
        if (is_dir($path) && !is_link($path)) {
            $list[] = array('name' => $entry, 'path' => $path, 'size' => dir_size($path));
        }
    }
    closedir($dh);
    usort($list, function ($a, $b) {
        return $b['size'] - $a['size'];
    });
    return $list;
}

// ── PARAMÈTRES ───────────────────────────────────────────

$root     = __DIR__;
$min_mb   = isset($_GET['min']) ? max(0, (float) $_GET['min']) : 1.0;
$top_n    = isset($_GET['top']) ? max(5, (int) $_GET['top']) : 50;
$scan_dir = isset($_GET['dir']) ? $_GET['dir'] : $root;

// Sécurité : interdire de sortir de la racine
$scan_dir = realpath($scan_dir);
if (!$scan_dir || strpos($scan_dir, $root) !== 0) {
    $scan_dir = $root;
}

$min_bytes = (int) ($min_mb * 1048576);
$rel       = str_replace($root, '', $scan_dir) ?: '/';

// ── SCAN ─────────────────────────────────────────────────

$files = array();
collect_files($scan_dir, $files, $min_bytes);
usort($files, function ($a, $b) {
    return $b['size'] - $a['size'];
});

$top    = array_slice($files, 0, $top_n);
$dirs   = immediate_dirs($scan_dir);
$total  = 0;
foreach ($files as $f) {
    $total += $f['size'];
}
$max_sz = !empty($top) ? $top[0]['size'] : 1;

// ── HTML ─────────────────────────────────────────────────
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WP Diagnostic — <?php echo htmlspecialchars($rel); ?></title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:'Segoe UI',system-ui,sans-serif;font-size:.9rem}
a{color:#60a5fa;text-decoration:none}a:hover{text-decoration:underline}
.hd{background:#1e293b;border-bottom:1px solid #334155;padding:.9rem 1.5rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.hd h1{font-size:1.2rem}
.badge{background:#0f172a;border:1px solid #334155;border-radius:20px;padding:.15rem .7rem;font-size:.78rem;color:#94a3b8}
.badge b{color:#e2e8f0}
.warn{color:#f87171;font-size:.78rem;margin-left:auto}
.main{padding:1.2rem;max-width:1300px;margin:0 auto}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.8rem;margin-bottom:1.2rem}
.stat{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:1rem;text-align:center}
.stat .v{font-size:1.6rem;font-weight:700;color:#60a5fa}
.stat .l{color:#94a3b8;font-size:.78rem;margin-top:.2rem}
.bar-wrap{background:#0f172a;border-radius:4px;height:7px;width:120px;display:inline-block;vertical-align:middle}
.bar-fill{height:7px;border-radius:4px}
form.filters{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:.8rem 1rem;margin-bottom:1.2rem;display:flex;gap:.8rem;flex-wrap:wrap;align-items:center}
form.filters label{color:#94a3b8;font-size:.83rem}
form.filters input[type=number]{background:#0f172a;border:1px solid #475569;border-radius:5px;color:#fff;padding:.3rem .5rem;width:70px;font-size:.83rem}
form.filters button{background:#2563eb;color:#fff;border:none;border-radius:5px;padding:.35rem .9rem;cursor:pointer;font-weight:600}
.section{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:1rem 1.2rem;margin-bottom:1.2rem}
.section h2{color:#60a5fa;font-size:1rem;margin-bottom:.8rem}
table{width:100%;border-collapse:collapse}
th{text-align:left;padding:.4rem .6rem;color:#64748b;font-size:.75rem;text-transform:uppercase;border-bottom:1px solid #334155}
td{padding:.45rem .6rem;border-bottom:1px solid #1e293b;vertical-align:middle}
tr:hover td{background:#ffffff08}
.path{color:#94a3b8;font-size:.78rem;word-break:break-all}
.sz{font-weight:700;font-size:.85rem;white-space:nowrap}
.ext{background:#0f172a;border:1px solid #334155;border-radius:3px;padding:.05rem .35rem;font-size:.73rem;font-family:monospace}
.alrt{background:#450a0a;border:1px solid #7f1d1d;border-radius:6px;padding:.7rem 1rem;color:#fca5a5;margin-bottom:1rem;font-size:.82rem}
</style>
</head>
<body>

<div class="hd">
  <span style="font-size:1.4rem">🔍</span>
  <h1>WP Heavy Files</h1>
  <span class="badge">Dossier : <b><?php echo htmlspecialchars($rel); ?></b></span>
  <span class="badge">Fichiers ≥ <?php echo $min_mb; ?> MB : <b><?php echo count($files); ?></b></span>
  <span class="badge">Total : <b><?php echo human($total); ?></b></span>
  <span class="warn">⚠️ Supprimer ce fichier après utilisation !</span>
</div>

<div class="main">

  <div class="alrt">⚠️ <b>Sécurité :</b> ce script expose la structure de votre serveur. Supprimez-le via FTP dès que vous avez terminé.</div>

  <div class="stats">
    <div class="stat"><div class="v"><?php echo count($files); ?></div><div class="l">Fichiers ≥ <?php echo $min_mb; ?> MB</div></div>
    <div class="stat"><div class="v"><?php echo human($total); ?></div><div class="l">Poids cumulé</div></div>
    <div class="stat"><div class="v"><?php echo !empty($top) ? human($top[0]['size']) : '—'; ?></div><div class="l">Fichier le + lourd</div></div>
    <div class="stat"><div class="v"><?php echo count($dirs); ?></div><div class="l">Sous-dossiers</div></div>
  </div>

  <form class="filters" method="GET">
    <label>Taille min (MB) :
      <input type="number" name="min" step="0.1" min="0" value="<?php echo $min_mb; ?>">
    </label>
    <label>Afficher top :
      <input type="number" name="top" min="5" max="500" value="<?php echo $top_n; ?>">
    </label>
    <input type="hidden" name="dir" value="<?php echo htmlspecialchars($scan_dir); ?>">
    <button type="submit">🔎 Appliquer</button>
    <a href="?" style="color:#94a3b8;font-size:.83rem">Réinitialiser</a>
  </form>

  <div class="section">
    <h2>📁 Poids des dossiers dans <?php echo htmlspecialchars($rel); ?></h2>
    <?php if (empty($dirs)): ?>
      <p style="color:#64748b">Aucun sous-dossier.</p>
    <?php else:
      $max_dir = $dirs[0]['size'];
    ?>
    <table>
      <thead><tr><th>Dossier</th><th>Taille</th><th style="width:160px">Relatif</th><th></th></tr></thead>
      <tbody>
      <?php foreach ($dirs as $d):
        $pct = $max_dir > 0 ? min(100, round($d['size'] / $max_dir * 100)) : 0;
        $col = $pct > 70 ? '#f87171' : ($pct > 35 ? '#fb923c' : '#34d399');
      ?>
      <tr>
        <td>📁 <?php echo htmlspecialchars($d['name']); ?></td>
        <td><span class="sz" style="color:<?php echo $col; ?>"><?php echo human($d['size']); ?></span></td>
        <td><span class="bar-wrap"><span class="bar-fill" style="width:<?php echo $pct; ?>%;background:<?php echo $col; ?>"></span></span></td>
        <td>
          <a href="?dir=<?php echo urlencode($d['path']); ?>&min=<?php echo $min_mb; ?>&top=<?php echo $top_n; ?>">Explorer →</a>
        </td>
      </tr>
      <?php endforeach; ?>
      </tbody>
    </table>
    <?php if ($scan_dir !== $root): ?>
    <p style="margin-top:.8rem">
      <a href="?dir=<?php echo urlencode(dirname($scan_dir)); ?>&min=<?php echo $min_mb; ?>&top=<?php echo $top_n; ?>">← Remonter</a>
      &nbsp;|&nbsp;
      <a href="?min=<?php echo $min_mb; ?>&top=<?php echo $top_n; ?>">← Racine</a>
    </p>
    <?php endif; ?>
    <?php endif; ?>
  </div>

  <div class="section">
    <h2>📄 Top <?php echo $top_n; ?> fichiers les plus lourds</h2>
    <?php if (empty($top)): ?>
      <p style="color:#64748b">Aucun fichier trouvé avec ces filtres. Essayez de baisser la taille minimum.</p>
    <?php else: ?>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Nom du fichier</th>
          <th>Chemin</th>
          <th>Ext.</th>
          <th>Taille</th>
          <th>Modifié</th>
          <th style="width:130px">Poids relatif</th>
        </tr>
      </thead>
      <tbody>
      <?php foreach ($top as $i => $f):
        $rel_path = str_replace($root, '', $f['path']);
        $ext      = strtolower(pathinfo($f['path'], PATHINFO_EXTENSION));
        $pct      = $max_sz > 0 ? min(100, round($f['size'] / $max_sz * 100)) : 0;
        $col      = $f['size'] >= 10485760 ? '#f87171' : ($f['size'] >= 2097152 ? '#fb923c' : '#34d399');
        $col_bar  = $pct > 70 ? '#f87171' : ($pct > 35 ? '#fb923c' : '#34d399');
      ?>
      <tr>
        <td style="color:#64748b"><?php echo $i + 1; ?></td>
        <td style="font-weight:600"><?php echo htmlspecialchars(basename($f['path'])); ?></td>
        <td class="path"><?php echo htmlspecialchars(dirname($rel_path)); ?></td>
        <td><?php echo $ext ? '<span class="ext">' . htmlspecialchars($ext) . '</span>' : '—'; ?></td>
        <td><span class="sz" style="color:<?php echo $col; ?>"><?php echo human($f['size']); ?></span></td>
        <td style="color:#64748b;font-size:.78rem;white-space:nowrap"><?php echo $f['mtime'] ? date('d/m/Y H:i', $f['mtime']) : '—'; ?></td>
        <td>
          <span class="bar-wrap">
            <span class="bar-fill" style="width:<?php echo $pct; ?>%;background:<?php echo $col_bar; ?>"></span>
          </span>
          <span style="color:#64748b;font-size:.75rem;margin-left:.3rem"><?php echo $pct; ?>%</span>
        </td>
      </tr>
      <?php endforeach; ?>
      </tbody>
    </table>
    <?php endif; ?>
  </div>

</div>
</body>
</html>
