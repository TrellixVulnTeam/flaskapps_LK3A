#!/usr/bin/python3
import os
import sys
if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'pybabel'
if len(sys.argv) != 2:
    print("usage: tr_init <language-code>")
    sys.exit(1)
try:
    os.unlink('titanembeds/translations/messages.pot')
except:
    pass
os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o titanembeds/translations/messages.pot titanembeds')
os.system(pybabel + ' init -i titanembeds/translations/messages.pot -d titanembeds/translations -l ' + sys.argv[1])