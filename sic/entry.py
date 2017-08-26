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
from xml.dom import minidom

class Field:
    def __init__( self, node = None ):
        self.name  = ""
        self.type  = ""
        self.value = ""

        if node is not None:
            self.name  = node.attributes['name'].value
            self.type  = node.attributes['type'].value

            if node.firstChild is not None:
                self.value = node.firstChild.data

class Entry:
    def __init__( self, node ):
        self.title = node.attributes['title'].value
        self.timestamp = int( node.attributes['time_stamp'].value )
        self.fields    = {}

        for field in node.getElementsByTagName('field'):
            field = Field(field)
            self.fields[ field.name ] = field

        for child in node.getElementsByTagName('notes'):
            if child.firstChild is not None:
                field = Field()
                field.name  = 'Notes'
                field.type  = 'notes'
                field.value = child.firstChild.data 
                self.fields['Notes'] = field

    def matches( self, query ):
        if query is None:
            return True

        query = query.lower()
        if query in self.title.lower():
            return True

        return False

