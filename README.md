# SJTU_Mahjong

## 前言

我们希望能够通过python实现类似与天凤牌理（[オンライン対戦麻雀 天鳳 / 牌理 (tenhou.net)](https://tenhou.net/2/)）的功能，即：基于你输入的牌，输出可能最优的打法。

虽然python上有mahjong这个包，但是我们打算利用已学内容独立地复现这个包中部分的功能。

最后，在我们完成的代码之上，实现部分的可视化，优化用户的可读性。

麻将图片来源：[【保存版】商用無料の高クオリティーの麻雀画像の無料素材まとめ | 麻雀豆腐 (majandofu.com)](https://majandofu.com/mahjong-images)

可视化参考：[牌効率トレーニングルーム - 牌効率を学ぶための計算ツール (clovernote.net)](http://mahjong.clovernote.net/)



## 进程更新



### Target 5 可视化部分

利用python输出markdown文件，并且根据下载的图片输出相对应的结果，达到可视化的目标。

### Target 4 判断向听数以及最优选择

此块是全篇最重要的内容！！

参考内容：[C#で麻雀の向聴数を求める方法!詳細解説&サンプルがダウンロード可能 (ganohr.net)](https://ganohr.net/blog/csharp-howto-calculate-mahjong-reach-distance/)



```python
def keisann(keisann_list: list, counter: int , resultdict: dict):
    global resultdict_list
    # resultdict = {'mentsu': int, 'taatsu':int, 'toitsu':int}
    # resultdict_list is a list whose elements are dict
    while counter < len(keisann_list):
        while keisann_list[counter] == 0 and counter < len(keisann_list) - 1:
        # 找到第一个keisann_list[counter]不为0的counter
            counter += 1
        
        if keisann_list[counter] >= 2:
            # 对子
            keisann_list_copy = keisann_list.copy()
            # 每一遍调用的时候使用函数keisann中的参数list的copy，保证了能够执行不同if的分支
            resultdict_copy = resultdict.copy()
            # 基于参数dict的各个内容的值，为了不影响其他分支，也使用copy
            keisann_list_copy[counter] -= 2
            resultdict_copy['toitsu'] += 1
            resultdict_list.append(resultdict_copy)
            # 每一次执行的时候使用append，虽然会减少效率，但是一定保证各种排列组合
            keisann(keisann_list_copy, counter, resultdict_copy)
            # 使用递归的思想，继续调用keisann函数
            
        if keisann_list[counter] >= 3:
            # 刻字（面子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 3
            resultdict_copy['mentsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann(keisann_list_copy.copy(), counter, resultdict_copy)
    
        if counter < len(keisann_list) - 2 and keisann_list[counter] >= 1 and keisann_list[counter + 1] >= 1 and keisann_list[counter + 2] >= 1:
            # 顺子（面子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 1
            keisann_list_copy[counter + 1] -= 1
            keisann_list_copy[counter + 2] -= 1
            resultdict_copy['mentsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann(keisann_list_copy.copy(), counter, resultdict_copy)
        
        if counter < len(keisann_list) - 2 and keisann_list[counter] >= 1 and keisann_list[counter + 2] >= 1:
            # 坎张（搭子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 1
            keisann_list_copy[counter + 2] -= 1
            resultdict_copy['taatsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann(keisann_list_copy.copy(), counter, resultdict_copy)
        
        if counter < len(keisann_list) - 1 and keisann_list[counter] >= 1 and keisann_list[counter + 1] >= 1:
            # 两面/边张（搭子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 1
            keisann_list_copy[counter + 1] -= 1
            resultdict_copy['taatsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann(keisann_list_copy.copy(), counter, resultdict_copy)
        
        counter +=1


def keisann_z(keisann_list: list, counter: int , resultdict: dict):
    global resultdict_list
    # similar to the above function, except that specific for list_z
    while counter < len(keisann_list) - 1:
        while keisann_list[counter] == 0 and counter < len(keisann_list) - 1:
        # 找到第一个keisann_list[counter]不为0的counter
            counter += 1
        
        if keisann_list[counter] >= 2:
            # 对子
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 2
            resultdict_copy['toitsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann_z(keisann_list_copy, counter, resultdict_copy)
            
        
        if keisann_list[counter] >= 3:
            # 刻字（面子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 3
            resultdict_copy['mentsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann_z(keisann_list_copy.copy(), counter, resultdict_copy)

        counter += 1
```

```python
def shanten(list_s: list, list_m: list, list_p: list, list_z: list):
    global resultdict_list
    min_shanten = 8
    # 将最小向听数定义为8（一般型）
    resultdict = {'mentsu':0, 'taatsu':0, 'toitsu':0}
    keisann(list_s, 0, resultdict)
    resultdict_list = remove_duplicate_dicts(resultdict_list.copy())
    # 每次计算完，减少resultdict_list中不必要的内容，增加计算效率
    resultdict_list_copy_s = resultdict_list.copy()
    # 将此刻resultdict_list的内容保存，使得下层循环调用完后重新调用

    for dict_temp_s in resultdict_list_copy_s:
        resultdict_list = resultdict_list_copy_s.copy()
        # 一次循环调用完，将resultdict_list归零为上层保存的内容     
        keisann(list_m, 0, dict_temp_s)
        resultdict_list = remove_duplicate_dicts(resultdict_list.copy())
        resultdict_list_copy_m = resultdict_list.copy()

        for dict_temp_m in resultdict_list_copy_m:
            resultdict_list = resultdict_list_copy_m.copy()
            keisann(list_p, 0, dict_temp_m)
            resultdict_list = remove_duplicate_dicts(resultdict_list.copy())
            resultdict_list_copy_p = resultdict_list.copy()

            for dict_temp_p in resultdict_list_copy_p:
                resultdict_list = resultdict_list_copy_p.copy()
                keisann_z(list_z, 0, dict_temp_p)
                resultdict_list = remove_duplicate_dicts(resultdict_list.copy())
                resultdict_list_copy_z = resultdict_list.copy()

                for dict_temp_z in resultdict_list_copy_z:
                    toitsu = dict_temp_z['toitsu']
                    taatsu = dict_temp_z['taatsu']
                    mentsu = dict_temp_z['mentsu']
                    janto = 0
                    hasJanto = False
                    # menntsu:面子 taatsu:搭子 janto:雀头

                    if toitsu > 0:
                        hasJanto = True
                        taatsu += toitsu - 1

                    if mentsu + taatsu > 4:
                        taatsu = 4 - mentsu

                    if hasJanto:
                        janto = 1
                        
                    shanten = 8 - mentsu * 2 - taatsu - janto
                    # very important! core equation!

                    if shanten < min_shanten:
                        min_shanten = shanten

    resultdict_list = [{'mentsu':0, 'taatsu':0, 'toitsu':0}]
    # 每次执行完shanten函数，为了不影响下次使用，将resultdict_list归零          
    return min_shanten 
```

```python
def main_test(list_s, list_m, list_p, list_z):
    for counter in range(9):
        ukeire('s', counter)
    for counter in range(9):
        ukeire('m', counter)
    for counter in range(9):
        ukeire('p', counter)
    for counter in range(7):
        ukeire('z', counter)
```



### Target 3 判断听牌并输出

听牌的判断同样可以由判断向听数中相关的代码（和牌即向听数为0）解决。

```python
def initial_dict():
    # 生成的字典格式如下所示，为了方便后续输出
    '''
    the resulf of initial():
    {'s': {1: [set(), 0], 2: [set(), 0], 3: [set(), 0], 4: [set(), 0], 5: [set(), 0], 6: [set(), 0], 7: [set(), 0], 8: [set(), 0], 9: [set(), 0]},
    'm': {1: [set(), 0], 2: [set(), 0], 3: [set(), 0], 4: [set(), 0], 5: [set(), 0], 6: [set(), 0], 7: [set(), 0], 8: [set(), 0], 9: [set(), 0]},
    'p': {1: [set(), 0], 2: [set(), 0], 3: [set(), 0], 4: [set(), 0], 5: [set(), 0], 6: [set(), 0], 7: [set(), 0], 8: [set(), 0], 9: [set(), 0]},
    'z': {1: [set(), 0], 2: [set(), 0], 3: [set(), 0], 4: [set(), 0], 5: [set(), 0], 6: [set(), 0], 7: [set(), 0]}}

    dict['s','m','p','z'] -> dict[1-9] -> list-> set and num
    '''
    dict_smpz = {}
    for letter in ['s', 'm', 'p', 'z']:
        dict_smpz[letter] = {}
    for num in range(1, 10):
        for letter in ['s', 'm', 'p']:
            dict_smpz[letter][num] = [set(), 0]
    for num in range(1, 8):
        dict_smpz['z'][num] = [set(), 0]
    return dict_smpz
```



### Target 2 判断是否和牌

和牌的判断可以由判断向听数中相关的代码（和牌即向听数为-1）解决，这里简单介绍一些麻将相关的概念。

麻将和牌形式（一般型）：
面子\*4+雀头\*1

其中面子是顺子（顾名思义，比如123m）或者刻子（三张相同的牌，比如111m），雀头则是两张相同的牌，或叫做对子。



### Target 1 将输入内容转换

先将所有牌进行编号，这里采用天凤（或者说是主流）编号方式，`0-9s,0-9m,0-9p,1-7z`（其中，s为索，m为万，p为饼，z为字，特别地，1-7z对应东南西北白发中，0为赤）并且规定用户输入的内容必须符合标准形式，否则将报错，以下为规则：

**smpz只能出现一次，牌必须在相对应输入的前边，smpz没有顺序要求，输出的数字也没有顺序要求。**

例如，`123789s123p11z123m`

可以通过正则表达式：

```python
import re
# 例如"\d+[smpz]" 并提取其中的数字
```

完成，不过我们这里采用另外相对简单的方法：

```python
# mahjong为用户输入的字母串
for i in range(len(mahjong)):
        if mahjong[i] == 's' or mahjong[i] == 'm' or mahjong[i] == 'p' or mahjong[i] == 'z':
            first_digit = j
            end_digit = i
            # 识别字母smpz，并将数字转换到相应的列表中
            if mahjong[i] == 's':
                mahjong_s_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'm':
                mahjong_m_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'p':
                mahjong_p_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'z':
                mahjong_z_list = list(mahjong[first_digit:end_digit])
            j = i + 1
# mahjong -> mahjong_(s/m/p/z)_list
```

此时列表中的内容为字符串，以最开始的输入为例`123789s123p11z123m`：

```python
# mahjong_s_list = ['1','2','3','7','8','9']
# mahjong_m_list = ['1','2','3']
# mahjong_p_list = ['1','2','3']
# mahjong_z_list = ['1','1']
```

为了后续处理方便，再进行第二步转换：

```python
def list_transfer_smp(list_smp:list):
    #['1', '2', '3', '4', '5', '6', '7', '8', '9'] -> [1,1,1,1,1,1,1,1,1]
    dict_smp= {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8}
    list_smp_= [0,0,0,0,0,0,0,0,0]
    for string in list_smp:
        list_smp_[dict_smp[string]] += 1
    return list_smp_

# 生成的smp与z对应的列表长度不一样，因此使用不同的函数
def list_transfer_z(list_z:list):
    dict_z= {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6}
    list_z_= [0,0,0,0,0,0,0]
    for string in list_z:
        list_z_[dict_z[string]] += 1
    return list_z_
# mahjong_(s/m/p/z)_list -> list_(s/m/p/z)
```

```python
list_s = list_transfer_smp(mahjong_s_list)
list_m = list_transfer_smp(mahjong_m_list)
list_p = list_transfer_smp(mahjong_p_list)
list_z = list_transfer_z(mahjong_z_list)
# list_s = [1,1,1,0,0,0,1,1,1]
# list_m = [1,1,1,0,0,0,0,0,0]
# list_p = [1,1,1,0,0,0,0,0,0]
# list_z = [2,0,0,0,0,0,0]
```



