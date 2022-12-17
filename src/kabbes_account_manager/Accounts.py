from parent_class import ParentPluralDict
import kabbes_account_manager
from kabbes_account_manager import Base, Key_Value_CRTI
import py_starter as ps
import pandas as pd
import dir_ops as do
import kabbes_cryptography as cryp

class Accounts( ParentPluralDict, Base ):

    DEFAULT_ATT_VALUES = {
    'Dir': None,
    'database_name': None,
    'cwd_dir': do.get_cwd()
    }

    _OVERRIDE_OPTIONS = {
    1: [ 'Open Account', 'open_Account_user' ],
    2: [ 'Make Account', 'make_Account_user'],
    5: [ 'Export non-encrypted', 'export_non_encrypted' ],
    6: [ 'Backup Accounts', 'backup' ]
    }

    MAX_PRINT_LENGTH = 10

    def __init__(self, **kwargs ):

        ParentPluralDict.__init__( self, 'Accounts' )
        Base.__init__( self, **kwargs )

        #
        self._cwd_Dir = do.Dir( self.cwd_dir )

        self.file_input_Path = self._cwd_Dir.join_Path( path = 'file_input.txt' ) 
        if not self.file_input_Path.exists():
            self.file_input_Path.create( override = True )

        settings_Path = self._cwd_Dir.join_Path( path = 'settings.json' )
        if settings_Path.exists():
            new_Settings = ps.Settings( **ps.json_to_dict(settings_Path.read()) )
            kabbes_account_manager.Settings = kabbes_account_manager.Settings.merge( new_Settings )

        self.Key_Value_CRTI = Key_Value_CRTI( self )

        #
        self.local_credentials_Dir =  self._cwd_Dir.join_Dir( path = kabbes_account_manager.Settings.local_credentials.rel_dir )
        self.backup_accounts_Dir =    self.local_credentials_Dir.join_Dir( path = kabbes_account_manager.Settings.local_credentials.backup_accounts_dir )
        self.private_Key_Path =       self.local_credentials_Dir.join_Path( path = kabbes_account_manager.Settings.local_credentials.private_key_filename )

        self.remote_credentials_Dir = self._cwd_Dir.join_Dir( path = kabbes_account_manager.Settings.remote_credentials.rel_dir )
        self.remote_accounts_Dir =    self.remote_credentials_Dir.join_Dir( path = kabbes_account_manager.Settings.remote_credentials.accounts_dir )
        self.public_Key_Path =        self.remote_credentials_Dir.join_Dir( path = kabbes_account_manager.Settings.remote_credentials.public_key_filename )

        self.non_encrypted_export_Path = self.local_credentials_Dir.join_Path( path = 'non_encrypted_export.json' )


        #
        self.load_Account_templates()

        #
        is_empty = self.get_Dir_user()
        self.backup_Dir = self.backup_accounts_Dir.join_Dir( path = self.Dir.dirs[-1] )
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
        RSA_inst.import_public_Key( self.public_Key_Path, set = True )
        RSA_inst.import_private_Key( self.private_Key_Path, set = True )
        self.Combined = cryp.Combined( RSA = RSA_inst, Dir = self.Dir )

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
            self.Combined.Dir = self.Dir
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

        if not self.remote_accounts_Dir.exists():
            self.remote_accounts_Dir.create()

        # first, see if the user gave us something to use
        if self.Dir == None:
            if self.database_name != None:
                self.Dir = do.Dir( self.remote_accounts_Dir.join( self.database_name ) )

        # now, check if Dir has been defined and is usable
        if self.Dir != None:
            if not self.Dir.exists():
                self.Dir = None

        # if we still have to setup the Dir
        if self.Dir == None:

            possible_Dirs = self.remote_accounts_Dir.list_contents_Paths( block_dirs = False, block_paths = True )

            if len(possible_Dirs) > 0:

                ind = 0
                if len(possible_Dirs ) > 1:

                    filenames = [ D.dirs[-1] for D in possible_Dirs ]
                    ps.print_for_loop( filenames )
                    ind = ps.get_int_input( 1, len(filenames), prompt = 'Select your Account catalog: ' ) - 1

                self.Dir = possible_Dirs.Objs[ ind ]
                return False

            else:
                print ('No options for data found in ' + str(self.remote_accounts_Dir))
                new_root = input( 'Enter a new folder name ' + str(self.remote_accounts_Dir.p) + '/' )
                self.Dir = do.Dir( self.remote_accounts_Dir.join( new_root ) )
                self.Dir.create()
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

    def open_Account( self, Acc_inst ):

        Acc_inst.run()

    def open_Account_user( self ):

        Accs = list(self)
        Accs.reverse()

        ps.print_for_loop( [ Acc.display() for Acc in Accs ] )
        ind = ps.get_int_input( 1, len(self), prompt = 'Select your Account: ', exceptions = [''] )
        if ind == '':
            return

        self.open_Account( Accs[ ind-1 ] )

    def export_non_encrypted( self ):

        json_string = self.export_to_json()
        ps.write_text_file( self.non_encrypted_export_Path.p, string = json_string )

    def backup( self ):

        self.export_to_Dir()
        self.Dir.copy( Destination = self.backup_Dir, overwrite = True )

    def get_Account_type_user( self ):

        '''return the user's selection of Account type (CreditCard, Online, etc) '''

        print ()
        ps.print_for_loop( list(self.Account_template_modules.keys()) )
        ind = ps.get_int_input( 1, len(self.Account_template_modules), prompt = 'Choose your Account Template' ) - 1
        return list( self.Account_template_modules.keys() )[ ind ]

    def run_RTI_choice( self, Acc_inst ):

        Acc_inst.run()

    def pre_run( self ):
        self.sort()

    def exit( self ):

        self.export_to_Dir()
