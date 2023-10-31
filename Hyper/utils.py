import swi
import ctypes

# Load a file and decompress it if it's squashed
def file_load(filename):
    SQSH = 0x48535153

    size = swi.swi("OS_File", "Is;....I", 17, filename)
    buffer = (ctypes.c_byte * size)()
    swi.swi("OS_File", "isI0", 16, filename, ctypes.addressof(buffer))

    if size > 20:
        header = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint32))
        if header[0] == SQSH:
             sq_size = size
             squashed = buffer

             size = header[1]
             buffer = (ctypes.c_byte * size)()

             ws_size = swi.swi("Squash_Decompress", "II;I", 8, sq_size-20)
             workspace = (ctypes.c_byte * ws_size)()

             swi.swi("Squash_Decompress", "iIIIII", 4,
                     ctypes.addressof(workspace),
                     ctypes.addressof(squashed)+20,
                     sq_size-20,
                     ctypes.addressof(buffer), size)

    return buffer, size

if __name__ == "__main__":
    print(file_load("underlay"))
