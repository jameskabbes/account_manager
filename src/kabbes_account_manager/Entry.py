import kabbes_account_manager
import kabbes_menu
import kabbes_user_client

class Entry( kabbes_account_manager.Base, kabbes_menu.Menu ):

    DEFAULT_ATT_VALUES = {'valid': True}

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Key', 'open_Key' ],
    "2": [ 'Open Value', 'open_Value'],
    "5": [ 'Open Entries', 'run_Entries'],
    "7": ['Delete','delete']
    }

    _IMP_ATTS = [ 'Key','Value' ]
    _ONE_LINE_ATTS = [ 'Key','Value' ]

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self, Entries, key = None, value = None, **kwargs ):

        kabbes_account_manager.Base.__init__( self, **kwargs )
        kabbes_menu.Menu.__init__( self )
        self.Entries = Entries

        #
        self.make_Key( val = key )
        if self.Key.val == '':
            self.valid = False

        if self.valid:
            self.make_Value( val = value )
        else:
            self.make_Value( val = 'so not valid bro' )

        self._Children = [ self.Key, self.Value ]

    def run_Entries( self ):
        self.Entries.run()

    def display( self ):

        return ' - '.join( [ str(self.Key.val), str(self.Value.val) ] )

    def export_to_dict( self ):

        return { self.Key.export() : self.Value.export() }

    def make_Key( self, **kwargs ):

        self.Key = kabbes_account_manager.Key( self, **kwargs )

    def make_Value( self, **kwargs ):

        self.Value = kabbes_account_manager.Value( self, **kwargs )

    def delete_self( self ):

        if self.Key.can_edit and self.Value.can_edit:
            self.Entries.delete_Entry( self )
        else:
            print ('Cannot delete Entry')

    def open_Key( self ):

        self.Key.run()

    def open_Value( self ):

        self.Value.run()

    def pre_run( self ):

        self.Value.copy()
