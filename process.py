# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

from  docx import  Document
from  docx.shared import  Pt
from  docx.oxml.ns import  qn
from docx.shared import Inches
import re
import codecs
import sys,getopt

pattern =re.compile(u"[\u4e00-\u9fa5]+")
pattern_digit=re.compile(r'[\d]+')
pattern1=re.compile(r'\^|\•|\…|\_|\.|\:|\'|\”|\"|\，|\-|\■|\—|\：|[A-Z]|\~|[a-z]')


def process_original_text(path):
    file = Document(path)
    all_text=''
    count=0
    for p in file.paragraphs:
        text=p.text.encode("UTF-8")
        if '重大飞行' in text:
            print 'find it'
        print text
        if len(text)<=2:
            continue
        text=text.replace('〇','0')
        text=text.replace('i','1')
        text=text.replace('（','(')
        text=text.replace('）',')')
        text=pattern1.sub('',text)
        assignNumberForLine(text.split())

def assignNumberForLine(line):
    unassigned=''
    for item in line:
        result=re.split('[\(]*(\d+)[\)]*',item)
        
        for w in result:
            if len(w)<1:
                continue
            if w.isdigit()==False:
                if unassigned!='':
                    unassigned=unassigned+w
                else:
                    unassigned=w
                    continue
            else:
                if unassigned=='':
                    continue
                print ">"+unassigned,w
                unassigned=''

    if unassigned!='':
        print ">"+unassigned
    print "------------------------------"



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
    print inputfile,outputfile
    f_handler=open(outputfile,'w')
    sys.stdout=f_handler
    process_original_text(inputfile)
