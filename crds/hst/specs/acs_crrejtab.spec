{
    'extra_keys': ('RPTCORR',),
    'file_ext': '.fits',
    'filetype': 'cosmic ray rejection',
    'ld_tpn': 'acs_crr_ld.tpn',
    'parkey': ('DETECTOR', 'RPTCORR'),
    'parkey_relevance': {},
    'reffile_format': 'table',
    'reffile_required': 'yes',
    'reffile_switch': 'crcorr',
    'rmap_relevance': '((DETECTOR != "SBC") and ((CRCORR != "OMIT") or (RPTCORR != "OMIT")))',
    'suffix': 'crr',
    'text_descr': 'Cosmic Ray Rejection Parameter Table',
    'tpn': 'acs_crr.tpn',
    'unique_rowkeys': ('CCDCHIP', 'CRSPLIT', 'MEANEXP'),
}