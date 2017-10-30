# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

from  docx import  Document
from  docx.shared import  Pt
from  docx.oxml.ns import  qn
from docx.shared import Inches
import re
import codecs
import sys,getopt

pattern=re.compile(r'\’|\丨|\^|\•|\…|\_|\.|\:|\'|\”|\"|\，|\-|\■|\—|\：|[A-Z]|\~|[a-z]|\“')
dict={}
former_page_number=[1,1,1,1,1,1,1,1,1,1,1,1]

def save(term,page):

    number=int(page)
    if number in dict:
        if term in dict[number]:
            return
        dict[number].append(term)
    else:
        dict[number]=[]
        dict[number].append(term)


def write_dict():
    for key in sorted(dict):
        for item in dict[key]:
            print item



def process_original_text(path):
    file = Document(path)
    all_text=''
    for p in file.paragraphs:
        text=p.text.encode("UTF-8")
        if len(text)<=2:
            continue
        text=text.replace('〇','0')
        text=text.replace('i','1')
        text=text.replace('（','(')
        text=text.replace('）',')')
        text=text.replace('M','14')
        text=text.replace('I','1')
        text=pattern.sub('',text)
        assignNumberForLine(text.split())

def assignNumberForLine(line):
    count=0
    unassigned=''
    for item in line:
        result=re.split('[\(]*(\d+)[\)]*',item)
        
        for w in result:

            if len(w)<1:
                continue
            if w.isdigit()==False:
                count+=1
                if unassigned!='':
                    '字 字 页码'
                    save(unassigned,former_page_number[count-2])
                    unassigned=w
                else:
                    unassigned=w
                    continue
            else:
                if count==0:
                    continue
                former_page_number[count-1]=w

                if unassigned=='':
                    continue
                else:
                    save(unassigned,w)
                unassigned=''

    if unassigned!='':

        save(unassigned,former_page_number[count-1])



def usage():
    print(u"""
    Usage:
    -h / --help :使用帮助
    -i / --inputfile :输入文件
    -o / --outputfile :输出文件
    例如 python process.py -i IMG_20171027_0001.docx -o hello.txt
    """)

if __name__ == '__main__':
    inputfile=''
    outputfile=''
    try:
        options,args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for opt,arg in options:
        if opt== '-h':
            usage()
            sys.exit()
        elif opt in ('-i','--inputfile'):
            inputfile=arg
        elif opt in ('-o','--outputfile'):
            outputfile=arg
    f_handler=open(outputfile,'w')
    sys.stdout=f_handler
    process_original_text(inputfile)
    write_dict()
