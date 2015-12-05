"""This module is used to generate unique time based file names."""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os.path
import sys
import datetime

from astropy.io import fits

from crds import cmdline, config, log, naming

class UniqnameScript(cmdline.Script):

    """Command line script for renaming references with official CRDS names."""

    description = """This script is used to rename references with unique official CRDS names."""
        
    epilog = """


    """

    def __init__(self, *args, **keys):
        super(UniqnameScript, self).__init__(*args, **keys)
    
    def add_args(self):
        """Setup command line switch parsing."""
        self.add_argument('--files', nargs="*", 
                          help="Files to rename.")
        self.add_argument('--dry-run', action='store_true',
                          help='Print how a file would be renamed without modifying it.')
        self.add_argument('-a', '--add-checksum', action='store_true',
                          help='Add FITS checksum.  Without, checksums *removed* if header modified.')
        self.add_argument('-f', '--add-filename-keywords', action='store_true',
                          help='When renaming, add FILENAME, ROOTNAME, HISTORY keywords for the generated name.')
        self.add_argument('-e', '--verify-file', action='store_true', 
                          help='Verify FITS compliance and any checksums before changing each file.')
        self.add_argument('-s', '--standard', action='store_true', 
                          help='Same as --add-filename-keywords --verify-file,  does not add checksums (add -a).')
        self.add_argument('-r', '--remove-original', action='store_true',
                          help='After renaming,  remove the orginal file.')
        self.add_argument('-o', '--output-path',
                          help='Output renamed files to this directory path.')
        self.add_argument('-b', '--brief', action='store_true',
                          help='Produce less output.')
        super(UniqnameScript, self).add_args()

    locate_file = cmdline.Script.locate_file_outside_cache
        
    def main(self):
        """Generate names corrsponding to files listed on the command line."""
        if self.args.standard:
            self.args.add_filename_keywords = True
            self.args.verify_file = True
        for filename in self.files:
            assert config.is_reference(filename), \
                "File " + repr(filename) + " does not appear to be a reference file.  Only references can be renamed."
            uniqname = naming.generate_unique_name(filename, self.observatory)
            if self.args.dry_run:
                log.info("Would rename", self.format_file(filename), "-->", self.format_file(uniqname))
            else:
                self.rewrite(filename, uniqname)
                if self.args.remove_original:
                    os.remove(filename)
    
    def rewrite(self, filename, uniqname):
        """Add a FITS checksum to `filename.`"""
        hdus = fits.open(filename, mode="readonly", checksum=self.args.verify_file)
        if self.args.verify_file:
            hdus.verify("fix+warn")
        basename = os.path.basename(uniqname)
        if self.args.add_filename_keywords:
            now = datetime.datetime.now()
            hdus[0].header["FILENAME"] = basename
            hdus[0].header["ROOTNAME"] = os.path.splitext(basename)[0].upper()
            hdus[0].header["HISTORY"] = "{0} renamed to {1} on {2} {3} {4}".format(
                os.path.basename(filename), basename, MONTHS[now.month - 1], now.day, now.year)
        if self.args.output_path:
            uniqname = os.path.join(self.args.outpath, basename)
        log.info("Rewriting", self.format_file(filename), "-->", self.format_file(uniqname))
        hdus.writeto(uniqname, output_verify="fix+warn", checksum=self.args.add_checksum)

    def format_file(self, filename):
        """Print absolute path or basename of `filename` depending on command line --brief"""
        return repr(os.path.basename(filename) if self.args.brief else filename)

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
    
if __name__ == "__main__":
    sys.exit(UniqnameScript()())