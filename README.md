# Phonon-Explorer
Phonons at your fingertips

Issues:
create working branch
cleanup all unused files on master branch
  --delete InputParameters.json
"^M" line endings in .txt file - ms/dos
     - ran dos2unix on InputParameters.txt to cleanup endings.  Issue or not?
paths need to be updated in 2 places:
      - RSE_Constants - lines 18 and 40
      - InputParameters.txt - lines 17, 19, 25, 26, 44, 80, 85	
Encoding needs to be specified as utf-8.  Dont use Windows 1251 encodings
	 - specifically quotes, 0x93 byte doesnt exist in utf-8, 0x22 i believe.
	 - .open(..., 'encoding=cp1251')
	 - this has to be worked out for python2.7 and python3.6

Errors Encountered on Running

Command: python3.6 GenerateConstQCuts.py

[asquiggle@cu-engr2-1-14-10 Python Code]$ python3.6 GenerateConstQCuts.py
Traceback (most recent call last):
  File "GenerateConstQCuts.py", line 21, in <module>
    params=Parameters(RSE_Constants.INPUTS_PATH, RSE_Constants.INPUTS_FILENAME)
  File "/home/asquiggle/Phonon-Explorer/Python Code/TextFile.py", line 35, in __init__
    parameters = f.read().splitlines()
  File "/usr/lib64/python3.6/codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x93 in position 3161: invalid start byte

CURRENT ERROR:

[asquiggle@cu-engr2-1-14-10 Python Code]$ python3.6 GenerateConstQCuts.py
Traceback (most recent call last):
  File "GenerateConstQCuts.py", line 28, in <module>
    testData.Generate()
  File "/home/asquiggle/Phonon-Explorer/Python Code/Data.py", line 325, in Generate
    Qs=np.genfromtxt(self.params.path_InputFiles+self.params.textfile_for_selectedQs)
  File "/usr/local/lib64/python3.6/site-packages/numpy/lib/npyio.py", line 1700, in genfromtxt
    fhd = iter(np.lib._datasource.open(fname, 'rt', encoding=encoding))
  File "/usr/local/lib64/python3.6/site-packages/numpy/lib/_datasource.py", line 262, in open
    return ds.open(path, mode, encoding=encoding, newline=newline)
  File "/usr/local/lib64/python3.6/site-packages/numpy/lib/_datasource.py", line 618, in open
    raise IOError("%s not found." % path)
OSError: /home/asquiggle/Phonon-Explorer/Input_FilesMantidTest.txt not found.