# This file is part of SafeInCloud database manipulation project.
#
# Copyright(c) 2016 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import sys
import getpass
import xmltodict

from sic.decrypter import Decrypter

def matches( query, card ):
    try:
        if query is None:
            return True

        query = query.lower()
        if query in card['@title'].lower():
            return True

        for field in card['field']:
            if query in field['@name'].lower():
                return True

            if '#text' in field and query in field['#text'].lower():
                return True
    except:
        pass

    return False

if len(sys.argv) < 2:
    print "Usage: %s DATABASE (search word)" % sys.argv[0]
    exit()

if len(sys.argv) == 3:
    search = sys.argv[2]
else:
    search = None

database = sys.argv[1]
password = getpass.getpass()

if len(sys.argv) == 2:
    database = sys.argv[1]

db = Decrypter( database, password )
data = db.decrypt()
doc = xmltodict.parse(data)

print "\n"

for card in doc['database']['card']:
    if 'label_id' in card and matches( search, card ) :
        title = card['@title']
        print "%s :" % title
        for field in card['field']:
            if '#text' in field:
                print "  %s: %s" % ( field['@name'], field['#text'] )
        print
