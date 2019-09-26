def get_col_char(col):
    """ Convert 1, 2, etc. to 'a', 'b', etc. """
    return chr(ord('a')+col)

def get_char_col(inp):
    return ord(inp)-ord('a')
