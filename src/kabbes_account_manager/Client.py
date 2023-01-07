import kabbes_account_manager
import kabbes_user_client
import kabbes_password_creator

class Client( kabbes_account_manager.Base, kabbes_user_client.Client ):

    _OVERRIDE_OPTIONS = {
        "1": ["Open Accounts", "run_Child_user"]
    }

    _CONFIG = {
        "_Dir": kabbes_account_manager._Dir,
        "_repo_Dir": kabbes_account_manager._repo_Dir,
        "Dir": None
    }

    def __init__( self, **kwargs ):

        kabbes_user_client.Client.__init__( self, **kwargs )
        kabbes_account_manager.Base.__init__( self )
        self.Accounts = kabbes_account_manager.Accounts( self )
        self.PasswordManager = kabbes_password_creator.Client()
        self._Children = [ self.Accounts ]



        # "path": "{{cwd.Dir}}/{{package_name}}.json",