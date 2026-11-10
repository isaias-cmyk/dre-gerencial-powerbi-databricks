from pathlib import Path
from datetime import datetime
import hashlib, json, shutil, zipfile

root = Path(__file__).resolve().parents[2]
stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
tag = f'lote2-3-1-investigacao-{stamp}'
files = [p for p in root.rglob('*') if p.is_file() and p.relative_to(root).parts[0] not in ('backups', '.git')]
def sha(p):
    return hashlib.file_digest(p.open('rb'), 'sha256').hexdigest().upper()
baseline = [{'Path':p.relative_to(root).as_posix(),'SHA256':sha(p),'Included':'.pbi' not in p.relative_to(root).parts} for p in files]
backup = root/'backups'/tag
ev = root/'docs/evidencias'/tag
snapshot = backup/'snapshot'
snapshot.mkdir(parents=True)
ev.mkdir(parents=True)
for row in baseline:
    if row['Included']:
        dest = snapshot/row['Path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(root/row['Path'],dest)
archive = backup/'snapshot.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for row in baseline:
        if row['Included']: z.write(snapshot/row['Path'],row['Path'])
restore=backup/'restauracao-teste'
with zipfile.ZipFile(archive) as z: z.extractall(restore)
for row in baseline:
    if row['Included']:
        assert sha(snapshot/row['Path']) == row['SHA256'] == sha(restore/row['Path'])
old=json.loads((root/'docs/evidencias/lote2-1-encerramento-20261102-162739/baseline.json').read_text(encoding='utf-8-sig'))
differences=[{'Path':r['Path'],'Before':r['Hash'],'Now':sha(Path(r['Path']))} for r in old if Path(r['Path']).exists() and sha(Path(r['Path']))!=r['Hash']]
result={'Tag':tag,'Backup':str(backup),'Evidence':str(ev),'Included':sum(r['Included'] for r in baseline),'Excluded':[r['Path'] for r in baseline if not r['Included']], 'ZIP_SHA256':sha(archive),'RestoreVerified':True,'Git':'Fora de repositório; status/rev-parse código 128','Desktop':'Aberto; snapshot apenas de leitura dos arquivos serializados, sem edição de produção; exigir novo fechamento e backup antes de edição futura','PreexistingDifferences':differences}
for path,data in [(ev/'preparacao.json',result),(ev/'baseline.json',baseline),(backup/'manifesto-sha256.json',baseline)]:
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'docs/evidencias/lote2-3-1-atual.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
