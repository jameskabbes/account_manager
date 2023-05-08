import kabbes_account_manager
import kabbes_password_creator

class Manager( kabbes_account_manager.Base ):

   
    def __init__( self, **kwargs ):

        kabbes_account_manager.Base.__init__( self, **kwargs )

        self.Accounts = kabbes_account_manager.Accounts( self )
        self.PasswordManager = kabbes_password_creator.Client()
        self._Children = [ self.Accounts ]

