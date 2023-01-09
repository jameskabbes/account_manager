import kabbes_account_manager 
import kabbes_menu
import kabbes_user_client
from parent_class import ParentPluralList

class Entries( ParentPluralList, kabbes_account_manager.Base, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Entry', 'run_Child_user' ],
    "5": [ 'Open Account', 'run_Account'],
    "7": [ '', 'do_nothing' ]
    }

    cfg_menu = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS ).cfg_menu

    def __init__( self, Account, dictionary = {}, **kwargs ):

        kabbes_account_manager.Base.__init__( self, **kwargs )
        ParentPluralList.__init__( self, att='Entries')
        kabbes_menu.Menu.__init__( self )
        self.Account = Account

        # Setup the dictionary
        self._import_from_dict( dictionary )

    def _import_from_dict( self, dictionary ):

        for key in dictionary:
            value = dictionary[ key ]
            new_Entry = self.make_Entry( key = key, value = value )

    def export_to_dict( self ):

        d = {}
        for Entry_inst in self:
            d.update( Entry_inst.export_to_dict() )

        return d

    def run_Account( self ):
        self.Account.run()

    def get_Entry( self, key ):

        for Entry_inst in self:
            if Entry_inst.Key.val == key:
                return Entry_inst
        return None

    def make_Entry( self, **kwargs ):

        new_Entry = kabbes_account_manager.Entry( self, **kwargs )

        if new_Entry.valid:
            self._add( new_Entry )

        return new_Entry

    def make_Entry_user( self ):

        while True:
            new_Entry = self.make_Entry()
            if not new_Entry.valid:
                break

        return new_Entry

    def delete_Entry( self, Entry_inst ):

        for i in range(len(self)):
            if self.Entries[i] == Entry_inst:
                del self.Entries[i]
                break

    def pre_run( self ):
        self.get_Entry( self.get_Entry( 'entry_to_copy' ).Value.val ).Value.copy()
