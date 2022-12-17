import py_starter as ps
args, kwargs = ps.get_system_input_arguments()

from kabbes_account_manager import Accounts
Accs = Accounts( *args, **kwargs )
Accs.run()
