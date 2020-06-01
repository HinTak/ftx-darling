# You should really be using this one instead, SERIOUS
# https://gist.github.com/pudquick/ac8f22326f095ed2690e

from ctypes import Structure, POINTER, CDLL, c_char_p, c_int32, create_string_buffer
from ctypes.util import find_library

# We build an opaque object pointer class type to safely handle data without inspecting it
class OpaqueType(Structure):
    pass

OpaqueTypeRef = POINTER(OpaqueType)

# Load up CoreFoundation via C/ctypes to help with string conversion since we don't have
# access to pyObjC's nice magic NS/CF bridging
CF = CDLL(find_library('CoreFoundation'))
CFStringGetLength           = CF.CFStringGetLength
CFStringGetCString          = CF.CFStringGetCString
CFStringGetCString.argtypes = [OpaqueTypeRef, c_char_p, c_int32, c_int32]

# Define a helper function for converting from the CFStringRef to a python string
def pystr(cfstringref):
    str_length = CFStringGetLength(cfstringref) + 1
    str_buff = create_string_buffer(str_length)
    result = CFStringGetCString(cfstringref, str_buff, str_length, 0)
    return str_buff.value

# Load our target framework via ctypes, in this case the 'Metadata' framework
MD = CDLL('/System/Library/Frameworks/CoreServices.framework/Frameworks/Metadata.framework/Versions/A/Metadata')

# The magic: Get a direct reference to the constant within the framework
kMDSPreferencesNameRef = (OpaqueTypeRef).in_dll(MD, 'kMDSPreferencesName')

# Now convert that back to a string
kMDSPreferencesName = pystr(kMDSPreferencesNameRef)

# >>> kMDSPreferencesName
# 'com.apple.SpotlightServer'