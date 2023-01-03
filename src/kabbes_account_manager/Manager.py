import kabbes_account_manager
import kabbes_config
import kabbes_password_creator

class Manager( kabbes_account_manager.Base ):

    _OVERRIDE_OPTIONS = {
        1: ["Open Accounts", "run_Child_user"]
    }

    _DEFAULT_CONFIG = {
        "Dir": None
    }

    def __init__( self, **override_settings ):
        kabbes_account_manager.Base.__init__( self )

        config = kabbes_config.Config( **self._DEFAULT_CONFIG )
        self.cfg = kabbes_config.load_Config( kabbes_account_manager.DEFAULT_CONFIG_PATH, config=config )
        self.cfg.load_dict( override_settings )

        self.Accounts = kabbes_account_manager.Accounts( self )
        self.PasswordManager = kabbes_password_creator.Manager()
        self._Children = [ self.Accounts ]

