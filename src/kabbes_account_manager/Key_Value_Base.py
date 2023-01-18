import kabbes_account_manager 
import kabbes_menu
import py_starter as ps

class Key_Value_Base( kabbes_account_manager.Base, kabbes_menu.Menu ):

    DEFAULT_ATT_VALUES = {
    'val': None,
    'can_edit': True
    }

    _OVERRIDE_OPTIONS = {
    "1": [ 'Edit', 'edit' ],
    "2": [ 'Copy', 'copy'],
    "3": [ 'Raw Edit', 'raw_edit'],
    "4": [ 'Read from File', 'read_from_file'],
    "5": [ 'Open Entry', 'run_Entry']
    }

    MAND_ATTS = ['val']
    _IMP_ATTS = ['val']
    _ONE_LINE_ATTS = ['val']

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__(self, Entry, **kwargs ):
        
        kabbes_account_manager.Base.__init__( self, **kwargs )
        kabbes_menu.Menu.__init__( self )

        self.Entry = Entry

        # Have to
        if self.type == 'Value':
            self.prompt_string = str(self.Entry.Key.val) + ': '

        self.get_mand_entries()


    def __len__( self ):
        return 1

    def __iter__( self ):
        return self

    def __next__( self ):
        raise StopIteration

    def run_Entry( self ):
        self.Entry.run()

    def get_mand_entries( self ):

        if self.val == None:
            self.get_val()

    def read_from_file( self ):
        self.edit( from_file = True )

    def edit( self, autocomplete = True, from_file = False, **kwargs ):

        if self.can_edit:

            prev_val = self.val
            if from_file:
                self.val = self.Entry.Entries.Account.Accounts.M.cfg['file_input.Path'].read()

            else:
                self.get_val( autocomplete = autocomplete, **kwargs )

            print ( str(prev_val) + ' -> ' + str(self.val) )
            if input('Type "yes" to confirm: ') != 'yes':
                print ('Abandoning changes')
                self.val = prev_val

        else:
            print ('Cannot modify this ' + str(self.type) )

    def raw_edit( self ):

        self.edit( autocomplete = False )

    def get_autocompleted_val( self ):

        print (self.prompt_string)
        search_kwargs = {
            "searching_from": self
        }

        self.Entry.Entries.Account.Accounts.Key_Value_CRTI.get_one_input( search_kwargs = search_kwargs )
        
        if self.Entry.Entries.Account.Accounts.Key_Value_CRTI.suggestion != None: #suggestion will always be of type self.type
            self.val = self.Entry.Entries.Account.Accounts.Key_Value_CRTI.suggestion.val
        else:
            self.val = self.Entry.Entries.Account.Accounts.Key_Value_CRTI.string

    def raw_input_val( self ):

        self.val = input( self.prompt_string )

    def export( self ):

        return self.val

    def copy( self ):

        ps.copy( self.val )

    def string_found_in_Children( self, string_lower ):

        if string_lower in str(self.val).lower():
            return [ self ]
        else:
            return []

    def pre_run( self ):

        self.copy()
