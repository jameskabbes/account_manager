from parent_class import ParentPluralDict
import kabbes_account_manager
import kabbes_menu
import py_starter as ps
import pandas as pd
import kabbes_cryptography as cryp


class Accounts( ParentPluralDict, kabbes_account_manager.Base, kabbes_menu.Menu ):

    _OVERRIDE_OPTIONS = {
    "1": [ 'Open Account', 'run_Child_user' ],
    "2": [ 'Make Account', 'make_Account_user'],
    "5": [ 'Export non-encrypted', 'export_non_encrypted' ],
    "6": [ 'Backup Accounts', 'backup' ]
    }

    MAX_PRINT_LENGTH = 10

    menu_client = kabbes_menu.Client( _OVERRIDE_OPTIONS=_OVERRIDE_OPTIONS )
    cfg_menu = menu_client.cfg_menu


    def __init__(self, Manager, **kwargs ):

        ParentPluralDict.__init__( self, 'Accounts' )
        kabbes_account_manager.Base.__init__( self, **kwargs )
        kabbes_menu.Menu.__init__( self )

        #
        self.M = Manager
        self.Key_Value_CRTI = kabbes_account_manager.Key_Value_CRTI( self )

        #
        self.load_Account_templates()

        #
        is_empty = self.get_Dir_user()
        self.setup_encryption()

        # Load Accounts
        self._import_from_Dir( is_empty )

    def get_Acc_by_att_value( self, att, value ):

        for Acc in self:
            if Acc.Entries.get_Entry( att ) != None:
                if Acc.get_Entry_key_value( att ) == value:
                    return Acc
        return None

    def sort( self, keys = [ 'times_accessed', 'access_date' ], ascending = [] ):

        if ascending == []:
            ascending = [ False, ] * len(keys)

        df = pd.DataFrame( { 'self': list(self.Accounts.values()) } )
        for key in keys:
            df[ key ] = df[ 'self' ].apply( lambda Acc: Acc.get_Entry_key_value( key ) )

        df.sort_values( keys, ascending = ascending, inplace = True )
        df.reset_index( drop = True, inplace = True )

        self.Accounts = {}
        for i in range(len(df)):
            self._add_Account( df.loc[i, 'self'] )

    def load_Account_templates( self ):

        self.Account_template_modules = {}
        for P in kabbes_account_manager.templates_Dir.list_contents_Paths( block_dirs = True, block_paths = False ):

            if P.root != '__init__' and P.root != 'BaseAccount':
                type = P.root #CreditCard
                module = ps.import_module_from_path( P.p )

                self.Account_template_modules[ type ] = module

    def setup_encryption( self ):

        RSA_inst = cryp.RSA()
        RSA_inst.import_public_Key(  self.M.cfg['keys.public.Path'],  set = True )
        RSA_inst.import_private_Key( self.M.cfg['keys.private.Path'], set = True )
        self.Combined = cryp.Combined( RSA = RSA_inst, Dir = self.M.cfg['Dir'] )

    def _import_from_json( self, json_string ):

        dictionary = ps.json_to_dict( json_string )
        self._import_from_dict( dictionary )

    def _import_from_dict( self, dictionary ):
        
        for Acc_id in dictionary:
            account_dictionary = dictionary[Acc_id]
            self.make_Account( account_dictionary['type'], dictionary = account_dictionary)

    def _import_from_Dir( self, is_empty ):

        if is_empty:
            json_string = "{}"

        else:
            self.Combined.Dir = self.M.cfg['Dir']
            json_string = self.Combined.decrypt().decode( kabbes_account_manager.ENCODING )

        self._import_from_json( json_string )

    def export_to_json( self ):

        dictionary = self.export_to_dict()
        return ps.dict_to_json( dictionary )

    def export_to_dict( self ):

        d = {}
        for Acc in self:
            d.update( Acc.export_to_dict() )

        return d

    def export_to_Dir( self ):

        json_string = self.export_to_json()
        self.Combined.encrypt( json_string.encode( kabbes_account_manager.ENCODING ) )

    def get_Dir_user( self ):

        if not self.M.cfg['remote.accounts.Dir'].exists():
            self.M.cfg['remote.accounts.Dir'].create()

        # first, see if the user gave us something to use
        if self.M.cfg.get_node('Dir').get_value() == None:
            if self.M.cfg.get_node('database_name').get_value() != None:
                self.M.cfg.get_node('Dir').set_value( self.M.cfg['remote.accounts.Dir'].join_Dir( path = self.M.cfg['database_name'] ) )

        # now, check if Dir has been defined and is usable
        if self.M.cfg.get_node('Dir').get_value() != None:
            if not self.M.cfg['Dir'].exists():
                self.M.cfg.get_node( 'Dir' ).set_value( None )

        # if we still have to setup the Dir
        if self.M.cfg.get_node('Dir').get_value() == None:

            possible_Dirs = self.M.cfg['remote.accounts.Dir'].list_contents_Paths( block_dirs = False, block_paths = True )

            if len(possible_Dirs) > 0:

                Dir = ps.get_selection_from_list( possible_Dirs )
                self.M.cfg.get_node('Dir').set_value( Dir ) 
                return False

            else:
                print ('No options for data found in ' + str(self.M.cfg['remote.accounts.Dir']))
                new_root = input( 'Enter a new folder name ' + str(self.M.cfg['remote.accounts.Dir']) + '/' )
                self.M.cfg.get_node('Dir').set_value( self.M.cfg['remote.accounts.Dir'].join_Dir( path=new_root ) )
                self.M.cfg['Dir'].create()
                return True

        return False

    def _add_Account( self, new_Account ):

        self._add( new_Account.get_id(), new_Account )

    def delete_Account( self, Acc_inst ):

        self._remove( Acc_inst.get_id() )

    def make_Account( self, type, **kwargs ):

        account_template_module = self.Account_template_modules[ type ]
        new_Account = account_template_module.construct( self, **kwargs )
        self._add_Account( new_Account )
        return new_Account

    def make_Account_user( self ):

        type = self.get_Account_type_user()
        new_Account = self.make_Account( type )
        new_Account.Entries.make_Entry_user()

    def export_non_encrypted( self ):

        json_string = self.export_to_json()
        self.M.cfg['decrypted_export.Path'].write( string=json_string )

    def backup( self ):

        self.export_to_Dir()
        self.M.cfg['Dir'].copy( Destination = self.M.cfg['backup.Dir'], overwrite = True )

    def get_Account_type_user( self ):

        '''return the user's selection of Account type (CreditCard, Online, etc) '''

        ps.print_for_loop( list(self.Account_template_modules.keys()) )
        ind = ps.get_int_input( 1, len(self.Account_template_modules), prompt = 'Choose your Account Template' ) - 1
        return list( self.Account_template_modules.keys() )[ ind ]

    def pre_run( self ):
        self.sort()

    def exit( self ):
        self.export_to_Dir()
