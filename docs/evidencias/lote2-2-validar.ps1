$ErrorActionPreference='Stop'
$root='C:\Projetos\PowerBI\DRE Moderno - Databricks'
$prep=Get-Content (Join-Path $root 'docs\evidencias\lote2-2-atual.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$ev=$prep.Evidence
Add-Type -Path 'C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Tabular.dll'
$relative='DRE Moderno - Databricks.SemanticModel\definition'
$before=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $prep.Backup "snapshot\$relative"))
$after=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $root $relative))
$old=$before.Model.Tables.Find('_Medidas')
$new=$after.Model.Tables.Find('_Medidas')
$catalog=@(Get-Content (Join-Path $ev 'catalogo-novas-medidas.json') -Raw -Encoding UTF8 | ConvertFrom-Json)
if($old.Measures.Count -ne 6 -or $new.Measures.Count -ne 36){throw 'Quantidade de medidas divergente.'}
$all=@($after.Model.Tables|ForEach-Object {$_.Measures})
if($all.Count -ne 36 -or @($all.Name|Select-Object -Unique).Count -ne 36){throw 'Quantidade/nomes duplicados.'}
foreach($m in $old.Measures){
 $n=$new.Measures.Find($m.Name)
 foreach($property in @('Name','Expression','Description','FormatString','DisplayFolder','LineageTag','IsHidden')){
  if($m.$property -cne $n.$property){throw "Medida existente alterada: $($m.Name).$property"}
 }
}
foreach($m in $catalog){
 $n=$new.Measures.Find($m.Nome)
 if(-not $n){throw "Medida ausente: $($m.Nome)"}
 $expected="CALCULATE ( [$($m.Base)], KEEPFILTERS ( 'vw_dre_comparativo'[ordem_dre] = $($m.Posicao) ) )" -replace '\s',''
 if(($n.Expression -replace '\s','') -cne $expected){throw "Expressão divergente: $($m.Nome)"}
 if($n.DisplayFolder -cne $m.Pasta -or $n.LineageTag -cne $m.LineageTag -or -not $n.Description){throw 'Metadados divergentes.'}
 if($n.FormatString -cne 'R$ #,##0.00;(R$ #,##0.00);R$ 0.00'){throw 'Formato monetário divergente.'}
 if($n.Expression -match 'COALESCE|ABS|tipolancamento|REMOVEFILTERS|ALL\('){throw 'Transformação proibida.'}
}
if($before.Model.Tables.Count -ne 15 -or $after.Model.Tables.Count -ne 15 -or $after.Model.Relationships.Count -ne 18){throw 'Estrutura alterada.'}
if($new.Columns.Count -ne 1 -or -not $new.Columns[0].IsHidden -or $new.Partitions.Count -ne 1 -or $new.Partitions[0].Source.Expression -cne $old.Partitions[0].Source.Expression){throw 'Organização/partição alterada.'}
$mPartitions=@($after.Model.Tables | ForEach-Object {$_.Partitions} | Where-Object {$_.Source.GetType().Name -eq 'MPartitionSource'})
if($mPartitions.Count -ne 8){throw 'Partições M divergentes.'}
$result=[ordered]@{Time=(Get-Date -Format o);Parser='TmdlSerializer Microsoft.PowerBI.Tabular';ParserAssembly=[Microsoft.AnalysisServices.Tabular.TmdlSerializer].Assembly.Location;TMDL='APROVADO';Tables=15;Relationships=18;MPartitions=8;BeforeMeasures=6;NewMeasures=30;AfterMeasures=36;ExistingMeasuresUnchanged=$true;NewExpressionsMatchContracts=$true;Metadata=@($all|Select-Object Name,Expression,Description,FormatString,DisplayFolder,LineageTag);DAXCompilation='NAO_EXECUTADA';DynamicTests='PENDENTES';SQL='NAO_EXECUTADO';LotStatus='IMPLEMENTADO_ESTATICAMENTE_NAO_CONCLUIDO'}
$result | ConvertTo-Json -Depth 15 | Set-Content (Join-Path $ev 'validacao-tmdl.json') -Encoding UTF8
[pscustomobject]@{TMDL='APROVADO';Tables=15;Relationships=18;Measures=36;NewMeasures=30;ExistingMeasuresUnchanged=$true;MPartitions=8} | ConvertTo-Json
