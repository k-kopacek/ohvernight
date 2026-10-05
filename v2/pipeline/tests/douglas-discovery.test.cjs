const {test}=require('node:test'),a=require('node:assert/strict'),D=require('../../explore/trail-seasons.js');
const trail=r=>({properties:{activities:{motorcycling:r}}});
test('published seasons check every trip day including year wrapping; restrictions win',()=>{
 a.match(D.season(trail({accpt:'12/01-03/14'}),'motorcycling','2026-09-27','2026-09-28'),/Outside/);
 a.match(D.season(trail({accpt:'12/01-03/14'}),'motorcycling','2026-12-31','2027-01-02'),/Within/);
 a.match(D.season(trail({managed:'01/01-12/31',restricted:'09/01-10/01'}),'motorcycling','2026-09-27','2026-09-28'),/restriction/);
 a.match(D.season(trail({accpt:'01/01-12/31',restricted:'check order'}),'motorcycling','2026-09-27','2026-09-28'),/review/);
 a.equal(D.days('2026-02-30','2026-03-01'),null);a.equal(D.windows('13/01-12/31'),null);
 a.match(D.season(trail({}),'motorcycling','2026-09-27','2026-09-28'),/unknown/);
});
test('camping excludes trailheads and horse camps; GPX escapes text and preserves segments',()=>{
 a.equal(D.camping(['CAMPGROUND','HORSE CAMP','TRAILHEAD'].map(site_type=>({properties:{site_type}}))).length,1);
 const x=D.gpx({properties:{name:'A & <B>'},geometry:{type:'MultiLineString',coordinates:[[[1,2],[2,3]],[[3,4],[4,5]]]}});
 a.match(x,/A &amp; &lt;B&gt;/);a.equal((x.match(/<trkseg>/g)||[]).length,2);
});
