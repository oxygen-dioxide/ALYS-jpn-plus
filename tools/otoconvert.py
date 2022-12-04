#oto.ini转换
#将日文VCV转换为适用于EN VCCV的形式
import os
import sys
import json
import pathlib
import itertools

from typing import List,Set,Dict,Union

#载入otoconvert.json，并生成各音素列表
externaldict=json.load(open(sys.argv[0].replace(".py",".json"),encoding="utf8"))
CValias:Dict[str,str]=externaldict["CValias"]#日文罗马音->假名
Cs:List[str]=externaldict["Cs"]#辅音列表
Valias:Dict[str,str]=externaldict["Valias"]#输出元音记号->输入元音记号
Talias:Dict[str,str]=externaldict["Talias"]#输出尾音记号->输入尾音记号

#oto.ini路径
if(len(sys.argv)==1):#直接启动脚本，则查找脚本所在文件夹的oto-base.ini
    #otopath=os.path.join(os.path.split(sys.argv[0])[0],"oto-base.ini")
    inputpath=pathlib.Path(sys.argv[0]).absolute().parent.joinpath("oto-base.ini")
elif(os.path.isfile(sys.argv[1])):#传入文件名
    inputpath=pathlib.Path(sys.argv[1]).absolute()
else:#传入路径
    inputpath=pathlib.Path(sys.argv[1]).absolute().joinpath("oto-base.ini")
#音阶后缀
suffix=inputpath.parent.name

#载入oto.ini
inputdict={}#条目名称->对应的oto条目
for line in open(inputpath,encoding="utf-8").readlines():
    linecontent=line.replace("=",",").split(",")
    if(linecontent[1].endswith(suffix)):#删除音高后缀
        linecontent[1]=linecontent[1][:-len(suffix)]
    #print(linecontent)
    for i in [2,3,4,5,6]:
        linecontent[i]=float(linecontent[i])
    inputdict[linecontent[1]]=linecontent


#开始转换条目
outputdict={}
#VCV
#输入格式："V CValia"
print("====VCV====")
for (CV_prev,CV) in itertools.product(CValias,CValias):
    V=CV_prev[-1]
    VCVotokey=Valias.get(V,V)+" "+CValias.get(CV,CV)
    if(VCVotokey in inputdict):
        outputdict[CV_prev+" "+CV]=inputdict[VCVotokey]
    else:
        print(VCVotokey+" 缺失")
#VT
#输入格式："VT"
print("====VT====")
for (CV_prev,T) in itertools.product(CValias,Talias):
    V=CV_prev[-1]
    VTotokey=Valias.get(V,V)+Talias.get(T,T)
    if(VTotokey in inputdict):
        outputdict[CV_prev+" "+T]=inputdict[VTotokey]
#HCV
#输入格式："- CValia"
print("====HCV====")
for CV in CValias:
    HCVotokey="- "+CValias.get(CV,CV)
    if(HCVotokey in inputdict):
        outputdict["- "+CV]=inputdict[HCVotokey]

#输出oto文件
with inputpath.parent.joinpath("oto.ini").open("w",encoding="utf8") as outputfile:
    for (key,otoline) in outputdict.items():
        #print(otoline)
        otoline[1]=key+suffix
        otoline=[str(i) for i in otoline]
        outputfile.write("{}={}\n".format(otoline[0],",".join(otoline[1:])))

import yaml

#symbols部分（音素定义）：
symbols_set:Dict[str,str]=dict()# symbol=>type
#C
for C in Cs:
    symbols_set[C]="fricative"
#V
for V in Valias:
    symbols_set[V]="vowel"
#CV
for CV in CValias:
    symbols_set[CV]="vowel"
symbols:List[Dict[str,str]]=[{"symbol":i,"type":j} for (i,j) in symbols_set.items()]

#entries部分（单词定义）
entries_set:Dict[str,List[str]]={}
#常规CV，不包含鼻音N M G J
for (romaji,kana) in CValias.items():
    entries_set[kana]=[romaji]
    entries_set[romaji]=[romaji]
#C
for C in Cs:
    entries_set[C]=[C]
for V in Valias:
    entries_set[V]=[V]
entries:List[Dict[str,Union[str,List[str]]]]=[{"grapheme":i,"phonemes":j} for (i,j) in entries_set.items()]
yaml.dump(
    {"symbols":symbols,"entries":entries},
    open("arpasing.yaml","w",encoding="utf8"),
    allow_unicode=True)