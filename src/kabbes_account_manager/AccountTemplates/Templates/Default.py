from kabbes_account_manager.AccountTemplates.BaseAccount import BaseAccount

def construct( *args, **kwargs ):

    return Default( *args, **kwargs )

class Default( BaseAccount ):

    OTHER_MAND_ENTRIES = [ 'password' ]
    OTHER_DICTIONARY = {
        'entry_to_copy': 'password'
    }

    def __init__( self, *args, **kwargs ):

        BaseAccount.__init__( self, *args, **kwargs )
