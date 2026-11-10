param([string]$ProjectRoot = 'C:\Projetos\PowerBI\DRE Moderno - Databricks')
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$stamp = [DateTimeOffset]::Now.ToString('yyyyMMdd-HHmmss')
$evidence = Join-Path $root "docs\evidencias\fase0-$stamp"
$backup = Join-Path $root "backups\fase0-$stamp"
if ((Test-Path -LiteralPath $evidence) -or (Test-Path -LiteralPath $backup)) { throw 'Destino já existe.' }
$desktop = @(Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue)
if ($desktop.Count -gt 0) { throw 'Power BI Desktop aberto. Snapshot interrompido.' }
# Inventário dos arquivos preexistentes; artefatos gerados ficam fora do snapshot.
$files = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force | Where-Object {
    $rel = $_.FullName.Substring($root.Length + 1)
    $rel -notmatch '^(docs|backups|\.git)\\'
} | Sort-Object FullName)
$inventory = @($files | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length + 1)
    [pscustomobject]@{ Path=$rel; Bytes=$_.Length; LastWriteTimeUtc=$_.LastWriteTimeUtc.ToString('o'); SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash; BackupIncluded=($rel -notmatch '(^|\\)\.pbi\\') }
})
New-Item -ItemType Directory -Path $evidence, $backup | Out-Null
function Write-Json($value, $path) { ConvertTo-Json -InputObject $value -Depth 40 | Set-Content -LiteralPath $path -Encoding UTF8 }
Write-Json $inventory (Join-Path $evidence 'inventario-arquivos.json')
$inventory | Export-Csv -LiteralPath (Join-Path $evidence 'inventario-arquivos.csv') -NoTypeInformation -Encoding UTF8
Write-Json @($inventory | Where-Object { -not $_.BackupIncluded }) (Join-Path $evidence 'exclusoes-backup.json')
$gitVersion = & git --version 2>&1
$gitVersionCode = $LASTEXITCODE
$gitTop = & git -C $root rev-parse --show-toplevel 2>&1
$gitTopCode = $LASTEXITCODE
$gitStatus = & git -C $root status --short 2>&1
$gitStatusCode = $LASTEXITCODE
Write-Json ([ordered]@{ Date=[DateTimeOffset]::Now.ToString('o'); Version="$gitVersion"; VersionExit=$gitVersionCode; TopLevel="$gitTop"; TopLevelExit=$gitTopCode; Status="$gitStatus"; StatusExit=$gitStatusCode; Initialized=$false; Gitignore=(Get-Content -LiteralPath (Join-Path $root '.gitignore') -Raw) }) (Join-Path $evidence 'git.json')
Write-Json ([ordered]@{ Date=[DateTimeOffset]::Now.ToString('o'); PBIDesktopCount=$desktop.Count; Check='Get-Process -Name PBIDesktop'; Scope='Processos visíveis nesta sessão; sem abertura visual do Desktop.' }) (Join-Path $evidence 'ambiente.json')
$jsonResults = @()
foreach ($item in $inventory | Where-Object { $_.BackupIncluded -and ([IO.Path]::GetExtension($_.Path) -in @('.json','.pbip','.pbir','.pbism','.platform')) }) {
    $obj = Get-Content -LiteralPath (Join-Path $root $item.Path) -Raw -Encoding UTF8 | ConvertFrom-Json
    $jsonResults += [pscustomobject]@{Path=$item.Path; Syntax='OK'; Schema=$obj.'$schema'; Version=$obj.version; Validation='Somente parsing JSON; schema não validado'}
}
Write-Json $jsonResults (Join-Path $evidence 'json-sintaxe.json')
$tables = @()
$connections = @()
$measures = @()
$tablesPath = Join-Path $root 'DRE Moderno - Databricks.SemanticModel\definition\tables'
foreach ($file in Get-ChildItem -LiteralPath $tablesPath -Filter '*.tmdl' | Sort-Object Name) {
    $raw = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    $name = [regex]::Match($raw,'(?m)^table (.+)\r?$').Groups[1].Value.Trim()
    $columns = @([regex]::Matches($raw,'(?m)^\tcolumn (.+)\r?$') | ForEach-Object { $_.Groups[1].Value.Trim() })
    $types = @([regex]::Matches($raw,'(?m)^\t\tdataType: (.+)\r?$') | ForEach-Object { $_.Groups[1].Value.Trim() })
    $tables += [pscustomobject]@{Name=$name; Path=$file.FullName.Substring($root.Length+1); Technical=($name -match '^(LocalDateTable_|DateTableTemplate_)'); Columns=$columns; DataTypesInColumnOrder=$types; LineageTags=@([regex]::Matches($raw,'(?m)^\s*lineageTag: (.+)\r?$') | ForEach-Object {$_.Groups[1].Value.Trim()}); Partitions=@([regex]::Matches($raw,'(?m)^\tpartition (.+)\r?$') | ForEach-Object {$_.Groups[1].Value.Trim()}); Modes=@([regex]::Matches($raw,'(?m)^\s*mode: (.+)\r?$') | ForEach-Object {$_.Groups[1].Value.Trim()})}
    foreach ($m in [regex]::Matches($raw,'(?m)^\tmeasure (.+)\r?$')) { $measures += [pscustomobject]@{Table=$name; Declaration=$m.Groups[1].Value.Trim()} }
    $conn = [regex]::Match($raw,'DatabricksMultiCloud\.Catalogs\("([^"]+)",\s*"([^"]+)"')
    if ($conn.Success) {
        $connections += [pscustomobject]@{Table=$name; Connector='DatabricksMultiCloud.Catalogs'; Host=$conn.Groups[1].Value; HttpPath=$conn.Groups[2].Value; Navigation=@([regex]::Matches($raw,'\[Name="([^"]+)",Kind="([^"]+)"\]') | ForEach-Object {[pscustomobject]@{Name=$_.Groups[1].Value;Kind=$_.Groups[2].Value}}); Connectivity='Não testada; inspeção estática'}
    }
}
Write-Json $tables (Join-Path $evidence 'tabelas.json')
Write-Json $connections (Join-Path $evidence 'conexoes.json')
Write-Json $measures (Join-Path $evidence 'medidas.json')
$relText = Get-Content -LiteralPath (Join-Path $root 'DRE Moderno - Databricks.SemanticModel\definition\relationships.tmdl') -Raw
$relationships = @([regex]::Matches($relText,'(?ms)^relationship (\S+)\r?\n(.*?)(?=^relationship |\z)') | ForEach-Object {
    $body = $_.Groups[2].Value
    [pscustomobject]@{ID=$_.Groups[1].Value; From=[regex]::Match($body,'fromColumn: (.+)').Groups[1].Value.Trim(); To=[regex]::Match($body,'toColumn: (.+)').Groups[1].Value.Trim(); ActiveDeclaration=$(if($body -match 'isActive: false'){'false explícito'}else{'Omitida; ativo padrão a confirmar no mecanismo'}); Technical=($body -match 'LocalDateTable_'); Properties=$body.Trim(); EffectiveCardinalityAndDirection='Não verificadas; Fase 1'}
})
Write-Json $relationships (Join-Path $evidence 'relacionamentos.json')
$pages = @(Get-ChildItem -LiteralPath (Join-Path $root 'DRE Moderno - Databricks.Report\definition\pages') -Filter page.json -Recurse | ForEach-Object {
    $page = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
    [pscustomobject]@{Path=$_.FullName.Substring($root.Length+1); ID=$page.name; DisplayName=$page.displayName; Width=$page.width;Height=$page.height;Schema=$page.'$schema'}
})
$visuals = @(Get-ChildItem -LiteralPath (Join-Path $root 'DRE Moderno - Databricks.Report\definition\pages') -Filter visual.json -Recurse | ForEach-Object {
    $v = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
    [pscustomobject]@{Path=$_.FullName.Substring($root.Length+1); ID=$v.name; Type=$v.visual.visualType; Schema=$v.'$schema'; Query=$v.visual.query; Filters=$v.filterConfig}
})
Write-Json $pages (Join-Path $evidence 'paginas.json')
Write-Json $visuals (Join-Path $evidence 'visuais.json')
$report = Get-Content -LiteralPath (Join-Path $root 'DRE Moderno - Databricks.Report\definition\report.json') -Raw | ConvertFrom-Json
Write-Json ([ordered]@{Themes=$report.themeCollection;Resources=$report.resourcePackages}) (Join-Path $evidence 'temas.json')
$payload = Join-Path $backup 'snapshot'
New-Item -ItemType Directory -Path $payload | Out-Null
$manifest = @($inventory | Where-Object BackupIncluded)
foreach ($item in $manifest) {
    $destination = Join-Path $payload $item.Path
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $root $item.Path) -Destination $destination
    if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $item.SHA256) { throw "Falha na cópia: $($item.Path)" }
}
Write-Json $manifest (Join-Path $backup 'manifesto-sha256.json')
$archive = Join-Path $backup 'snapshot.zip'
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory($payload, $archive)
$restore = Join-Path $backup 'restauracao-teste'
[IO.Compression.ZipFile]::ExtractToDirectory($archive, $restore)
$checks = @($manifest | ForEach-Object {
    $originalHash = (Get-FileHash -LiteralPath (Join-Path $root $_.Path) -Algorithm SHA256).Hash
    $restoredHash = (Get-FileHash -LiteralPath (Join-Path $restore $_.Path) -Algorithm SHA256).Hash
    [pscustomobject]@{Path=$_.Path;Expected=$_.SHA256;OriginalAfter=$originalHash;Restored=$restoredHash;Match=($_.SHA256 -eq $originalHash -and $_.SHA256 -eq $restoredHash)}
})
if (@($checks | Where-Object { -not $_.Match }).Count) { throw 'Hashes divergentes na restauração/original.' }
if (@(Get-ChildItem -LiteralPath $restore -Recurse -File -Force).Count -ne $manifest.Count) { throw 'Quantidade de arquivos restaurados divergente.' }
$unchanged = @($inventory | ForEach-Object { [pscustomobject]@{Path=$_.Path;Match=((Get-FileHash -LiteralPath (Join-Path $root $_.Path) -Algorithm SHA256).Hash -eq $_.SHA256)} })
if (@($unchanged | Where-Object { -not $_.Match }).Count) { throw 'Arquivo preexistente alterado durante snapshot.' }
Write-Json $checks (Join-Path $evidence 'restauracao-hashes.json')
Write-Json $unchanged (Join-Path $evidence 'integridade-original-antes-documentacao.json')
# Verificação de referências de entrada também na cópia restaurada.
$restoredPbip = Get-Content -LiteralPath (Join-Path $restore 'DRE Moderno - Databricks.pbip') -Raw | ConvertFrom-Json
$restoredReport = Join-Path $restore $restoredPbip.artifacts[0].report.path
$restoredPbir = Get-Content -LiteralPath (Join-Path $restoredReport 'definition.pbir') -Raw | ConvertFrom-Json
$restoredModel = [IO.Path]::GetFullPath((Join-Path $restoredReport $restoredPbir.datasetReference.byPath.path))
if (-not (Test-Path -LiteralPath (Join-Path $restoredModel 'definition.pbism'))) { throw 'Referência relativa quebrada no backup.' }
$result = [ordered]@{Timestamp=[DateTimeOffset]::Now.ToString('o');ProjectRoot=$root;Evidence=$evidence;Backup=$backup;Archive=$archive;ArchiveSHA256=(Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash;OriginalFileCount=$inventory.Count;BackupFileCount=$manifest.Count;ExcludedFileCount=($inventory.Count-$manifest.Count);RestoredFileCount=$checks.Count;RestoreHashes='OK';OriginalUnchanged='OK antes de atualizar documentação';RestoredEntryReferences='OK PBIP -> Report -> SemanticModel';JsonSyntaxCount=$jsonResults.Count;TableCount=$tables.Count;BusinessTableCount=@($tables | Where-Object {-not $_.Technical}).Count;RelationshipCount=$relationships.Count;MeasureCount=$measures.Count;PageCount=$pages.Count;VisualCount=$visuals.Count;DesktopOpening='Não executada';Phase1='Não iniciada'}
Write-Json $result (Join-Path $evidence 'resultado.json')
$result | ConvertTo-Json -Depth 5
