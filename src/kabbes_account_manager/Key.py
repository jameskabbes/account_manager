from kabbes_account_manager import Key_Value_Base

class Key( Key_Value_Base ):

    def __init__(self, *args, **kwargs ):

        self.prompt_string = 'Key: '

        Key_Value_Base.__init__( self, *args, **kwargs )

        if self.val in self.Entry.Entries.Account.IMMUTABLE_ENTRY_KEYS:
            self.can_edit = False

    def get_val( self, autocomplete = True, **kwargs ):

        while True:

            prev_key_values = [ Entry.Key.val for Entry in self.Entry.Entries ]

            if autocomplete:
                self.get_autocompleted_val()
            else:
                self.raw_input_val()

            if self.val not in prev_key_values:
                break

            else:
                print ('That key already exists')
