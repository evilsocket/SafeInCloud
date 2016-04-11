# This file is part of SafeInCloud database manipulation project.
#
# Copyright(c) 2016 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
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

from sic.decrypter import Decrypter

if len(sys.argv) < 4:
    print "Usage: %s DATABASE PASSWORD OUTPUT" % sys.argv[0]
    exit()

db = Decrypter( sys.argv[1], sys.argv[2] )
db.decrypt_to_file( sys.argv[3] )
