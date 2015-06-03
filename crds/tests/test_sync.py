"""This module contains doctests and unit tests which exercise some of the more
complex features of the basic rmap infrastructure.

"""

from __future__ import division # confidence high
from __future__ import with_statement
from __future__ import print_function

import os

import crds
from crds import log, config, rmap
from crds.sync import SyncScript
from crds.tests import CRDSTestCase, test_config

# ==================================================================================

class TestSync(CRDSTestCase):
    
    script_class = SyncScript

    def setUp(self):
        super(TestSync, self).setUp()
        config.clear_crds_state()
        os.environ["CRDS_PATH"] = self.temp_dir
        os.environ["CRDS_REF_SUBDIR_MODE"] = "flat"
        log.set_test_mode()

    def test_sync_contexts(self):
        self.run_script("crds.sync --contexts hst_cos.imap")
        for name in crds.get_cached_mapping("hst_cos.imap").mapping_names():
            self.assert_crds_exists(name)
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references")
        for name in crds.get_cached_mapping("hst_cos_deadtab.rmap").reference_names():
            self.assert_crds_exists(name)
            with open(config.locate_file(name, "hst"), "w+") as handle:
                handle.write("foo")
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --check-files", 2)
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --check-files --repair-files", 2)
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --check-files --repair-files")
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --check-files --repair-files --check-sha1sum")

    def test_sync_explicit_files(self):
        self.assert_crds_not_exists("hst_cos_deadtab.rmap")
        self.run_script("crds.sync --files hst_cos_deadtab.rmap --check-files --repair-files --check-sha1sum")
        crds.get_cached_mapping("hst_cos_deadtab.rmap")

    def test_sync_readonly_cache(self):
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --readonly-cache")

    def test_sync_organize_flat(self):
        self.assert_crds_not_exists("hst_cos_deadtab.rmap")
        self.assert_crds_not_exists("s7g1700gl_dead.fits")
        self.assert_crds_not_exists("s7g1700ql_dead.fits")
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --organize=flat")
        self.assert_crds_exists("hst_cos_deadtab.rmap")
        self.assert_crds_exists("s7g1700gl_dead.fits")
        self.assert_crds_exists("s7g1700ql_dead.fits")
    
    def test_sync_organize_instr(self):
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --organize=instrument --organize-delete-junk")
        self.assert_crds_exists("hst_cos_deadtab.rmap")
        self.assert_crds_exists("s7g1700gl_dead.fits")
        self.assert_crds_exists("s7g1700ql_dead.fits")
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references --organize=flat --organize-delete-junk")
        
    def test_sync_fetch_sqlite3_db(self):
        self.run_script("crds.sync --fetch-sqlite-db")
        
    def test_sync_dataset_ids(self):
        old_state = test_config.setup()
        self.run_script("crds.sync --contexts hst.pmap --dataset-ids LA9K03CBQ:LA9K03CBQ --fetch-references")
        test_config.cleanup(old_state)
        
    def test_purge_mappings(self):
        self.run_script("crds.sync --contexts hst_cos_deadtab.rmap --fetch-references")
        self.run_script("crds.sync --organize=flat")
        r = crds.get_cached_mapping("hst_cos_deadtab.rmap")
        self.assertEqual(r.reference_names(), ["s7g1700gl_dead.fits", "s7g1700ql_dead.fits"])
        self.assertEqual(rmap.list_references("*", "hst"), ["s7g1700gl_dead.fits", "s7g1700ql_dead.fits"])
        self.assert_crds_exists("s7g1700gl_dead.fits")
        self.assert_crds_exists("s7g1700ql_dead.fits")
        self.run_script("crds.sync --contexts hst_acs_imphttab.rmap --fetch-references --purge-mappings --purge-references")
        self.assertEqual(rmap.list_references("*", "hst"), ['w3m1716tj_imp.fits', 'w3m17170j_imp.fits', 'w3m17171j_imp.fits'])
        self.assertEqual(rmap.list_mappings("*", "hst"), ['hst_acs_imphttab.rmap'])
        
# ==================================================================================


def tst():
    """Run module tests,  for now just doctests only."""
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSync)
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    print(tst())