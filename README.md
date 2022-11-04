# NPP Protein Lexer
It can be helpful when looking at a protein sequence to be able to quickly identify
regions that are hydrophilic, acidic, basic, lipophilic, and so on.

Some online tools like [CLUSTAL Omega](https://www.ebi.ac.uk/Tools/msa/clustalo/) have good colorizing, but wouldn't it
be nice to have this kind of highlighting in Notepad++?

![A multiple sequence alignment file after colorizing with protein_lexer.py](/protein_lexer_after.PNG)

I've created a script with the [PythonScript plugin](https://npppythonscript.sourceforge.net/) that colorizes protein files.
Go to that link for info on how to install the plugin.

Once you've installed PythonScript to Notepad++, you can download the attached `protein_lexer.py` and drop it into the
`plugins/PythonScript/scripts` subfolder of your Notepad++ installation's directory.

If you just want to colorize a file without always running the script at startup, you can just run it from the
`Plugins->PythonScript->Scripts` drop-down menu whenever you open a protein file.

You can set the script to run on startup by opening `plugins/PythonScript/scripts/setup.py` and adding two lines
to import protein_lexer. Then you can go to `Plugins->PythonScript->Configuration...` from the main menu and change
the `Initialisation` combo box value to `ATSTARTUP`.

![Change settings to load protein lexer at startup](/settings_load_protein_lexer.PNG)

Once the script runs, it will automatically colorize `fasta` and `clustal_num` files whenever they are opened in the editor.

You can add more file extensions and customize the colors for each type of amino acid by editing `protein_lexer.py`.

The styles are the tuples of three ints in all caps near the top of the file, e.g.

```py
ACID_STYLE = (0xbe, 0, 0) # red
```

and the file extensions are just above that.

By default the colors for amino acids are as follows:

<section>
<li>Acid (D, E): <span style='color:red'>red</span></li>
<li>Amphiphilic (A, C, G, Y): black</li>
<li>Base (K, R): <span style='color:blue'>blue</span></li>
<li>Cyclic (Proline): <span style='color:green'>green</span></li>
<li>Hydrophilic (N, Q, S, T): <span style='color:cyan'>cyan</span></li>
<li>Lipophilic (I, L, M, F, W, V): <span style='color:grey'>grey</span></li>
</section>

Any characters other than the standard one-letter codes will also be colored black.

# TODO

1. Consider only applying styles to large blocks of several (say 8+) contiguous UPPERCASELETTERS. That might reduce performance though.