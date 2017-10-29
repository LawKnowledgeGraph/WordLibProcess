# -*- coding: UTF-8 -*- 
#! /usr/local/bin/python

from  docx import  Document
from  docx.shared import  Pt
from  docx.oxml.ns import  qn
from docx.shared import Inches
import re
import codecs

pattern =re.compile(u"[\u4e00-\u9fa5]+")
pattern_digit=re.compile(r'[\d]+')
pattern1=re.compile(r'\^|\•|\…|\_|\.|\:|\'|\”|\"|\，|\-|\…')
path='test.txt'
file_object = open(path, 'a')

def read(path):
    file = Document(path)
    all_text=''
    count=0
    for p in file.paragraphs:
        text=p.text.encode("UTF-8")
        print text
        if len(text)<=2:
            continue
        text=text.replace('〇','0')
        text=text.replace('i','1')
        text=text.replace('（','(')
        text=text.replace('）',')')
        text=pattern1.sub('',text)
        assignNumberForLine(text.split())
        line=''

def assignNumberForLine(line):
    unassigned=''
    for item in line:
        result=re.split('\((\d+)\)',item)
        
        for w in result:
            if len(w)<1:
                continue
            # print w
            # continue
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


def write(text):
    if len(text)<=2:
        return
    file_object.write(text)
    file_object.write('\n')
    # 


if __name__ == '__main__':
    path='./IMG_20171027_0002.docx'
    # process()
    read(path)
    # file_object.close()