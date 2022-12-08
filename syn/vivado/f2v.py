#!/usr/bin/python3
from pathlib import Path
import os
def replacepath(old_path):
    if(old_path[0] in ["$"]):
        new_path=Path(os.getenv("PRJ")).joinpath(*Path(old_path).parts[1:])
        return new_path

def casefile(file_in):
    with open(file_in,"r") as fin:
        with open("fpga.f", "a") as fout:
            for line in fin:
                if(line[0:2] in ["//","+l"]):
                    print("info:this is invalid rtl code: "+line)
                elif(line[0:2] in ["+i","-y"]):
            	    print("info:this is include rtl path: "+line)
            	    with open("include_path.txt","a") as include_path:
            	        include_path.write(line)
                elif(line[0:2] in ["-f"]):
                    print("info:this is filelist : "+line)
                    pathenv=Path(line[3:-1]).parts
                    print(pathenv)
                    if(pathenv[0] in ["$PRJ"]):
                        new_path=Path(os.getenv(pathenv[0][1:])).joinpath(*Path(line[3:-1]).parts[1:])
                        casefile(new_path)
                    else:
                        casefile(line[3:-1])
                elif(line[0:2] in ["./","$P"]):
                    print("info:this is valid rtl code :" +line)
                    fout.write(line)    


if __name__=="__main__":
        if(os.path.isfile("fpga.f")):
            os.remove("fpga.f")
        if(os.path.isfile("include_path.txt")):
            os.remove("include_path.txt")
        casefile("test1.f")
