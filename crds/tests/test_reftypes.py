from __future__ import division # confidence high
from __future__ import with_statement
from __future__ import print_function
from __future__ import absolute_import

# ==================================================================================

import os
import tempfile

# ==================================================================================
import numpy as np

from nose.tools import assert_raises, assert_true

# ==================================================================================

from crds.core import utils, log, exceptions
from crds.certify import reftypes
from crds import hst, jwst

from crds.tests import test_config

# ==================================================================================


def reftypes_load_type_spec_spec():
    """
    >>> old_state = test_config.setup()
    >>> SPEC_FILE = os.path.join(os.path.abspath(hst.HERE), "specs", "acs_biasfile.spec")
    >>> spec = reftypes.TypeSpec.from_file(SPEC_FILE)
    >>> test_config.cleanup(old_state)
    """

def reftypes_load_type_spec_rmap():
    """
    >>> old_state = test_config.setup()
    >>> SPEC_FILE = os.path.join(os.path.abspath(hst.HERE), "specs", "cos_xwlkfile.rmap")
    >>> spec = reftypes.TypeSpec.from_file(SPEC_FILE)
    >>> test_config.cleanup(old_state)
    """

def reftypes_hst_load_raw_specs():
    """
    >>> old_state = test_config.setup()
    >>> SPECS = os.path.join(os.path.abspath(hst.HERE), "specs")
    >>> spec = reftypes.load_raw_specs(SPECS)
    >>> test_config.cleanup(old_state)
    """
  
def reftypes_hst_save_json_specs():
    """
    >>> old_state = test_config.setup()
    >>> SPECS = os.path.join(os.path.abspath(hst.HERE), "specs")
    >>> specs = reftypes.load_raw_specs(SPECS)
    >>> f = tempfile.NamedTemporaryFile(delete=False)
    >>> f.close()
    >>> reftypes.save_json_specs(specs, f.name)  # doctest: +ELLIPSIS
    CRDS - INFO -  Saved combined type specs to '...'
    >>> test_config.cleanup(old_state)
    """
  
def reftypes_jwst_load_raw_specs():
    """
    >>> old_state = test_config.setup()
    >>> SPECS = os.path.join(os.path.abspath(jwst.HERE), "specs")
    >>> spec = reftypes.load_raw_specs(SPECS)
    >>> test_config.cleanup(old_state)
    """
  
def reftypes_jwst_save_json_specs():
    """
    >>> old_state = test_config.setup()
    >>> SPECS = os.path.join(os.path.abspath(jwst.HERE), "specs")
    >>> specs = reftypes.load_raw_specs(SPECS)
    >>> f = tempfile.NamedTemporaryFile(delete=False)
    >>> f.close()
    >>> reftypes.save_json_specs(specs, f.name) # doctest: +ELLIPSIS
    CRDS - INFO -  Saved combined type specs to '...'
    >>> test_config.cleanup(old_state)
    """
  
def reftypes_hst_reference_name_to_tpn_infos():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("hst")
    >>> infos = types.reference_name_to_tpninfos("data/s7g1700gl_dead.fits")
    >>> print(log.PP(infos))
    [('DESCRIP', 'HEADER', 'CHARACTER', 'REQUIRED', values=()),
     ('DETECTOR', 'HEADER', 'CHARACTER', 'REQUIRED', values=('FUV', 'NUV')),
     ('FILETYPE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('DEADTIME REFERENCE TABLE',)),
     ('INSTRUME', 'HEADER', 'CHARACTER', 'REQUIRED', values=('COS',)),
     ('PEDIGREE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&PEDIGREE',)),
     ('SEGMENT', 'COLUMN', 'CHARACTER', 'REQUIRED', values=('FUVA', 'FUVB', 'ANY')),
     ('USEAFTER', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&SYBDATE',)),
     ('VCALCOS', 'HEADER', 'CHARACTER', 'REQUIRED', values=())]
    >>> test_config.cleanup(old_state)
    """

def reftypes_jwst_reference_name_to_tpn_infos():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("jwst")
    >>> infos = types.reference_name_to_tpninfos("data/jwst_miri_flat_slitlessprism.fits")
    >>> print(log.PP(infos))
    [('DETECTOR', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_XSTART+DQ_ARRAY.SHAPE[-1]-1<=1032)'),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_YSTART+DQ_ARRAY.SHAPE[-2]-1<=1024)'),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_FULL_FRAME', expression='(DQ_ARRAY.SHAPE[-2:]==(1024,1032))'),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression="(has_type(DQ_ARRAY,'INT'))"),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression='(is_image(DQ_ARRAY))'),
     ('DQ', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_SUBARRAY', expression='(DQ_ARRAY.SHAPE[-2:]==(META_SUBARRAY_YSIZE,META_SUBARRAY_XSIZE))'),
     ('DQ', 'ARRAY_DATA', 'EXPRESSION', 'REQUIRED', expression="(has_type(DQ_ARRAY,'INT'))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression="(has_column_type(DQ_DEF_ARRAY,'BIT','INT'))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression="(has_column_type(DQ_DEF_ARRAY,'DESCRIPTION','STRING'))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression="(has_column_type(DQ_DEF_ARRAY,'NAME','STRING'))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression="(has_column_type(DQ_DEF_ARRAY,'VALUE','INT'))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression="(has_columns(DQ_DEF_ARRAY,['BIT','VALUE','NAME','DESCRIPTION']))"),
     ('DQ_DEF', 'ARRAY_DATA', 'EXPRESSION', condition='(DQ_ARRAY.DATA.sum())', expression='(is_table(DQ_DEF_ARRAY))'),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_XSTART+ERR_ARRAY.SHAPE[-1]-1<=1032)'),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_YSTART+ERR_ARRAY.SHAPE[-2]-1<=1024)'),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_FULL_FRAME', expression='(ERR_ARRAY.SHAPE[-2:]==(1024,1032))'),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression="(has_type(ERR_ARRAY,'FLOAT'))"),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression='(is_image(ERR_ARRAY))'),
     ('ERR', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_SUBARRAY', expression='(ERR_ARRAY.SHAPE[-2:]==(META_SUBARRAY_YSIZE,META_SUBARRAY_XSIZE))'),
     ('EXP_TYPE', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('FULLFRAME_XSIZE', 'EXPRESSION', 'EXPRESSION', 'IF_FULL_FRAME', expression='(META_SUBARRAY_XSIZE==1032)'),
     ('FULLFRAME_XSTART', 'EXPRESSION', 'EXPRESSION', 'IF_FULL_FRAME', expression='(META_SUBARRAY_XSTART==1)'),
     ('FULLFRAME_YSIZE', 'EXPRESSION', 'EXPRESSION', 'IF_FULL_FRAME', expression='(META_SUBARRAY_YSIZE==1024)'),
     ('FULLFRAME_YSTART', 'EXPRESSION', 'EXPRESSION', 'IF_FULL_FRAME', expression='(META_SUBARRAY_YSTART==1)'),
     ('META.EXPOSURE.READPATT', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('ACQ1', 'ACQ2', 'ALLIRS2', 'BRIGHT1', 'BRIGHT2', 'DEEP2', 'DEEP8', 'FAST', 'FASTGRPAVG', 'FASTINTAVG', 'FGS', 'FGS60', 'FGS8370', 'FGS840', 'FGSRAPID', 'FINEGUIDE', 'ID', 'MEDIUM2', 'MEDIUM8', 'NIS', 'NISRAPID', 'NRS', 'NRSIRS2', 'NRSN16R4', 'NRSN32R8', 'NRSN8R2', 'NRSRAPID', 'NRSIRS2RAPID', 'ALLIRS2', 'NRSSLOW', 'RAPID', 'SHALLOW2', 'SHALLOW4', 'SLOW', 'TRACK', 'ANY', 'N/A')),
     ('META.EXPOSURE.TYPE', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('FGS_DARK', 'FGS_FOCUS', 'FGS_IMAGE', 'FGS_INTFLAT', 'FGS_SKYFLAT', 'MIR_IMAGE', 'MIR_TACQ', 'MIR_LYOT', 'MIR_4QPM', 'MIR_LRS-FIXEDSLIT', 'MIR_LRS-SLITLESS', 'MIR_MRS', 'MIR_DARK', 'MIR_FLAT-IMAGE', 'MIR_FLATIMAGE', 'MIR_FLAT-MRS', 'MIR_FLATMRS', 'MIR_CORONCAL', 'NIS_AMI', 'NIS_DARK', 'NIS_FOCUS', 'NIS_IMAGE', 'NIS_LAMP', 'NIS_SOSS', 'NIS_TACQ', 'NIS_TACONFIRM', 'NIS_WFSS', 'N/A', 'ANY', 'NRC_IMAGE', 'NRC_GRISM', 'NRC_TACQ', 'NRC_CORON', 'NRC_FOCUS', 'NRC_DARK', 'NRC_FLAT', 'NRC_LED', 'NRC_WFSC', 'NRC_TACONFIRM', 'NRC_TSIMAGE', 'NRC_TSGRISM', 'NRS_AUTOFLAT', 'NRS_AUTOWAVE', 'NRS_BOTA', 'NRS_BRIGHTOBJ', 'NRS_CONFIRM', 'NRS_DARK', 'NRS_FIXEDSLIT', 'NRS_FOCUS', 'NRS_IFU', 'NRS_IMAGE', 'NRS_LAMP', 'NRS_MIMF', 'NRS_MSASPEC', 'NRS_TACONFIRM', 'NRS_TACQ', 'NRS_TASLIT', 'ANY', 'N/A')),
     ('META.EXPOSURE.TYPE', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('MIR_IMAGE', 'MIR_TACQ', 'MIR_LYOT', 'MIR_4QPM', 'MIR_LRS-FIXEDSLIT', 'MIR_LRS-SLITLESS', 'MIR_MRS', 'MIR_DARK', 'MIR_FLATIMAGE', 'MIR_FLATMRS', 'MIR_FLAT-IMAGE', 'MIR_FLAT-MRS', 'MIR_CORONCAL', 'ANY', 'N/A')),
     ('META.INSTRUMENT.BAND', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('SHORT', 'MEDIUM', 'LONG', 'ANY', 'N/A')),
     ('META.INSTRUMENT.CHANNEL', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('1', '2', '3', '4', '12', '34', 'ANY', 'N/A')),
     ('META.INSTRUMENT.DETECTOR', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('MIRIFULONG', 'MIRIFUSHORT', 'MIRIMAGE', 'ANY', 'N/A')),
     ('META.INSTRUMENT.FILTER', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('CLEAR', 'F070LP', 'F070W', 'F090W', 'F1000W', 'F100LP', 'F1065C', 'F110W', 'F1130W', 'F1140C', 'F115W', 'F1280W', 'F140M', 'F140X', 'F1500W', 'F150W', 'F150W2', 'F1550C', 'F170LP', 'F1800W', 'F182M', 'F187N', 'F200W', 'F2100W', 'F210M', 'F212N', 'F227W', 'F2300C', 'F250M', 'F2550W', 'F2550WR', 'F277W', 'F290LP', 'F300M', 'F322W2', 'F335M', 'F356W', 'F360M', 'F380M', 'F410M', 'F430M', 'F444W', 'F460M', 'F480M', 'F560W', 'F770W', 'FLENS', 'FND', 'FNDP750L', 'GR150C', 'GR150R', 'OPAQUE', 'P750L', 'WL3', 'WLP4', 'ANY', 'N/A')),
     ('META.INSTRUMENT.GRATING', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('G140M', 'G235M', 'G395M', 'G140H', 'G235H', 'G395H', 'PRISM', 'MIRROR', 'N/A', 'ANY')),
     ('META.INSTRUMENT.NAME', 'HEADER', 'CHARACTER', 'REQUIRED', values=('MIRI',)),
     ('META.INSTRUMENT.PUPIL', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('CLEAR', 'CLEARP', 'F090W', 'F115W', 'F140M', 'F150W', 'F158M', 'F162M', 'F164N', 'F200W', 'F323N', 'F405N', 'F466N', 'F470N', 'FLAT', 'GDHS', 'GDHS0', 'GDHS60', 'GR700XD', 'GRISMC', 'GRISMR', 'GRISMV2', 'GRISMV3', 'MASKBAR', 'MASKIPR', 'MASKRND', 'NRM', 'PINHOLES', 'WLM8', 'WLP4', 'WLP8', 'ANY', 'N/A')),
     ('META.REFFILE.AUTHOR', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('META.REFFILE.DESCRIPTION', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('META.REFFILE.HISTORY', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('META.REFFILE.PEDIGREE', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('&PEDIGREE',)),
     ('META.REFFILE.TYPE', 'HEADER', 'CHARACTER', 'REQUIRED', values=()),
     ('META.REFFILE.USEAFTER', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&JWSTDATE',)),
     ('META.SUBARRAY.FASTAXIS', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1', '-1', '2', '-2')),
     ('META.SUBARRAY.FASTAXIS', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.SUBARRAY.NAME', 'HEADER', 'CHARACTER', 'OPTIONAL', values=()),
     ('META.SUBARRAY.NAME', 'HEADER', 'CHARACTER', 'OPTIONAL', values=('1024X16', '128X128', '128X2048', '2048X128', '2048X64', '32X32', '64X2048', '8X8', 'ALLSLITS', 'BRIGHTSKY', 'FULL', 'GENERIC', 'MASKA210R', 'MASKA335R', 'MASKA430R', 'MASKBLWB', 'MASKBSWB', 'MASK1065', 'MASK1140', 'MASK1550', 'MASKLYOT', 'S1600A1', 'S200A1', 'S200A2', 'S200B1', 'S400A1', 'SLITLESSPRISM', 'STRIPE', 'SUB1024A', 'SUB1024B', 'SUB128', 'SUB128LLCORNER', 'SUB128DIAGONAL', 'SUB128CENTER', 'SUB16', 'SUB160', 'SUB160P', 'SUB1A', 'SUB1B', 'SUB2048', 'SUB256', 'SUB32', 'SUB32LLCORNER', 'SUB32DIAGONAL', 'SUB32CENTER', 'SUB320', 'SUB400P', 'SUB512', 'SUB64', 'SUB640', 'SUB64P', 'SUB80', 'SUB8LLCORNER', 'SUB8DIAGONAL', 'SUB8CENTER', 'SUB96', 'SUBAMPCAL', 'SUBFP1A', 'SUBFP1B', 'SUBGRISM128', 'SUBGRISM256', 'SUBGRISM64', 'SUBSTRIP256', 'SUBSTRIPE256', 'SUBSTRIP96', 'SUBPRISM', 'SUBSTRIP80', 'SUBTASOSS', 'SUBTAAMI', 'WFSS128C', 'WFSS128R', 'WFSS64C', 'WFSS64R', 'ANY', 'N/A')),
     ('META.SUBARRAY.NAME', 'HEADER', 'CHARACTER', 'REQUIRED', values=()),
     ('META.SUBARRAY.SLOWAXIS', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1', '-1', '2', '-2')),
     ('META.SUBARRAY.SLOWAXIS', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.SUBARRAY.XSIZE', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1:1032',)),
     ('META.SUBARRAY.XSIZE', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.SUBARRAY.XSTART', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1:1032',)),
     ('META.SUBARRAY.XSTART', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.SUBARRAY.YSIZE', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1:1024',)),
     ('META.SUBARRAY.YSIZE', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.SUBARRAY.YSTART', 'HEADER', 'INTEGER', 'OPTIONAL', values=('1:1024',)),
     ('META.SUBARRAY.YSTART', 'HEADER', 'INTEGER', 'REQUIRED', values=()),
     ('META.TELESCOPE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('JWST',)),
     ('MIRIFULONG_AXIS', 'EXPRESSION', 'EXPRESSION', condition="(DETECTOR=='MIRIFULONG')", expression='((FASTAXIS==1)and(SLOWAXIS==2))'),
     ('MIRIFUSHORT_AXIS', 'EXPRESSION', 'EXPRESSION', condition="(DETECTOR=='MIRIFUSHORT')", expression='((FASTAXIS==1)and(SLOWAXIS==2))'),
     ('MIRIMAGE_AXIS', 'EXPRESSION', 'EXPRESSION', condition="(DETECTOR=='MIRIMAGE')", expression='((FASTAXIS==1)and(SLOWAXIS==2))'),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_XSTART+SCI_ARRAY.SHAPE[-1]-1<=1032)'),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_YSTART+SCI_ARRAY.SHAPE[-2]-1<=1024)'),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_FULL_FRAME', expression='(SCI_ARRAY.SHAPE[-2:]==(1024,1032))'),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression="(has_type(SCI_ARRAY,'FLOAT'))"),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'REQUIRED', expression='(is_image(SCI_ARRAY))'),
     ('SCI', 'ARRAY_FORMAT', 'EXPRESSION', 'IF_SUBARRAY', expression='(SCI_ARRAY.SHAPE[-2:]==(META_SUBARRAY_YSIZE,META_SUBARRAY_XSIZE))'),
     ('SUBARRAY_INBOUNDS_X', 'EXPRESSION', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_XSTART+META_SUBARRAY_XSIZE-1<=1032)'),
     ('SUBARRAY_INBOUNDS_Y', 'EXPRESSION', 'EXPRESSION', 'ANY_SUBARRAY', expression='(1<=META_SUBARRAY_YSTART+META_SUBARRAY_YSIZE-1<=1024)')]
    >>> test_config.cleanup(old_state)
    """
def reftypes_hst_get_filekinds():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("hst")
    >>> types.get_filekinds("nicmos")
    ['backtab', 'darkfile', 'flatfile', 'idctab', 'illmfile', 'maskfile', 'nlinfile', 'noisfile', 'pedsbtab', 'phottab', 'pmodfile', 'pmskfile', 'rnlcortb', 'saacntab', 'saadfile', 'tdffile', 'tempfile', 'zprattab']
    >>> test_config.cleanup(old_state)
    """

def reftypes_jwst_get_filekinds():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("jwst")
    >>> types.get_filekinds("niriss")
    ['all', 'amplifier', 'area', 'dark', 'distortion', 'extract1d', 'flat', 'gain', 'ipc', 'linearity', 'mask', 'pathloss', 'photom', 'readnoise', 'regions', 'saturation', 'specwcs', 'superbias', 'throughput', 'wcsregions']
    >>> test_config.cleanup(old_state)
    """
    
def reftypes_reference_name_to_tpn_text():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("hst")
    >>> print(types.reference_name_to_tpn_text("data/s7g1700gl_dead.fits"))
    [('DESCRIP', 'HEADER', 'CHARACTER', 'REQUIRED', values=()),
     ('DETECTOR', 'HEADER', 'CHARACTER', 'REQUIRED', values=('FUV', 'NUV')),
     ('FILETYPE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('DEADTIME REFERENCE TABLE',)),
     ('INSTRUME', 'HEADER', 'CHARACTER', 'REQUIRED', values=('COS',)),
     ('PEDIGREE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&PEDIGREE',)),
     ('SEGMENT', 'COLUMN', 'CHARACTER', 'REQUIRED', values=('FUVA', 'FUVB', 'ANY')),
     ('USEAFTER', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&SYBDATE',)),
     ('VCALCOS', 'HEADER', 'CHARACTER', 'REQUIRED', values=())]
    >>> test_config.cleanup(old_state)
    """

def reftypes_reference_name_to_ld_tpn_text():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("hst")
    >>> print(types.reference_name_to_tpn_text("data/s7g1700gl_dead.fits"))
    [('DESCRIP', 'HEADER', 'CHARACTER', 'REQUIRED', values=()),
     ('DETECTOR', 'HEADER', 'CHARACTER', 'REQUIRED', values=('FUV', 'NUV')),
     ('FILETYPE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('DEADTIME REFERENCE TABLE',)),
     ('INSTRUME', 'HEADER', 'CHARACTER', 'REQUIRED', values=('COS',)),
     ('PEDIGREE', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&PEDIGREE',)),
     ('SEGMENT', 'COLUMN', 'CHARACTER', 'REQUIRED', values=('FUVA', 'FUVB', 'ANY')),
     ('USEAFTER', 'HEADER', 'CHARACTER', 'REQUIRED', values=('&SYBDATE',)),
     ('VCALCOS', 'HEADER', 'CHARACTER', 'REQUIRED', values=())]
    >>> test_config.cleanup(old_state)
    """
    

def reftypes_get_row_keys_by_instrument():
    """
    >>> old_state = test_config.setup()
    >>> types = reftypes.get_types_object("hst")
    >>> types.get_row_keys_by_instrument("cos")
    ['aperture', 'cenwave', 'date', 'fpoffset', 'opt_elem', 'segment']
    >>> test_config.cleanup(old_state)
    """

# ==================================================================================

class TestReftypes(test_config.CRDSTestCase):

    def setUp(self, *args, **keys):
        super(TestReftypes, self).setUp(*args, **keys)
        self._old_debug = log.set_exception_trap(False)

    def tearDown(self, *args, **keys):
        super(TestReftypes, self).tearDown(*args, **keys)
        log.set_exception_trap(self._old_debug)
        
    # ------------------------------------------------------------------------------
        
    def test_validator_bad_presence(self):
        #         tinfo = certify.TpnInfo('DETECTOR','H','C','Q', ('WFC','HRC','SBC'))
        #         assert_raises(ValueError, certify.validator, tinfo)
        pass
    
# ==================================================================================

def main():
    """Run module tests,  for now just doctests only."""
    import unittest

    suite = unittest.TestLoader().loadTestsFromTestCase(TestReftypes)
    unittest.TextTestRunner().run(suite)

    from crds.tests import test_reftypes, tstmod
    return tstmod(test_reftypes)

if __name__ == "__main__":
    print(main())
