"""This module encapsulates code related to determining the datasets which are affected
by table changes.   The nature of the optimization is that,  viewed as a file change,  CRDS
would think a new table "affects everything" and be forced to recommend reprocessing all datasets.
The code in this module is tasked with determining if the rows selected from two versions of
a table by particular dataset parameters are actually different.   

If the rows are not different, then effectifvely the new version of the table should not cause 
a dataset to be processed.

If the rows are different,  then the dataset should be reprocessed.  
"""

from astropy.io import fits
from crds import rmap, log

def is_reprocessing_required(dataset,  dataset_parameters, old_context, new_context, update):
    """This is the top level interface to crds.bestrefs running in "Affected Datasets" mode.
    
    It determines if reprocessing `dataset` with parameters `dataset_parameters` should be performed as
    a consequence of switching from `old_reference` to `new_reference`.  old_reference is assigned to dataset
    by old_context,  and new_reference is assigned to dataset by new_context.
        
    Parameters
    ----------
    dataset: 
             id of dataset being reprocessed,  <assoc>:<member> or <unassoc>:<unassoc> format
    
    dataset_parameters:
                        { parameter : value, ...} for all matching parameters and row selection parameters
    
                        XXX row selection parameters not used in file selection may not be present until
                        XXX explicitly added to the CRDS interface to the DADSOPS parameter database...
                        XXX and possibly even to DADSOPS itself. Normally the row selections have only been
                        XXX done with direct access to dataset .fits files.
    
    old_context: loaded pmap or name of old context,  possibly for metadata or None

    new_context: loaded pmap or name of new context,  possibly for metadata
    
    update: Update object

    Returns
    -------
    True        IFF reprocessing should be done as a consequence of the table change.
    """

    # Log that deep examination is occuring.
    log.verbose('Deep examination of references instantiated.', verbosity=25)

    # What do we have as parameters
    #log.verbose('Dataset is ', dataset, verbosity=25)
    #log.verbose('dataset_parameters is ', dataset_parameters, verbosity=25)
    #log.verbose('old_context is ', old_context, verbosity=25)
    #log.verbose('new_context is ', new_context, verbosity=25)
    #log.verbose('old_reference is ', old_reference, verbosity=25)
    #log.verbose('new_reference is ', new_reference, verbosity=25)

    # Although the basic premise of the module is a table-based optimization,  if it could be
    # done for other references with benefit,  we'd want to rename the module and do it.   
    # So conceptually and practically,  these are references,  not necessarily tables.   
    # If non-tables are not  optimized,  that should be detected here and non-table-references 
    # reduced to True:  reprocess.
    
    # no old_context means "single context" mode,  always reprocess.
    if old_context == None:   
        return True
    
    # reprocess on transition from meaningless assignment (no comparison possible) to defined reference
    meaningless = ("n/a", "undefined", "not found",)
    if (update.old_reference.lower().startswith(meaningless) and 
        not update.new_reference.lower().startswith(meaningless)):
        return True

    # mostly debug wrappers here,  allows simple string parameters to work and resolves cache paths.
    #old_context = rmap.asmapping(old_context, cached=True)   
    #new_context = rmap.asmapping(new_context, cached=True)   
    old_context = rmap.asmapping(old_context, cached=True)   
    new_context = rmap.asmapping(new_context, cached=True)   
    old_reference = old_context.locate_file(update.old_reference.lower())
    new_reference = new_context.locate_file(update.new_reference.lower())
    

    # See if deep checking into the reference is possible.
    try:
        deep_look = DeepLook.from_filekind(update.instrument, update.filekind)

        # **DEBUG**
        # ** Since we are not getting full headers, if this is a test
        # ** dataset, replace the headers.
        dataset_id = dataset.split(':')[0]
        #log.verbose_warning('Forcing use of LBYX01010, regardless...', verbosity=25)
        #dataset_id = 'LBYX01010'           #***DEBUG: force headers regardless of actua data
        if dataset_id in deep_look.stub_input:
            log.verbose_warning('Substituting header for dataset "{}"'.format(dataset), verbosity=25)
            dataset_parameters = deep_look.stub_input[dataset_id]['headers']
            log.verbose_warning('headers = ', dataset_parameters, verbosity=25)


        log.verbose(deep_look.preamble, 'Dataset headers = {}'.format(dataset_parameters), verbosity=75)
        log.verbose(deep_look.preamble, 'Comparing references {} and {}.'.format(old_reference, new_reference), verbosity=75)
        deep_look.are_different(dataset_parameters, old_reference, new_reference)
        
        log.verbose(deep_look.preamble, 'Reprocessing is {}required.'.format('' if deep_look.is_different else 'not '), verbosity=25)
        log.verbose(deep_look.preamble, deep_look.message, verbosity=25)
        return deep_look.is_different

    except DeepLookError as error:

        # Could not determine difference, therefore presume so.
        log.verbose_warning('Deep examination error: {}'.format(error.message), verbosity=25)
        log.verbose_warning('Deep examination failed, presuming reprocessing.', verbosity=25)
        return True
    

###########
# Utilities
###########
def str_to_number(input, strip=True):
    
    types = [int, long, float, complex]

    result = None
    for t in types:
        try:
            result = t(input)
            break
        except:
            next
    
    if result is None:
        result = input.strip() if strip else input
        
    return result

def mode_select(table, constraints):
    """Return rows that match the constraints
    
    Parameters
    ----------
    table: FITS_rec
           Table to examine
           
    constraints: {field: (value, cmpfn, **kargs}
                 For each field, compare the given value using the
                 the specified comparison function. The cmpfn looks like
                     bool = cmpfn(row[field], value, **kargs)
                 
    Returns
    -------
    The next row that matches.
    """
    for row in table:
        selected = True
        for field in constraints:
            (value, cmpfn, args) = constraints[field]
            selected = selected & cmpfn(str_to_number(row[field]), value, args)

        if selected:
            yield row

def mode_equality(modes_a, modes_b):
    """Check if the modes are equal"""
    
    # Assume not equal
    equality = False
    
    # Must be the same length
    if len(modes_a) == len(modes_b):
        
        # Must have some length
        if len(modes_a) > 0:
            equality = (modes_a == modes_b)

        # Else, nothing compares, so basically equal
        else:
            equality = True

    # That's all folks
    return equality

###################
#
# Comparison functions
#
###################

def cmp_equal(table_value, matching_values, wildcards=[]):
    """Value equality

    Parameters
    ----------
    table_value: obj
                 Value from a reference table.

    matching_values: obj or [obj,]
                     What to check against. May be singular or a list

    wildcards: [value,]
               Values that are considered "everything".
               If the table_value is a wildcard, equality is
               presumed.
"""

    # Presume not equal
    is_equal = False

    # Is this a wildcard?
    if table_value in wildcards:
        is_equal = True

    # Otherwise, do a direct match
    else:
        try:
            is_equal = (table_value in matching_values)
        except:
            is_equal = (table_value == matching_values)

    # That's all folks.
    return is_equal


# **DEBUG**
#
# Dummy up the definitions the examination rules
# To be later placed into some type of file
##############

class DeepLookError(Exception):
    """Deep Look error base class
    """
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class DeepLook(object):
    """Base class to define how reference tables are deep-checked
    for differences between references
    """
 
    rules = {} # List of classes to use for rules.

    def __init__(self):

        # Preamble for log messages
        self.preamble = 'Rule {}:'.format(self.__class__.__name__)

        # Meta Values that may be found in header keywords
        self.metavalues = {}

        # Default mode fields
        self.mode_fields = {}

        # Default way to compare
        self.cmp_equal_parameters = (cmp_equal, {'wildcards': ['ANY']})

        # Basic presumption is that there is a difference unless
        # proven otherwise.
        self.is_different = True
        self.message = 'Comparision not done, presuming references are different.'

    @classmethod
    def from_filekind(cls, instrument, filekind):
        """Create the appropriate object for the type of reference file"""

        name = (instrument + '_' + filekind).lower()
        log.verbose('Instantiating rules for reference type {}.'.format(name), verbosity=25)
        if name in cls.rules:
            return  cls.rules[name]() 
        else:
            raise DeepLookError('No rules for instrument {} and reference file kind {}'.format(instrument, filekind))

    def are_different(self, headers, old_reference, new_reference):
        """Do the deep examination of the reference files with-respect-to the given dataset headers

        Affects
        =======
            self.is_different: Sets True or False whether the references are different.
            self.message: Reason for current state of is_different
        """

        # Convert header keys to lowercase for consistency
        headers_low = dict((k.lower(), v) for k, v in headers.iteritems())

        # Start off that the references are different.
        self.is_different = True
        self.message = 'Comparision started but not completed.'

        # Get values for the mode fields
        constraint_values = {}
        for field in self.mode_fields:
            constraint_values[field] = str_to_number(headers_low[field]) if field in headers_low else None
        if None in constraint_values.values():
            self.message = 'Not all mode fields are defined in the dataset.'
            return

        # Modify the constraint values if any "meta" values are
        # present.
        for key in constraint_values:
            if key in self.metavalues:
                if constraint_values[key] in self.metavalues[key]:
                    constraint_values[key] = self.metavalues[key][constraint_values[key]]

        # Read the references
        #**DEBUG
        # Need to generalize below for specified and multiple
        # extensions
        data_old = fits.open(old_reference)[1].data
        data_new = fits.open(new_reference)[1].data

        # Columns must be the same between tables.
        if sorted(data_old.columns.names) != sorted(data_new.columns.names):
            self.message = 'Columns are different between references.'
            return

        # Now that values are in hand, produce the full constraint
        # dictionary
        constraints = {}
        for field in self.mode_fields:
            constraints[field] = (constraint_values[field],) + self.mode_fields[field]

        # Reduce the tables to just those rows that match the mode
        # specifications.
        mode_rows_old = [repr(row) for row in mode_select(data_old, constraints)]
        mode_rows_new = [repr(row) for row in mode_select(data_new, constraints)]

        # Sort the rows
        mode_rows_old.sort()
        mode_rows_new.sort()

        # Check on equality.
        # That's all folks.
        self.is_different = not mode_equality(mode_rows_old, mode_rows_new)

        if self.is_different:
            self.message = 'Selection rules have excuted and the selected rows are different.'
        else:
            self.message = 'Selection rules have executed and the selected rows are the same.'


#############################
#
# Rules for COS
#
#############################


class DeepLook_COS(DeepLook):
    """Generic class for all COS rules
    """

    def __init__(self):
        super(DeepLook_COS, self).__init__()

        # **DEBUG**
        # Define dummy data.
        # Remove when proper headers are retrievable
        self.stub_input = { # dataset => headers
            'xLA7803FKQ': {
                'headers': {
                    'opt_elem': 'G160M',
                    'cenwave':  '1600',
                    'aperture': 'WCA',
                    'segment':  'BOTH',
                },
            },
            'xLBYX01010': {
                'headers': {
                    'opt_elem': 'G140L',
                    'cenwave':  '1280',
                    'aperture': 'PSA',
                    'segment':  'FUVB',
                },
            },
            'xLB4P02050': {
                'headers': {
                    'opt_elem': 'G160M',
                    'cenwave':  '1600',
                    'aperture': 'PSA',
                },
            },
            'xLB4P07010': {
                'headers': {
                    'opt_elem': 'G140L',
                    'cenwave':  '1230',
                    'aperture': 'PSA',
                },
            },
            'xLB6M01030': {
                'headers': {
                    'opt_elem': 'G230L',
                    'cenwave':  '3000',
                    'aperture': 'PSA',
                },
            },
            'xLBK617010': {
                'headers': {
                    'opt_elem': 'G185M',
                    'cenwave':  '1986',
                    'aperture': 'PSA',
                },
            },
        }


class DeepLook_COSSegment(DeepLook_COS):
    """Tables that require SEGMENT only"""

    def __init__(self):
        super(DeepLook_COSSegment, self).__init__()

        self.mode_fields = {
            'segment': self.cmp_equal_parameters,
        }


class DeepLook_COSFullmode(DeepLook_COS):
    def __init__(self):
        super(DeepLook_COSFullmode, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'cenwave':  self.cmp_equal_parameters,
            'aperture': self.cmp_equal_parameters,
        }


class DeepLook_COSOpt_elem(DeepLook_COS):
    def __init__(self):
        super(DeepLook_COSOpt_elem, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
        }


class DeepLook_COSDISPTAB(DeepLook_COS):
    def __init__(self):
        super(DeepLook_COSDISPTAB, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'cenwave':  self.cmp_equal_parameters,
        }


class DeepLook_COSLAMPTAB(DeepLook_COS):
    def __init__(self):
        super(DeepLook_COSLAMPTAB, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'cenwave':  self.cmp_equal_parameters,
            'fpoffset': self.cmp_equal_parameters,
        }

class DeepLook_COSTDSTAB(DeepLook_COS):
    def __init__(self):
        super(DeepLook_COSTDSTAB, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'aperture': self.cmp_equal_parameters,
        }



#############################
#
# Rules for STIS
#
#############################


class DeepLook_STIS(DeepLook):
    """Generic class for all STIS rules
    """

    def __init__(self):
        super(DeepLook_STIS, self).__init__()

        # **DEBUG**
        # Define dummy data.
        # Remove when proper headers are retrievable
        self.stub_input = { # dataset => headers
        }

class DeepLook_STISopt_elem(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISopt_elem, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
        }

class DeepLook_STISaperture(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISaperture, self).__init__()

        self.mode_fields = {
            'aperture': self.cmp_equal_parameters,
        }

class DeepLook_STIScenwave(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STIScenwave, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'cenwave': self.cmp_equal_parameters,
        }

class DeepLook_STISfullmode(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISfullmode, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'cenwave':  self.cmp_equal_parameters,
            'aperture': self.cmp_equal_parameters,
        }

class DeepLook_STISCCDTAB(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISCCDTAB, self).__init__()

        self.mode_fields = {
            'ccdamp': self.cmp_equal_parameters,
            'ccdgain': self.cmp_equal_parameters,
            'ccdoffst': self.cmp_equal_parameters,
            'binaxis1': self.cmp_equal_parameters,
            'binaxis2': self.cmp_equal_parameters,
        }

class DeepLook_STISLAMPTAB(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISLAMPTAB, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'lampset': self.cmp_equal_parameters,
            'sclamp': self.cmp_equal_parameters,
        }

class DeepLook_STISMLINTAB(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISMLINTAB, self).__init__()

        self.mode_fields = {
            'detector': self.cmp_equal_parameters,
        }

class DeepLook_STISWCPTAB(DeepLook_STIS):
    def __init__(self):
        super(DeepLook_STISWCPTAB, self).__init__()

        self.mode_fields = {
            'opt_elem': self.cmp_equal_parameters,
            'detector': self.cmp_equal_parameters,
        }




DeepLook.rules = {
    'cos_bpixtab':   DeepLook_COSSegment,
    'cos_brsttab':   DeepLook_COSSegment,
    'cos_deadtab':   DeepLook_COSSegment,
    'cos_disptab':   DeepLook_COSDISPTAB,
    'cos_fluxtab':   DeepLook_COSFullmode,
    'cos_lamptab':   DeepLook_COSLAMPTAB,
    'cos_phatab':    DeepLook_COSOpt_elem,
    'cos_spwcstab':  DeepLook_COSFullmode,
    'cos_tdstab':    DeepLook_COSTDSTAB,
    'cos_walktab':   DeepLook_COSSegment,
    'cos_wcptab':    DeepLook_COSOpt_elem,
    'cos_xtractab':  DeepLook_COSFullmode,
    'stis_apdestab': DeepLook_STISaperture,
    'stis_apertab':  DeepLook_STISaperture,
    'stis_bpixtab':  DeepLook_STISopt_elem,
    'stis_ccdtab':   DeepLook_STISCCDTAB,
    'stis_cdstab':   DeepLook_STISopt_elem,
    'stis_disptab':  DeepLook_STIScenwave,
    'stis_echsctab': DeepLook_STISopt_elem,
    'stis_exstab':   DeepLook_STISopt_elem,
    'stis_halotab':  DeepLook_STISopt_elem,
    'stis_lamptab':  DeepLook_STISLAMPTAB,
    'stis_mlintab':  DeepLook_STISMLINTAB,
    'stis_phottab':  DeepLook_STIScenwave,
    'stis_riptab':   DeepLook_STISopt_elem,
    'stis_sdctab':   DeepLook_STISfullmode,
    'stis_sptrctab': DeepLook_STIScenwave,
    'stis_srwtab':   DeepLook_STISopt_elem,
    'stis_tdstab':   DeepLook_STISopt_elem,
    'stis_teltab':   DeepLook_STISopt_elem,
    'stis_wcptab':   DeepLook_STISWCPTAB,
    'stis_xtractab': DeepLook_STISfullmode,
}
