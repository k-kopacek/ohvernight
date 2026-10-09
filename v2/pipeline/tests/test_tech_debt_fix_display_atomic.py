import hashlib, os, stat, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
import build_display
class StagedDisplayPublicationTest(unittest.TestCase):
 def setup_fixture(self,root):
  output=root/"regions/fixture/display"; output.mkdir(parents=True); (output/"first.geojson").write_bytes(b"old-first"); (output/"coverage.geojson").write_bytes(b"old-coverage"); (output/"unknown.txt").write_bytes(b"old-unknown"); return output
 def patches(self,root):
  manifest={"layers":[{"id":"first","format":"feature_collection","kind":"land","status_ref":None}]}
  first=({"type":"FeatureCollection","features":[]},{"path":"regions/fixture/display/first.geojson","layer_id":"first","feature_count":0})
  coverage=({"type":"FeatureCollection","features":[]},{"path":"regions/fixture/display/coverage.geojson","layer_id":"coverage","feature_count":0})
  return (patch.object(build_display,"_read_json",return_value=manifest),patch.object(build_display,"build_layer",return_value=first),patch.object(build_display,"build_coverage",return_value=coverage))
 def test_failure_preserves_old_directory_and_cleans_stage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); output=self.setup_fixture(root); before={p.name:p.read_bytes() for p in output.iterdir()}; writes=0; orig=Path.write_bytes
   def fail(path,data):
    nonlocal writes; writes+=1
    if writes==2: raise OSError("synthetic interrupted publication")
    return orig(path,data)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2],patch.object(Path,"write_bytes",fail):
    with self.assertRaisesRegex(OSError,"synthetic interrupted"): build_display.build_region("fixture",root=root,write=True)
   self.assertEqual({p.name:p.read_bytes() for p in output.iterdir()},before); self.assertEqual(list(output.parent.glob(".fixture-display-*")),[])
 def test_success_preserves_unknown_files_and_uses_normal_directory_permissions(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); output=self.setup_fixture(root)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2]: build_display.build_region("fixture",root=root,write=True)
   self.assertEqual({p.name for p in output.iterdir()},{"first.geojson","coverage.geojson","index.json","unknown.txt"})
   self.assertEqual((output/"unknown.txt").read_bytes(),b"old-unknown")
   mask=os.umask(0); os.umask(mask); self.assertEqual(stat.S_IMODE(output.stat().st_mode),0o777 & ~mask)
   self.assertEqual(list(output.parent.glob(".fixture-display-*")),[])

 def test_rename_failure_restores_previous_display(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); output=self.setup_fixture(root); before={p.name:p.read_bytes() for p in output.iterdir()}; original=Path.replace; calls=0
   def fail_stage(source,destination):
    nonlocal calls
    if source.name.startswith('.fixture-display-') and destination==output: raise OSError('stage rename failed')
    calls+=1; return original(source,destination)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2],patch.object(Path,'replace',fail_stage):
    with self.assertRaisesRegex(OSError,'stage rename failed'): build_display.build_region('fixture',root=root,write=True)
   self.assertEqual({p.name:p.read_bytes() for p in output.iterdir()},before)
   self.assertFalse((root/'regions/fixture/.display-backup').exists())

 def test_rebuild_recovers_stale_backup_and_removes_stale_stage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); parent=root/'regions/fixture'; parent.mkdir(parents=True)
   backup=parent/'.display-backup'; backup.mkdir(); (backup/'unknown.txt').write_bytes(b'keep')
   stale=parent/'.fixture-display-stale'; stale.mkdir(); (stale/'partial').write_bytes(b'partial')
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2]: build_display.build_region('fixture',root=root,write=True)
   self.assertEqual((parent/'display/unknown.txt').read_bytes(),b'keep'); self.assertFalse(stale.exists())

 def test_ambiguous_backups_fail_loudly(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); parent=root/'regions/fixture'; parent.mkdir(parents=True)
   (parent/'.display-backup-a').mkdir(); (parent/'.display-backup-b').mkdir()
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2]:
    with self.assertRaisesRegex(RuntimeError,'Ambiguous display backups'): build_display.build_region('fixture',root=root,write=True)

 def test_symlink_display_is_refused_before_publication(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); parent=root/'regions/fixture'; parent.mkdir(parents=True); target=root/'real-display'; target.mkdir(); (parent/'display').symlink_to(target, target_is_directory=True)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2]:
    with self.assertRaisesRegex(ValueError,'Refusing symlinked display'): build_display.build_region('fixture',root=root,write=True)
   self.assertFalse((parent/'.display-backup').exists())

 def test_artifact_paths_cannot_be_flattened(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); patches=self.patches(root)
   bad=({'type':'FeatureCollection','features':[]},{'path':'regions/fixture/display/nested/first.geojson','layer_id':'first','feature_count':0})
   with patches[0],patch.object(build_display,'build_layer',return_value=bad),patches[2]:
    with self.assertRaisesRegex(ValueError,'directly inside display'): build_display.build_region('fixture',root=root,write=True)

 def test_real_region_tracked_outputs_are_unchanged_after_rebuild(self):
  repo=Path(__file__).resolve().parents[3]; v2=repo/'v2'
  for region in ('aspen','douglas-co'):
   display=v2/'regions'/region/'display'
   before={p.relative_to(repo).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in display.rglob('*') if p.is_file()}
   build_display.build_region(region,v2,write=True)
   after={p.relative_to(repo).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in display.rglob('*') if p.is_file()}
   self.assertEqual(after,before,region)
