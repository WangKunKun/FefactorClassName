####前言
近日由于种种原因，需要把代码里面的类全部都修改一遍类名。

在网上找了一圈相关的开源库，没有发现有合适满意的，始终都存在一些问题，要么出现误修改，要么把方法名或者属性名也给修改了等等情况。

于是决定掏出生疏的Python来写一个。

**批量修改类名需要解决四个问题：**

- 1. 如何取得需要修改的类名？
- 2. 如何修改文件中出现的类名并且不会出现误改等情况？
- 3. 如何修改文件名?
- 4. 修改文件名后，如何同步修改project.pbxproj里面的文件名信息？

####问题一、如何取得需要修改的类名？

#####想法A：

> 由于自己前不久写了一个获取target对应的编译以及资源文件的工具[MacPbxprojHelper](https://github.com/WangKunKun/MacPbxprojHelper)，利用其来获取到target对应的类名写入文件，然后用python来读取文件获取到需要修改的类名，实时上第一版我也是这么做的，但是不够优雅，明明一个脚本能解决的事，为什么需要那么多步操作呢？

#####想法B：
> 利用python直接遍历文件夹获取类名，没错就决定是你了。
其实用python遍历文件实现起来特别简单快捷。但是其中也有可能存在的问题，例如我们的项目中包含有部分资源文件，而资源文件的后缀名是不定的，但是实际我们只需要.m以及.mm结尾的文件前缀作为我们的类名，当然其中包含有类目也需要过滤掉。并且考虑到我们具备一些特殊的需求，需要过滤某些文件甚至某些文件夹下的文件等等。我这边的脚本都有考虑到

实现代码如下：

```
def getClassNames(filepath):
    #读取文件名入数组
    #过滤文件夹
    filterDirs = ["ThirdKit/","小说/"]
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
                    splitNames = name.split(".m")
                    #只选择.m和.mm结尾的文件
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
```

####问题二、如何修改文件中出现的类名并且不出现误改的情况？

在我搜集到的开源的脚本中，有极大比例的一部分是直接通过类名替换，其实这特别容易出现误改。比如我有一个类名为ABC，一个类名为AB，那么ABC就可能出现被修改两次的情况。所以我这边就采用笨办法，先敲定类名出现的场景，根据其场景设定规则，只有出现类名出现在这些规则中时，才去替换，这样就可以保证100%的正确率。（这也是大坑，因为不同的程序员书写习惯的问题，导致规则的定义实际极度繁琐，而且会出现部分遗漏，每一次遗漏后，我都需要添加规则再重跑来验证··）

>下面就是这个脚本最大的贡献·· 自认为基本涵盖完了类名的出现场景（如果有没有涵盖的，请记得一定联系我！！），一共37种规则，**运用这37种规则，做到了一次脚本，既完美修改，无需在动代码就可以直接运行并且不会有闪退问题··**

```
#一开始构思了 14个 后来....
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
    rule_35 = ':' + cn + '<' #继承类名后面 直接接入协议 默认实际是不存在这个问题的
    rule_36 = '"' + cn + '_' #类取名有下划线以及数字 以及通过工厂用数字来创建的情况
    rule_37 = '"' + cn + '%' #类取名有数字 以及通过工厂用数字来创建的情况
```

###问题三、如何修改文件名?

这个问题其实很好解决，利用python的os库就可以直接rename，只是需要拼接全路径。并且在给类文件重命名的时，需要注意前缀和后缀添加的位置，不要添加到.h和.m后面去了即可。

###问题四、如何同步修改project.pbxproj里面的文件信息？

这里又和第二个问题一样需要定义一定规则，才能确保不会出现误替换，但是这个规则和上面比起来简直是小巫见大巫。规则如下：

```
def pbRule(cn):
    rule_1 = '=' + cn + "."
    rule_2 = ' ' + cn + "."
    rule_3 = '/' + cn + "."
    rule_4 = '"' + cn + "."
```

> 以上，问题都解决了。

###使用方式

    ----------脚本说明----------
    脚本用于批量修改类名
    脚本可传入四个参数
    1、待处理的文件路径. example-->'./KanManHua'
    2、待修改的pbxproj文件地址 example--        >'./KanManHua.xcodeproj/project.pbxproj'
    3、类名前缀 example-->'MHT_'
    4、类名后缀 example-->'_MHT'

    其中前三个参数为必传参数 划重点，要考
    ----------请开心使用---------
    另脚本支持 -h --help 操作
 **当参数错误时，也有对应提示以及上述帮助信息**

#####正常使用
示例：
```
python changeClassName.py ./KanManHua ./KanManHua.xcodeproj/project.pbxproj MHT_ _MHT
```

#####helpinfo获取
示例：
```
python changeClassName.py
python changeClassName.py -h
python changeClassName.py --help
```

###[脚本地址](https://github.com/WangKunKun/FefactorClassName)

###后记

由于我司还有需求修改指定 target的类名，实际也有一套可以仅仅只修改target类名的方法，但是由于使用要复杂一点，首先要提取target对应的编译类，再使用脚本来修改，修改使用到我之前发布的一个工具类[MacPbxprojHelper](https://github.com/WangKunKun/MacPbxprojHelper)，如有需要的话请和我联系。
联系方式：357863248@qq.com

[MacPbxprojHelper介绍链接](https://www.jianshu.com/p/6814a593c984)