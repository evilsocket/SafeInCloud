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
import struct
import StringIO
import zlib

from Crypto.Cipher import AES
from passlib.utils import pbkdf2

class Decrypter:
    def __init__( self, db_filename, password ):
        self.db_filename = db_filename
        self.password    = password
        self.input       = None

    def __read_byte(self, fd = None):
        if fd is None:
            fd = self.input
        return struct.unpack( 'B', fd.read(1) )[0]

    def __read_short(self):
        return struct.unpack( 'H', self.input.read(2) )[0]

    def __read_bytearray(self, fd = None):
        if fd is None:
            fd = self.input
        size = self.__read_byte(fd)
        return struct.unpack( "%ds" % size, fd.read( size ) )[0]

    def __derive( self, password, salt, iters = 10000 ):
        return pbkdf2.pbkdf2( password, salt, iters, 32 )

    def decrypt( self ):
        #print "@ Decrypting %s ..." % self.db_filename

        self.input = open( self.db_filename, 'rb' )

        magic  = self.__read_short()
        sver   = self.__read_byte()
        salt   = self.__read_bytearray()

        # print "  - [PBKDF2] Deriving first key ..."

        skey   = self.__derive( self.password, salt )
        iv     = self.__read_bytearray()
        cipher = AES.new( skey, AES.MODE_CBC, iv )
        salt2  = self.__read_bytearray()
        block  = self.__read_bytearray()
        decr   = cipher.decrypt(block)
        sub_fd = StringIO.StringIO(decr)
        iv2    = self.__read_bytearray( sub_fd )
        pass2  = self.__read_bytearray( sub_fd )
        check  = self.__read_bytearray( sub_fd )

        # print "  - [PBKDF2] Deriving second key ..."

        skey2  = self.__derive( pass2, salt2, 1000 )
        cipher = AES.new( pass2, AES.MODE_CBC, iv2 )
        data   = cipher.decrypt( self.input.read() )

        # print "@ Decompressing ..."
        decompressor = zlib.decompressobj()
        return decompressor.decompress(data) + decompressor.flush()


    def decrypt_to_file( self, output ):
        data = self.decrypt()
        od = open( output, 'w+t' )
        od.write( data )
        od.close()
