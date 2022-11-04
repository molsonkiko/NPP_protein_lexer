# -*- coding: utf-8 -*-
"""
    A lexer for styling protein sequences based on amino acid type.
    Applies these styles only to files with the extensions shown in FILE_EXTENSIONS.

    Usage:
    Default colors for each amino acid type are below.
    Run script.

    Note: By commenting or deleting everything, including,
    the <comment_or_delete> tags it is ready to be used
    as an additional lexer

"""

from Npp import editor, notepad, LEXER, SCINTILLANOTIFICATION, NOTIFICATION, LANGTYPE # , MESSAGEBOXFLAGS

# the extensions of files to auto-apply styling to
FILE_EXTENSIONS = ['fasta', 'clustal_num']

# colors for aa types
ACID_STYLE = (0xbe, 0, 0) # red
AMPHIPHILIC_STYLE = (0, 0, 0) # black, no special styles
BASE_STYLE = (0, 0, 0xbe) # blue
CYCLIC_STYLE = (0, 0xf6, 0) # green
HYDROPHILIC_STYLE = (0, 0xb0, 0xd0) # cyan
LIPOPHILIC_STYLE = (0x84, 0x84, 0x84) # grey
# numbers for aa types
DEFAULT = 0
ACID_NUM = 50
AMPHIPHILIC_NUM = 51
BASE_NUM = 52
CYCLIC_NUM = 53
HYDROPHILIC_NUM = 54
LIPOPHILIC_NUM = 55

AA_TYPES = {
    'A': AMPHIPHILIC_NUM, # Alanine
    'R': BASE_NUM, # Arginine
    'N': HYDROPHILIC_NUM, # Asparagine
    'D': ACID_NUM, # Aspartic Acid
    'C': AMPHIPHILIC_NUM, # Cysteine
    'E': ACID_NUM, # Glutamic Acid
    'Q': HYDROPHILIC_NUM, # Glutamine
    'G': AMPHIPHILIC_NUM, # Glycine
    'H': BASE_NUM, # Histidine
    'I': LIPOPHILIC_NUM, # Isoleucine
    'L': LIPOPHILIC_NUM, # Leucine
    'K': BASE_NUM, # Lysine
    'M': LIPOPHILIC_NUM, # Methionine
    'F': LIPOPHILIC_NUM, # Phenylalanine
    'P': CYCLIC_NUM, # Proline
    'S': HYDROPHILIC_NUM, # Serine
    'T': HYDROPHILIC_NUM, # Threonine
    'W': LIPOPHILIC_NUM, # Tryptophan
    'Y': AMPHIPHILIC_NUM, # Tyrosine
    'V': LIPOPHILIC_NUM, # Valine
}

def style_it(start, length, STYLE):
    ''' Inform scintilla to do the styling'''
    if length >= 0:
        editor.startStyling(start, 31)
        editor.setStyling(length, STYLE)

try:
    # on first run this will generate an NameError exception
    ProteinLexer().main()
except NameError:

    class ProteinLexerSingleton(type):
        ''' Ensures that only one column lexer instance exists and
            prevents of getting multiple callbacks
        '''
        _instance = None
        def __call__(cls, *args, **kwargs):
            ''' The real constructor and first method called when
                a new instance should be created.
                On first instantiation class variable _instance gets itself assigned,
                every subsequent instantiation try returns this object
            '''
            if cls._instance is None:
                cls._instance = super(ProteinLexerSingleton, cls).__call__(*args, **kwargs)
            return cls._instance

    class ProteinLexer(object):
        ''' A column based lexer implementation.
            Odd and even columns do get different styles assigned.
            Only one separator can be defined.
            Line-based approach - styling takes place when new line has been added
        '''
        __metaclass__ = ProteinLexerSingleton

        DEFAULT = 0 # don't change it

        def __init__(self):
            ''' Register needed callbacks on first class instantiation '''
            editor.callbackSync(self.styleneeded_callback, [SCINTILLANOTIFICATION.STYLENEEDED])
            notepad.callback(self.bufferactivated_callback, [NOTIFICATION.BUFFERACTIVATED])
            # notepad.callback(self.langchanged_callback, [NOTIFICATION.LANGCHANGED])


        def ProteinLexer(self, start_pos, end_pos):
            ''' Main lexing logic.
                Gets called by styleneeded callback
            '''
            og_wrap_mode = editor.getWrapMode()
            # suspends text wrap to improve speed
            editor.setWrapMode(0)
            # first everything will be styled with default style
            style_it(start_pos, end_pos-start_pos, self.DEFAULT)

            # loop over line indexes from start_pos and end_pos
            for ii in range(start_pos, end_pos):
                char = chr(editor.getCharAt(ii))
                style_num = AA_TYPES.get(char)
                if not isinstance(style_num, int):
                    continue
                style_it(ii, 1, style_num)

            # this needs to stay and to be the last line, to signal scintilla we are done.
            editor.startStyling(end_pos,31)
            editor.setWrapMode(og_wrap_mode) # reset text wrap settings

        def init_scintilla(self):
            ''' Initialize configured styles '''
            editor.setMarginWidthN(0,38)
            editor.setMarginWidthN(1,14)
            editor.setMarginWidthN(2,0)

            if editor.getLexer() != LEXER.CONTAINER:
                editor.setLexer(LEXER.CONTAINER)

            editor.styleSetFore(ACID_NUM, ACID_STYLE)
            editor.styleSetFore(AMPHIPHILIC_NUM, AMPHIPHILIC_STYLE)
            editor.styleSetFore(BASE_NUM, BASE_STYLE)
            editor.styleSetFore(CYCLIC_NUM, CYCLIC_STYLE)
            editor.styleSetFore(HYDROPHILIC_NUM, HYDROPHILIC_STYLE)
            editor.styleSetFore(LIPOPHILIC_NUM, LIPOPHILIC_STYLE)
            editor.styleSetFore(DEFAULT, (0, 0, 0)) # white foreground by default
            for num in [0, 50, 51, 52, 53, 54, 55]:
                editor.styleSetBack(num, (0xff, 0xff, 0xff)) # always white background

        def is_lexer_doc(self):
            ''' Check if the current document is of interest
                by seeing if it has a relevant extension.
                See FILE_EXTENSIONS above.
            '''
            fname = notepad.getCurrentFilename()
            for ext in FILE_EXTENSIONS:
                # notepad.messageBox(ext + ' ' + fname, 'ext and filename', MESSAGEBOXFLAGS.OK)
                if fname.endswith('.' + ext):
                    return True
            return False

        def styleneeded_callback(self,args):
            ''' Called by scintilla to inform the lexer
                about the need to style the document.
                If document is of interest call main logic (ProteinLexer) function
                Ensures that the start position is really the first position per line
            '''
            if self.is_lexer_doc():
                startPos = editor.getEndStyled()
                lineNumber = editor.lineFromPosition(startPos)
                startPos = editor.positionFromLine(lineNumber)
                self.ProteinLexer(startPos, args['position'])
                
        def bufferactivated_callback(self, args):
            self.main()

        def main(self):
            ''' Main entry point
                To prevent issues with other lexers document language will
                be set to normal text, then document does get the class name
                property assigned, styles do get initialized and main lexing
                function does get called on whole document
            '''
            if not self.is_lexer_doc():
                return
            notepad.setLangType(LANGTYPE.TXT)
            self.init_scintilla()
            self.ProteinLexer(0, editor.getTextLength())

        # # <comment_or_delete>
        # # just some demo text not really needed by lexer
        # notepad.new()
        # editor.appendText('''>1UBQ_1|Chain A|UBIQUITIN|Homo sapiens (9606)
# MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
# '''
        # )
        # # </comment_or_delete>

    ProteinLexer().main()
