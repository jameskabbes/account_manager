from kabbes_menu import CRTI
from collections import Counter
import pandas as pd

class Key_Value_CRTI( CRTI ):

    def __init__( self, *args, **kwargs ):
        CRTI.__init__( self, *args, **kwargs )

    def search( self, searching_from=None, **kwargs ):

        self.suggestions = []
        if len(self.string) > 1:
            self.suggestions = self.Aself.string_found_in_Children( self.string.lower() )

        # Get unique keys that share the same combos
        if searching_from.type == 'Key':
            
            # First, only keep keys
            self.suggestions = [ s for s in self.suggestions if s.type == 'Key' ]

        # Get unique Value val's that also pertain to the same Keys
        elif searching_from.type == 'Value':

            # First, only keep values
            self.suggestions = [ s for s in self.suggestions if s.type == 'Value' ]

            # Only keep Value's where the corresponding Key val is the same as the one being searched
            self.suggestions = [ s for s in self.suggestions if s.Entry.Key.val == searching_from.Entry.Key.val ]

        ### [ A, B, C, C, B, E, C ] -> [ C, B, A, E ]
        df = pd.DataFrame( {'suggestion': self.suggestions} )
        df[ 'val' ] = df['suggestion'].apply( lambda x: x.val )
        df['count'] = df.groupby('val')['val'].transform('count')
        df.sort_values( 'count', ascending=False, inplace=True )
        df.drop_duplicates( subset='val', keep='first', inplace=True )

        self.suggestions = df['suggestion'].values

