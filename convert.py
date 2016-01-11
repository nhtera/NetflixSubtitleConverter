import os
import time
import sys
if sys.version_info[0] > 2:
    # py3k
    pass
else:
    # py2
    import codecs
    import warnings
    def open(file, mode='r', buffering=-1, encoding=None,
             errors=None, newline=None, closefd=True, opener=None):
        if newline is not None:
            warnings.warn('newline is not supported in py2')
        if not closefd:
            warnings.warn('closefd is not supported in py2')
        if opener is not None:
            warnings.warn('opener is not supported in py2')
        return codecs.open(filename=file, mode=mode, encoding=encoding,
                    errors=errors, buffering=buffering)

DFXPstart = u"""<?xml version="1.0" encoding="UTF-8"?>
<tt xml:lang='en' xmlns='http://www.w3.org/2006/10/ttaf1' xmlns:tts='http://www.w3.org/2006/10/ttaf1#style'>
<head>
      <styling>
            <style id="b1" tts:fontSize="14" tts:fontWeight="normal" tts:fonfFamily="verdana" tts:color="#ffffff"/>
      </styling>
</head>
<body>
    <div xml:lang="en" xml:id="captions" style="b1">
"""
DFXPend = u"""    </div>\n</body>\n</tt>"""
p = u"""            <p begin="{0}" end="{1}">{2}</p>
"""
directory = ""

def main():
    cwd = os.getcwd()
    if len(sys.argv) == 2:
        directory = sys.argv[1]
        if os.path.exists(directory):
            srt(directory)
        else:
            print "\nCould not find path."
    if len(sys.argv) < 2:
        print "\nCurrent directory: "+cwd
        srt(cwd)
    print "\nProgram will exit in 5 seconds"
    time.sleep(5)
    
def srt(directory):
    times = ""
    begin = ""
    end = ""
    dialogue = ""
    linenumber = 0
    output = ""
    encoding = "utf-8"
    linestrip = u""
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".srt") and os.path.isfile(file):
                filename = file;
                print "\nFile to convert: "+filename
                filepath = os.path.join(root,file)
                newfilename = filename[:-4]+".dfxp"
                newfilepath = filepath[:-4]+".dfxp"

                encoding = ""
                encodings = ['utf-8', 'utf-16', 'windows-1250', 'windows-1252']
                for e in encodings:
                    try:
                        fh = codecs.open(filepath, 'r', encoding=e)
                        fh.readlines()
                        fh.seek(0)
                    except UnicodeDecodeError:
                        print('got unicode error with %s , trying different encoding' % e)
                    else:
                        encoding = e
                        print('opening the file with encoding:  %s ' % e)
                        break

                f = open(filepath, 'r', encoding=encoding)
                output = open(newfilepath, 'w', encoding="utf-8")

                output.write(DFXPstart)
                for line in f:
                    linestrip = line.strip()
                    if linestrip.isdigit():
                        linenumber = linestrip
                    if not linestrip.isdigit():
                        if "-->" in line:
                            times = line.split("-->")
                            begin = times[0].strip().replace(",", ".")
                            end = times[1].strip().replace(",", ".")
                        elif (line == "\n" or line == "\r\n") and linenumber > 1:
                            dialogue = dialogue.replace("\n","")
                            dialogue = dialogue[:-6]
                            if dialogue:
                                output.write(p.format(begin, end, dialogue))
                                dialogue = ""
                        else:
                            dialogue += linestrip +"<br />"
                output.write(DFXPend)
                output.close()
                f.close()
                print "\nConverted file: "+newfilename
                
main()
