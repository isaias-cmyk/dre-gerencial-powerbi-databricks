$ErrorActionPreference='Stop'
$root='C:\Projetos\PowerBI\DRE Moderno - Databricks'
$ev=Join-Path $root 'docs\evidencias\lote2-1-20261102-160536'
Add-Type -Path 'C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Tabular.dll'
$def=Join-Path $root 'DRE Moderno - Databricks.SemanticModel\definition'
$oldDef=Join-Path $root 'backups\lote2-1-20261102-160536\snapshot\DRE Moderno - Databricks.SemanticModel\definition'
$before=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder($oldDef)
$after=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder($def)
$expected=@('DRE | Realizado','DRE | Orçado','DRE | Previsto','DRE | Resultado Líquido Realizado','DRE | Resultado Líquido Orçado','DRE | Resultado Líquido Previsto')
$allMeasures=@($after.Model.Tables | ForEach-Object {$_.Measures})
if($allMeasures.Count -ne 6){throw 'Quantidade de medidas diferente de seis.'}
foreach($name in $expected){if(@($allMeasures | Where-Object Name -eq $name).Count -ne 1){throw "Medida ausente/duplicada: $name"}}
if($before.Model.Tables.Count -ne 14 -or $after.Model.Tables.Count -ne 15){throw 'Inventário de tabelas divergente.'}
if($after.Model.Relationships.Count -ne 18){throw 'Quantidade de relações divergente.'}
$t=$after.Model.Tables.Find('_Medidas')
if($t.IsHidden -or $t.Columns.Count -ne 1 -or -not $t.Columns[0].IsHidden){throw 'Tabela/coluna de organização incorreta.'}
if($t.Partitions.Count -ne 1 -or $t.Partitions[0].Source.GetType().Name -ne 'CalculatedPartitionSource'){throw 'Partição auxiliar não é calculada local.'}
if($t.Partitions[0].Source.Expression -ne 'DATATABLE ( "_Organizacao", INTEGER, { { 0 } } )'){throw 'Fonte auxiliar inesperada.'}
foreach($r in $after.Model.Relationships){if($r.FromTable.Name -eq '_Medidas' -or $r.ToTable.Name -eq '_Medidas'){throw 'Relação indevida na tabela de medidas.'}}
foreach($m in $allMeasures){
 if($m.Expression -match 'COALESCE|tipolancamento|USERELATIONSHIP|CROSSFILTER'){throw "Lógica proibida: $($m.Name)"}
 if($m.Name -like '*Resultado Líquido*'){
  if($m.Description -notmatch 'PROVISÓRIO' -or $m.DisplayFolder -notmatch 'provisório' -or $m.Expression -notmatch 'KEEPFILTERS' -or $m.Expression -notmatch '= 13'){throw 'Contrato provisório/filtro 13 ausente.'}
 }else{
  if($m.Expression -notmatch 'HASONEVALUE' -or $m.Expression -notmatch 'CONTAINSSTRING' -or $m.Expression -notmatch 'BLANK'){throw 'Guarda de contexto/EBIT ausente.'}
 }
}
$sourceCounts=@{Before=0;After=0}
foreach($table in $before.Model.Tables){foreach($p in $table.Partitions){if($p.Source.GetType().Name -eq 'MPartitionSource'){$sourceCounts.Before++}}}
foreach($table in $after.Model.Tables){foreach($p in $table.Partitions){if($p.Source.GetType().Name -eq 'MPartitionSource'){$sourceCounts.After++}}}
if($sourceCounts.Before -ne $sourceCounts.After){throw 'Quantidade de partições M alterada.'}
$result=[ordered]@{
 Date=(Get-Date -Format o);TMDLParser='OK';ParserAssembly=[Microsoft.AnalysisServices.Tabular.TmdlSerializer].Assembly.Location;
 BeforeTables=$before.Model.Tables.Count;AfterTables=$after.Model.Tables.Count;BeforeRelationships=$before.Model.Relationships.Count;AfterRelationships=$after.Model.Relationships.Count;
 MeasureNames=$expected;Measures=6;DuplicateMeasureNames=0;LocalCalculatedTable=$true;HiddenAuxiliaryColumn=$true;MPartitionCounts=$sourceCounts;
 MeasuresMetadata=@($allMeasures|Select-Object Name,Expression,Description,FormatString,DisplayFolder,LineageTag);
 DAXCompilation='Não executada; parser TMDL não compila expressões DAX';DynamicTests='Pendentes no modelo reaberto';LotStatus='Implementado estaticamente; não concluído';NextLot='Não iniciado'
}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ev 'validacao-tmdl.json') -Encoding UTF8
[pscustomobject]@{TMDLParser='OK';Tables=15;Relationships=18;Measures=6;MPartitions=$sourceCounts.After;DynamicTests='Pendentes'} | ConvertTo-Json
