from kabbes_account_manager.AccountTemplates.BaseAccount import BaseAccount

def construct( *args, **kwargs ):

    return Bank( *args, **kwargs )

class Bank( BaseAccount ):

    OTHER_MAND_ENTRIES = [ 'routing' ]
    OTHER_DICTIONARY = {
        'entry_to_copy': 'routing'
    }

    def __init__( self, *args, **kwargs ):

        BaseAccount.__init__( self, *args, **kwargs )
