# RISC OS Toolbox

Library to use the RISC OS Toolbox in Python.

Hyper contains a python port of the Hyper Toolbox demo application.

Written by Chris Johns, with contributions from Charles Ferguson and Lauren Croney

## Version history

0.1.0 - First public beta release.\
0.2.0 - Bug fixes.\
1.0.0 - Update to the event dispatch system. Added mixins.\
1.0.1 - Bug fixes.\
1.0.2 - Bug fixes.\
1.1.0 - Support more gadgets and objects. Message improvments, Throwback support.

## Future plans

To reduce unexpected calls, handler functions will gain way to specify their match scope. Currently handlers are 
called for the self, parent and ancestor object (unless a previous call has handled it). The default scope of the handlers may change.

To allow for all possible ComponentIDs, and to better handle ObjectIDs the handling of these may need to change.

Better handling of wimp message numbers.

