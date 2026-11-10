param([string[]]$Only, [string]$Account)
$ErrorActionPreference='Stop'
$root='C:\Projetos\PowerBI\DRE Moderno - Databricks'
$scripts=Join-Path $root 'docs\testes\lote2-2'
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
$out=Join-Path $root "docs\evidencias\lote2-2-execucao-$stamp"
New-Item -ItemType Directory -Path $out | Out-Null
$before=@(Get-ChildItem -LiteralPath $root -File -Force -Recurse | Where-Object { $_.FullName.Substring($root.Length+1) -notmatch '^(docs|backups|\.git)\\' } | ForEach-Object {[pscustomobject]@{Path=$_.FullName;Hash=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}})
$before | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $out 'baseline.json') -Encoding UTF8
Add-Type -Path 'C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll'
$portFile=Get-ChildItem -LiteralPath 'C:\Users\<usuario>\AppData\Local\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces' -Filter msmdsrv.port.txt -Recurse -Force | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$port=(Get-Content -LiteralPath $portFile.FullName -Raw -Encoding Unicode).Trim()
if ($port -notmatch '^\d+$') {throw 'Porta local inválida.'}
$conn=[Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$port;Connect Timeout=10")
$status=@()
try {
 $conn.Open()
 $catalogs=@($conn.GetSchemaDataSet('DBSCHEMA_CATALOGS',$null).Tables[0] | Select-Object -ExpandProperty CATALOG_NAME)
 if($catalogs.Count -ne 1){throw 'Mais de um catálogo: seleção explícita necessária.'}
 $conn.ChangeDatabase($catalogs[0])
 $guard=$conn.CreateCommand();$guard.CommandText='SELECT * FROM $SYSTEM.TMSCHEMA_TABLES';$reader=$guard.ExecuteReader();$names=@();while($reader.Read()){$names+=$reader['Name']};$reader.Close()
 foreach($expected in @('dim_filial','dim_conta','dim_dre','dim_calendario','fato_lancamentos','fato_orcamento','fato_previsao','vw_dre_comparativo')){if($expected -notin $names){throw "Modelo não corresponde ao projeto: $expected ausente"}}
 [ordered]@{Time=(Get-Date -Format o);Port=$port;Catalog=$catalogs[0];Tables=$names;Connection='ADOMD local somente leitura';QuerySource=$scripts} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $out 'sessao.json') -Encoding UTF8
 $files=@(Get-ChildItem -LiteralPath $scripts -Filter '*.dax' | Sort-Object Name)
 if($Only){$files=@($files | Where-Object {$_.Name -in $Only})}
 foreach($file in $files){
  $query=Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
  if($Account){$query=$query.Replace('__ID_CONTA_ANALITICA__',$Account.Replace('"','""'))}
  if($query.Contains('__ID_CONTA_ANALITICA__')){ $status+=[pscustomobject]@{File=$file.Name;State='NAO_EXECUTADO';Reason='Conta analítica ainda não selecionada'};continue }
  $start=Get-Date
  try {
   $cmd=$conn.CreateCommand();$cmd.CommandTimeout=120;$cmd.CommandText=$query
   $reader=$cmd.ExecuteReader();$rows=[Collections.Generic.List[object]]::new()
   while($reader.Read()){
    $row=[ordered]@{}
    for($i=0;$i -lt $reader.FieldCount;$i++){ $value=$reader.GetValue($i);if($value -is [DBNull]){$value=$null};$row[$reader.GetName($i)]=$value }
    $rows.Add([pscustomobject]$row)
   }
   $reader.Close()
   ConvertTo-Json -InputObject @($rows.ToArray()) -Depth 20 | Set-Content (Join-Path $out ($file.BaseName+'.json')) -Encoding UTF8
   if($rows.Count){$rows.ToArray() | Export-Csv -LiteralPath (Join-Path $out ($file.BaseName+'.csv')) -NoTypeInformation -Encoding UTF8}
   $status+=[pscustomobject]@{File=$file.Name;State='EXECUTADO';Rows=$rows.Count;Seconds=((Get-Date)-$start).TotalSeconds;Account=$Account;QuerySHA256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash}
  }catch{
   $err=$_.Exception.ToString();$err | Set-Content (Join-Path $out ($file.BaseName+'.erro.txt')) -Encoding UTF8
   $status+=[pscustomobject]@{File=$file.Name;State='ERRO';Error=$err}
   if($reader -and -not $reader.IsClosed){$reader.Close()}
  }
 }
} finally { $conn.Dispose() }
$status | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $out 'execucao.json') -Encoding UTF8
$after=@($before | ForEach-Object {[pscustomobject]@{Path=$_.Path;Before=$_.Hash;After=(Get-FileHash -LiteralPath $_.Path -Algorithm SHA256).Hash;Unchanged=((Get-FileHash -LiteralPath $_.Path -Algorithm SHA256).Hash -eq $_.Hash)}})
$after | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $out 'integridade.json') -Encoding UTF8
[pscustomobject]@{Output=$out;Status=$status;ChangedFiles=@($after|Where-Object {-not $_.Unchanged}|Select-Object -ExpandProperty Path)} | ConvertTo-Json -Depth 12


