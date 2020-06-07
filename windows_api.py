import ctypes

# Title of messagebox; text; style- 0 is OK, 1 is OK/CANCEL, itd.
def windows_message(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

