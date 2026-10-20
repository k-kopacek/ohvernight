// DRAFT checker for docs/design/protected-tokens.json. NOT in CI and not imported by any test.
// Read-only: confirms every protected value is still present, byte-for-byte, in its file.
//
//   node docs/design/check-protected-tokens.mjs
//
// Exit 1 lists each value that is missing. The proposal recommends that Codex
// moves this into v2/pipeline/tests/ as a CI test only after owner approval.
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=resolve(fileURLToPath(new URL('../..',import.meta.url)));
const list=JSON.parse(await readFile(resolve(root,'docs/design/protected-tokens.json'),'utf8'));
const files=new Map(),missing=[];
for(const entry of list.entries){
  if(!files.has(entry.file))files.set(entry.file,await readFile(resolve(root,entry.file),'utf8'));
  if(!files.get(entry.file).includes(entry.value))missing.push(entry);
}
const fixture=JSON.parse(await readFile(resolve(root,'v2/pipeline/tests/fixtures/legacy-negated-wording.json'),'utf8'));
console.log(JSON.stringify({base:list.base,entries:list.entries.length,files:files.size,missing:missing.length,
  byReference:{legacyNegatedWordingStrings:fixture.strings.length}},null,1));
for(const entry of missing)console.error(`MISSING ${entry.file} [${entry.ref}] ${JSON.stringify(entry.value)}`);
if(missing.length)process.exitCode=1;
