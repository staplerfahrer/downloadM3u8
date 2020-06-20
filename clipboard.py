import ctypes

CF_TEXT = 1
# help here: https://stackoverflow.com/questions/579687/
# how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python
kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def getClipboardText():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            dataLocked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(dataLocked)
            value = text.value
            kernel32.GlobalUnlock(dataLocked)
            return value.decode('utf-8')
    finally:
        user32.CloseClipboard()
    return ''

def emptyClipBoard():
    openClipBoard = ctypes.windll.user32.OpenClipboard
    emptyClipBoard = ctypes.windll.user32.EmptyClipboard
    closeClipBoard = ctypes.windll.user32.CloseClipboard
    openClipBoard(None)
    emptyClipBoard()
    closeClipBoard()

if __name__ == "__main__":
	print(getClipboardText())
