from kabbes_account_manager.AccountTemplates.BaseAccount import BaseAccount

def construct( *args, **kwargs ):

    return CreditCard( *args, **kwargs )

class CreditCard( BaseAccount ):

    OTHER_MAND_ENTRIES = [ 'Card Number','CVV','Expiration Date' ]
    OTHER_DICTIONARY = {
        'entry_to_copy': 'Card Number'
    }

    def __init__( self, *args, **kwargs ):

        BaseAccount.__init__( self, *args, **kwargs )
