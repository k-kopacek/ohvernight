const {test}=require('node:test'),a=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const D=require('../../explore/trail-seasons.js');
const trail=r=>({properties:{activities:{motorcycling:r}}});
const season=(r,start,end)=>D.season(trail(r),'motorcycling',start,end);
const browse=fs.readFileSync(path.join(__dirname,'../../explore/browse.js'),'utf8');
const NOTE="Ohvernight does not evaluate the managed, accepted or discouraged dates from the source for a trip. Dates the source does not list are unknown. The Motor Vehicle Use Map and current agency orders govern motor vehicle use.";
const FILTER="Trip dates are compared only with restricted dates from the source; other source dates are not evaluated.";
test('no trail outcome derives a within or outside verdict from managed or accepted dates',()=>{
 const records=[{accpt:'12/01-03/14'},{managed:'12/01-03/14'},{managed:'06/01-11/30'},{accpt:'01/01-12/31'},{managed:'05/16-11/30',accpt:'12/01-05/15'},{managed:'check dates'},{accpt:'12/01-03/14',disc:'04/01-11/30'}];
 for(const r of records)for(const [start,end] of [['2026-10-10','2026-10-11'],['2026-12-31','2027-01-02'],['2026-07-04','2026-07-05']]){
  const out=season(r,start,end);a.doesNotMatch(out,/Outside published use dates|Within published use dates/);a.doesNotMatch(out,/\b(outside|within)\b/i);
 }
 for(const file of ['trail-seasons.js','browse.js'])a.doesNotMatch(fs.readFileSync(path.join(__dirname,'../../explore',file),'utf8'),/Outside published use dates|Within published use dates/);
});
test('an accepted range that excludes an October trip is not presented as out of season',()=>{
 a.equal(season({accpt:'12/01-03/14'},'2026-10-10','2026-10-11'),'Source dates not interpreted — see details');
 a.equal(season({accpt:'12/01-03/14'},'2026-10-10','2026-10-11'),season({accpt:'12/01-03/14'},'2026-12-31','2027-01-02'),'trip dates do not change the outcome');
 a.ok(browse.includes(NOTE),'detail states the dates are not evaluated and unlisted dates are unknown');
 a.ok(browse.includes(`accpt:'source field "accepted"'`)&&browse.includes('${v}'),'raw source string is shown under the source field name');
 a.ok(browse.includes(FILTER));
});
test('a restricted range that overlaps the trip keeps the restriction outcome, including year wrapping',()=>{
 a.equal(season({managed:'01/01-12/31',restricted:'09/01-10/01'},'2026-09-27','2026-09-28'),'Published restriction overlaps trip');
 a.equal(season({restricted:'01/01-12/31'},'2026-10-10','2026-10-11'),'Published restriction overlaps trip');
 a.equal(season({accpt:'04/01-11/30',restricted:'12/01-03/14'},'2026-12-31','2027-01-02'),'Published restriction overlaps trip');
 a.equal(season({accpt:'04/01-11/30',restricted:'12/01-03/14'},'2027-03-14','2027-03-14'),'Published restriction overlaps trip');
 a.equal(season({accpt:'04/01-11/30',restricted:'12/01-03/14'},'2027-03-15','2027-03-16'),'Source dates not interpreted — see details');
 a.equal(season({accpt:'01/01-12/31',restricted:'check order'},'2026-09-27','2026-09-28'),'Restriction needs review');
 a.equal(season({},'2026-09-27','2026-09-28'),'Use permission unknown');
 a.equal(season({managed:'01/01-12/31',disc:'01/01-12/31'},'2026-09-27','2026-09-28'),'Published use discouraged — review');
});
test('new trail-date wording makes no positive or seasonal claim',()=>{
 for(const text of [D.NOT_INTERPRETED,NOTE,FILTER,'source field "managed"','source field "accepted"','source field "discouraged"','source field "restricted"'])a.doesNotMatch(text,/\b(allowed|open|legal|permitted|verified|in season)\b/i,text);
});
