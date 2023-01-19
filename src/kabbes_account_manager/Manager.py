import kabbes_account_manager
import kabbes_password_creator
import kabbes_client

class Manager( kabbes_account_manager.Base ):

    _BASE_DICT = {
        "_repo_Dir": kabbes_account_manager._repo_Dir,
        "Dir": None
    }


    client = kabbes_client.Package( kabbes_account_manager._Dir, dict = _BASE_DICT )
    cfg = client.cfg
    
    def __init__( self, **kwargs ):

        kabbes_account_manager.Base.__init__( self, **kwargs )

        self.Accounts = kabbes_account_manager.Accounts( self )
        self.PasswordManager = kabbes_password_creator.Client()
        self._Children = [ self.Accounts ]

