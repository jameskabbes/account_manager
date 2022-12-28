import kabbes_account_manager
import kabbes_settings
import dir_ops as do

class Manager( kabbes_account_manager.Base ):

    _OVERRIDE_OPTIONS = {
        1: ["Open Accounts", "run_Child_user"]
    }

    _DEFAULT_SETTINGS = {
        "_cwd_Dir": do.Dir( do.get_cwd() ),
        "Dir": None
    }

    def __init__( self, **override_settings ):
        kabbes_account_manager.Base.__init__( self )

        settings = kabbes_settings.Settings( **self._DEFAULT_SETTINGS )
        self.s = kabbes_settings.load_Settings( kabbes_account_manager.DEFAULT_SETTINGS_PATH, settings=settings )
        self.s.load_dict( override_settings )


        self.Accounts = kabbes_account_manager.Accounts( self )
        self._Children = [ self.Accounts ]
