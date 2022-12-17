from kabbes_account_manager.AccountTemplates.BaseAccount import BaseAccount

def construct( *args, **kwargs ):

    return Online( *args, **kwargs )

class Online( BaseAccount ):

    OTHER_MAND_ENTRIES = [ 'email','username','password' ]
    OTHER_DICTIONARY = {
        'entry_to_copy': 'password'
    }

    def __init__( self, *args, **kwargs ):

        BaseAccount.__init__( self, *args, **kwargs )
