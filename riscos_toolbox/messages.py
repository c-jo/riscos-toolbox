from types import Point
import swi
import ctypes
import struct

class UserMessage(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_uint32),
        ("sender", ctypes.c_uint32),
        ("my_ref", ctypes.c_uint32),
        ("your_ref", ctypes.c_uint32),
        ("code", ctypes.c_uint32) ]

    def __init__(self, code, length=None):
        self.length = length if length else ctypes.sizeof(self)
        self.code = code

    def from_pollblock(self, poll_block):
        length = poll_block[0]
        if length > ctypes.sizeof(self) or length % 4 != 0:
            raise(ValueError("invalid Length in bloxk"))
        dst = ctypes.cast(
                ctypes.pointer(self), ctypes.POINTER(ctypes.c_uint32))
        for w in range(0, length//4):
            dst[w] = poll_block[w]

    def from_block(self, data):
        if len(data) < 20:
            raise(ValueError("Incomplete message header"))

        length, code = struct.unpack("I12xI", data[0:20])

        if code != self.__class__._code:
            raise(ValueError("block data isn't for this message"))

        if length < 20 or length > ctypes.sizeof(self) or length % 4 != 0:
            raise(ValueError("invalid length in block"))

        dst = ctypes.cast(
                ctypes.pointer(self), ctypes.POINTER(ctypes.c_ubyte))
        for b in range(0, length):
            dst[b] = data[b]

class DataSave(UserMessage):
   _code = 1
   _fields_ = [
        ("window_handle", ctypes.c_int32),
        ("icon_handle", ctypes.c_int32),
        ("screen", Point),
        ("estimated_size", ctypes.c_uint32),
        ("filetype", ctypes.c_uint32),
        ("_filename", ctypes.c_char*212) ]

   def __init__(self):
       super().__init__(DataSave._code)

   @property
   def filename(self):
        return self._filename

   @filename.setter
   def filename(self, newname):
       self._filename = newname+b'\0'
       self.length = 44 + (len(self._filename)+3)//4*4

if __name__ == "__main__":
    data = struct.pack("IIIIIIiiiII12s", 56, 0x1234, 0x1000, 0x1001, 1,
    4, 5, 500, 600, 4096, 0xffd, b"TestFile")
    print(len(data))

    ds = DataSave()
    ds.from_block(data)
    print(ds.length)

    print(hex(ds.my_ref))
    print(ds.filename)
    print(ds.length)
    ds.filename = b"ADFS::HardDisc4.$.Foo"
    print(ds.length)

