import kabbes_account_manager
from kabbes_account_manager import Key_Value_Base
import kabbes_password_creator.generator_support as pgs

class Value( Key_Value_Base ):

    def __init__(self, *args, **kwargs ):

        ###
        Key_Value_Base.__init__( self, *args, **kwargs )
        ###

        if self.Entry.Key.val in self.Entry.Entries.Account.IMMUTABLE_ENTRY_VALUES:
            self.can_edit = False

    def get_val( self, autocomplete = True ):

        if self.Entry.Key.val == 'password':

            random_key = 'random'
            password = input('Enter the value for password, type "' + random_key + '" for random password:  ')

            if password == random_key:
                password = pgs.word_password()
                print (password)

            self.val = password

        else:
            
            if autocomplete:
                self.get_autocompleted_val()

            else:
                self.raw_input_val()
