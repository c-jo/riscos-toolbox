# Fake SWI

import sys
import types


class SWIModule:

    @classmethod
    def swi(cls, *args):
        pass

    class block:
        def __init__(self, *args):
            pass


mod_fakeswi = types.ModuleType('fakeswi', 'Fake swi python module')

# Poke in the functions and classes into the faked swi module
for attr_name in dir(SWIModule):
    if attr_name[0] != '_':
        # print("Promoting into swi module: {}".format(attr_name))
        setattr(mod_fakeswi, attr_name, getattr(SWIModule, attr_name))

sys.modules['swi'] = mod_fakeswi
