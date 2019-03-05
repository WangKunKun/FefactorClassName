#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import getopt


def helpInfo():
    print("----------脚本说明----------")
    print("脚本用于批量修改类名")
    print("脚本可传入四个参数")
    print("1、待处理的文件路径. example-->'./KanManHua'\n2、待修改的pbxproj文件地址 example-->'./KanManHua.xcodeproj/project.pbxproj'\n3、类名前缀 example-->'MHT_'\n4、类名后缀 example-->'_MHT'\n")
    print("其中前三个参数为必传参数 划重点，要考")
    print("----------请开心使用---------")
    print("另脚本支持 -h 操作")

#一开始构思了 14个 后来....
def rule(cn):
    rule_1 = '"' + cn + '.' #引用修改
    rule_2 = '"' + cn + '"' #类名被直接使用
    rule_3 = ':' + cn + ' ' #继承 后续有空格
    rule_4 = ':' + cn + '\n' #类名后面是换行
    rule_5 = ' ' + cn + '<'
    rule_6 = ' ' + cn + '\n' #类名后面是换行
    rule_7 = ' ' + cn + ' '
    rule_8 = ' ' + cn + '('
    rule_9 = '[' + cn + ' '
    rule_10 = '[' + cn + '*'
    rule_11 = '(' + cn + '*'
    rule_12 = ')' + cn + '*'
    rule_13 = ' ' + cn + '*'
    rule_14 = ' ' + cn + '\n'
    rule_15 = '(' + cn + ' '
    rule_16 = ' ' + cn + ';'
    rule_17 = ',' + cn + ' '
    rule_18 = ',' + cn + '*'
    rule_19 = ')' + cn + ' ' 
    rule_20 = ',' + cn + ';'
    rule_21 = ' ' + cn + ','
    rule_22 = '<' + cn + '*' #被当做协议 遵守类
    rule_23 = '<' + cn + ' '
    rule_24 = ',' + cn + ','
    rule_25 = ' ' + cn + ':'
    rule_26 = ':' + cn + '//' #后面跟注释的、、我TM。。
    rule_27 = ' ' + cn + '//' 
    rule_28 = ' ' + cn + '{' #后面跟大括号的··
    rule_29 = ')' + cn + '<' #为什么遵守协议 也用了 实际类名 没有用ID
    rule_30 = '(' + cn + '.' #为什么类要使用.语法
    rule_31 = ' ' + cn + '.'  #类名调用.语法
    rule_32 = '!' + cn + '.'  
    rule_33 = ':' + cn + '.'  #类名调用点语法 被当做参数传入
    rule_34 = '[' + cn + '\n' #类名被换行
    rule_35 = ':' + cn + '<' #继承类名后面 直接接入协议 默认实际是不存在这个问题的  防止人为 以及修改模板
    rule_36 = '"' + cn + '_' #类取名有下划线以及数字 以及通过工厂用数字来创建的情况
    rule_37 = '"' + cn + '%' #类取名有数字 以及通过工厂用数字来创建的情况
    rule_38 = '<' + cn + '>' #协议作为文件名  修改的可能为协议名
    rule_39 = ',' + cn + '>' 
    rule_40 = ' ' + cn + '>' 

    rules = []
    rules.append(rule_1)
    rules.append(rule_2)
    rules.append(rule_3)
    rules.append(rule_4)
    rules.append(rule_5)
    rules.append(rule_6)
    rules.append(rule_7)
    rules.append(rule_8)
    rules.append(rule_9)
    rules.append(rule_10)
    rules.append(rule_11)
    rules.append(rule_12)
    rules.append(rule_13)
    rules.append(rule_14)
    rules.append(rule_15)
    rules.append(rule_16)
    rules.append(rule_17)
    rules.append(rule_18)
    rules.append(rule_19)
    rules.append(rule_20)
    rules.append(rule_21)
    rules.append(rule_22)
    rules.append(rule_23)
    rules.append(rule_24)
    rules.append(rule_25)
    rules.append(rule_26)
    rules.append(rule_27)
    rules.append(rule_28)
    rules.append(rule_29)
    rules.append(rule_30)
    rules.append(rule_31)
    rules.append(rule_32)
    rules.append(rule_33)
    rules.append(rule_34)
    rules.append(rule_35)
    rules.append(rule_36)
    rules.append(rule_37)
    rules.append(rule_38)
    rules.append(rule_39)
    rules.append(rule_40)
    return rules

def pbRule(cn):
    rule_1 = '=' + cn + "."
    rule_2 = ' ' + cn + "."
    rule_3 = '/' + cn + "."
    rule_4 = '"' + cn + "."
    rules = []
    rules.append(rule_1)
    rules.append(rule_2)
    rules.append(rule_3)
    rules.append(rule_4)
    return rules


def getClassNames(filepath):
    #读取文件名入数组
    #过滤文件夹
    filterDirs = ["WKCrashSDK/"]
    #过滤文件
    filterFiles = []
    classNames = []
    #遍历filepath下所有文件，包括子目录
    for root, dirs, files in os.walk(filepath):
        for name in files:
            path = os.path.join(root, name)
            #过滤文件夹
            isFilterDir = 0
            for filterDir in filterDirs:
                if filterDir in path:
                    isFilterDir = 1
                    break
            if isFilterDir != 1:
                if ".m" in name:
                    #过滤main.m文件
                    if name == "main.m":
                        continue
                    splitNames = name.split(".m")
                    if splitNames[1] == "" or splitNames[1] == "m":
                        cn = splitNames[0]
                        #过滤文件
                        isFilterFile = 0
                        for ff in filterFiles:
                            if ff == cn:
                                isFilterFile = 1
                        if isFilterFile != 1:
                            #过滤类目
                            if cn.find("+") == -1:
                                print(cn)
                                classNames.append(cn)
    return classNames




def changePBFile(PBFilePath,classNames,prefix,suffix):
    with open(PBFilePath,"r") as file_read:
        lines = file_read.readlines()
    with open(PBFilePath,"w") as file_write:
        for line in lines:
            for cn in classNames:
                oldRules = pbRule(cn)
                newRules = pbRule(prefix + cn + suffix)
                for x in xrange(0,len(oldRules)):
                    if oldRules[x] in line:
                        line = line.replace(oldRules[x],newRules[x])
                        print(line)
            file_write.write(line) #全部类名遍历完后再写



def changeClassName(filepath,PBFilePath,prefix,suffix=""):


    #读取文件名入数组
    print("-------------------")
    print("-------获取文件名列表-----")
    classNames = getClassNames(filepath)
    print("------需修改类名数量 " + str(len(classNames)) + "-------")
    # 修改文件内容
    # 遍历filepath下所有文件，包括子目录
    print("-------获取完成-----")
    print("-------开始修改文件内容-----")
    for root, dirs, files in os.walk(filepath):
        for name in files:
            ##过滤framework 以及 .a
            oldFilePath = os.path.join(root, name)
            if oldFilePath.find(".framework/") != -1 or oldFilePath.find(".a/") != -1:
                continue;
            ##仅仅处理 .h .m .xib .pch .storyboard
            if name.find(".pch") != -1 or name.find(".h") != -1 or name.find(".m") != -1 or name.find(".xib") != -1 or name.find(".storyboard") != -1:
                print("-------正在处理" + name + "-----")
                #去掉.以及后缀
                splitFileNameArr = name.split('.')
                fileName = splitFileNameArr[0]
                newFileName = prefix + fileName + suffix + "." + splitFileNameArr[1]
                newFilePath = os.path.join(root, newFileName)
                # print(oldFilePath)
                # print(newFilePath)
                with open(oldFilePath,"r") as file_read:
                        lines = file_read.readlines()
                with open(oldFilePath,"w") as file_write:
                    for line in lines:
                        for cn in classNames:
                            oldRules = rule(cn)
                            newRules = rule(prefix + cn + suffix)
                            for x in xrange(0,len(oldRules)):
                                if oldRules[x] in line:
                                    line = line.replace(oldRules[x],newRules[x])
                        file_write.write(line) #全部类名遍历完后再写
                if fileName in classNames:
                    os.rename(oldFilePath,newFilePath)  
    print("-------修改文件内容完成-----")
    # 修改pb文件内容
    print("-------开始修改pb文件-------")
    changePBFile(PBFilePath,classNames,prefix,suffix)
    #修改类名
    print("-------处理pb文件完成--------")

#main
opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
isNeedHelp = 0
filePath = ""
pbPath = ""
prefix = ""
suffix = ""
for o,a in opts:
    if o == '-h' or o == '--help':
        isNeedHelp = 1
        helpInfo()
        os._exit(0)
if isNeedHelp == 0:
    argsCount = len(args)
    if argsCount < 3:
        helpInfo()
        os._exit(0)
    else:
        filePath = args[0]
        filePathExist = os.path.exists(filePath)
        if filePathExist != 1:
            print("error：" + filePath + "不是有效路径")
            os._exit(0)
        pbPath = args[1]
        pbPathExist = os.path.isfile(pbPath)
        if pbPathExist != 1:
            print("error：" + pbPath + "不是有效文件")
            os._exit(0)
        prefix = args[2]
        suffix = ""
        if argsCount > 3:
            suffix = args[3]
        if prefix == "" and suffix == "":
            print("大佬 前缀后缀都为空字符串。。。你是在逗本脚本吗??")
            os._exit(0)
changeClassName(filePath,pbPath,prefix,suffix)

