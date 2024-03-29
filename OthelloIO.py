"""
    OthelloZero: OthelloIO
    Author: Caleb Spradlin
    Date: 27/09/19
    This file contains basic helper functions that deal with string and int conversions to satisy the board games in out functions 
"""

def get_col_char(col):
    """ Convert 1, 2, etc. to 'a', 'b', etc. """
    #print("1st Taking in", col, "putting out", chr(ord('a')+col))
    return chr(ord('a')+col)

def get_char_col(inp):
    """ Convert substring 'a', 'b', 'c', to 0,1,2, etc. """
    #print("2nd Taking in", inp, "putting out", (ord(inp)-ord('a')))
    return ord(inp)-ord('a')

def split_string(inp):
    """Splits string based on substring ' ' """
    return inp.split(" ")
