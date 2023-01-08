import kabbes_account_manager
import kabbes_user_client
import kabbes_password_creator

class Manager( kabbes_account_manager.Base ):

    _CONFIG = {
        "_Dir": kabbes_account_manager._Dir,
        "_repo_Dir": kabbes_account_manager._repo_Dir,
        "Dir": None
    }

    cfg = kabbes_user_client.Client( dict=_CONFIG ).cfg

    def __init__( self, **kwargs ):

        kabbes_account_manager.Base.__init__( self, **kwargs )
        self.Accounts = kabbes_account_manager.Accounts( self )
        self.PasswordManager = kabbes_password_creator.Client()
        self._Children = [ self.Accounts ]

