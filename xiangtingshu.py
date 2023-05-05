# 向听数
'''
対子があり、まだ雀頭が決定していない場合は雀頭とする
雀頭として決定したあと、残っている対子は、搭子として扱う
「面子の数 + 搭子の数」が4を超えている場合、「搭子の数 = 4 - 面子の数」へ補正する
1～3の処理を行い「8 - 面子 * 2 - 搭子 - 雀頭の有無」を行う
※ 雀頭を取っていたら「雀頭の有無」は1、なかったら「0」
4で求めた最小の値を「向聴数として採用」する
'''
import re
import time
from generate_random_mahjong import generate_random_mahjong


# 有雀头时，23/13/12/22都是搭子

def keisann(keisann_list: list, counter: int, resultdict: dict):
    global resultdict_list
    # resultdict = {'mentsu': int, 'taatsu':int, 'toitsu':int}
    while counter < len(keisann_list):
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
            keisann(keisann_list_copy, counter, resultdict_copy)

        if keisann_list[counter] >= 3:
            # 刻字（面子）
            keisann_list_copy = keisann_list.copy()
            resultdict_copy = resultdict.copy()
            keisann_list_copy[counter] -= 3
            resultdict_copy['mentsu'] += 1
            resultdict_list.append(resultdict_copy)
            keisann(keisann_list_copy.copy(), counter, resultdict_copy)

        if counter < len(keisann_list) - 2 and keisann_list[counter] >= 1 and keisann_list[counter + 1] >= 1 and \
                keisann_list[counter + 2] >= 1:
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

        counter += 1


def keisann_z(keisann_list: list, counter: int, resultdict: dict):
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


def remove_duplicate_dicts(resultdict_list):
    # 第一次减少resultdict_list中的数量
    new_resultdict_list = []
    for d in resultdict_list:
        # 将resultdict_list中重复的dict去除
        if d not in new_resultdict_list:
            new_resultdict_list.append(d)

    # 第二次减少resultdict_list中的数量
    # 用于存储去重后的字典
    unique_dicts = []
    for d1 in range(len(new_resultdict_list)):
        # 是否需要添加到去重后的列表中的标志
        add_flag = True
        for d2 in range(len(new_resultdict_list)):
            if new_resultdict_list[d1]['mentsu'] == new_resultdict_list[d2]['mentsu'] and new_resultdict_list[d1][
                'taatsu'] == new_resultdict_list[d2]['taatsu'] and new_resultdict_list[d1]['toitsu'] < \
                    new_resultdict_list[d2]['toitsu']:
                # 不需要添加到去重后的列表中
                add_flag = False
                break
            if new_resultdict_list[d1]['mentsu'] == new_resultdict_list[d2]['mentsu'] and new_resultdict_list[d1][
                'taatsu'] < new_resultdict_list[d2]['taatsu'] and new_resultdict_list[d1]['toitsu'] == \
                    new_resultdict_list[d2]['toitsu']:
                # 不需要添加到去重后的列表中
                add_flag = False
                break
            if new_resultdict_list[d1]['mentsu'] < new_resultdict_list[d2]['mentsu'] and new_resultdict_list[d1][
                'taatsu'] == new_resultdict_list[d2]['taatsu'] and new_resultdict_list[d1]['toitsu'] == \
                    new_resultdict_list[d2]['toitsu']:
                # 不需要添加到去重后的列表中
                add_flag = False
                break

        # 如果需要添加到去重后的列表中，则将其添加到列表中
        if add_flag:
            unique_dicts.append(new_resultdict_list[d1])

    return unique_dicts


def shanten(list_s: list, list_m: list, list_p: list, list_z: list):
    global resultdict_list
    min_shanten = 8
    resultdict = {'mentsu': 0, 'taatsu': 0, 'toitsu': 0}
    keisann(list_s, 0, resultdict)
    resultdict_list = remove_duplicate_dicts(resultdict_list.copy())
    resultdict_list_copy_s = resultdict_list.copy()

    for dict_temp_s in resultdict_list_copy_s:
        resultdict_list = resultdict_list_copy_s.copy()
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
                        # print(mentsu,taatsu,toitsu)

                    '''
                    if min_shanten == -1 or min_shanten == 0:
                        return min_shanten 
                    '''

    resultdict_list = [{'mentsu': 0, 'taatsu': 0, 'toitsu': 0}]
    return min_shanten


def ukeire_display(list_s_copy, list_m_copy, list_p_copy, list_z_copy, marker, counter):
    global output_dict
    global list_s, list_m, list_p, list_z
    for num in range(9):
        # 分别对smpz增加一张牌
        if list_s_copy[num] != 4:
            list_s_copy[num] += 1
            if shanten(list_s, list_m, list_p, list_z) > shanten(list_s_copy, list_m_copy, list_p_copy, list_z_copy):
                # 如果向听数减少，则输出该牌
                output_dict[marker][counter + 1][0].add(f'{num + 1}s')
            list_s_copy[num] -= 1

        if list_m_copy[num] != 4:
            list_m_copy[num] += 1
            if shanten(list_s, list_m, list_p, list_z) > shanten(list_s_copy, list_m_copy, list_p_copy, list_z_copy):
                # 如果向听数减少，则输出该牌
                output_dict[marker][counter + 1][0].add(f'{num + 1}m')
            list_m_copy[num] -= 1

        if list_p_copy[num] != 4:
            list_p_copy[num] += 1
            if shanten(list_s, list_m, list_p, list_z) > shanten(list_s_copy, list_m_copy, list_p_copy, list_z_copy):
                # 如果向听数减少，则输出该牌
                output_dict[marker][counter + 1][0].add(f'{num + 1}p')
            list_p_copy[num] -= 1

    for num in range(7):
        list_z_copy[num] += 1
        if shanten(list_s, list_m, list_p, list_z) > shanten(list_s_copy, list_m_copy, list_p_copy, list_z_copy):
            # 如果向听数减少，则输出该牌
            output_dict[marker][counter + 1][0].add(f'{num + 1}z')
        list_z_copy[num] -= 1


def ukeire(marker: str, counter: int):
    global output_dict
    global list_s, list_m, list_p, list_z
    list_s_copy = list_s.copy()
    list_m_copy = list_m.copy()
    list_p_copy = list_p.copy()
    list_z_copy = list_z.copy()
    listcopy_dict = {'s': list_s_copy, 'm': list_m_copy, 'p': list_p_copy, 'z': list_z_copy}
    # 将marker和list对应
    if listcopy_dict[marker][counter] != 0:
        listcopy_dict[marker][counter] -= 1
        if shanten(list_s, list_m, list_p, list_z) == shanten(list_s_copy, list_m_copy, list_p_copy, list_z_copy):
            ukeire_display(list_s_copy, list_m_copy, list_p_copy, list_z_copy, marker, counter)
            # print(f'{counter + 1}{marker}: ', end = '')
            # print()
        listcopy_dict[marker][counter] += 1


def output_display(output_dict, min_shanten):
    global list_s, list_m, list_p, list_z

    for pai, pai_list in output_dict.items():
        print(f'{pai}: {min_shanten}向听', end=' ')
        # 先倒序再排序再倒序，使得按照smpz的顺序输出
        for content_num in range(len(pai_list)):
            pai_list[content_num] = pai_list[content_num][::-1]
        pai_list.sort()
        for content_num in range(len(pai_list)):
            pai_list[content_num] = pai_list[content_num][::-1]

        for content in pai_list:
            print(content, end=' ')
        print(f'{len(pai_list)}种')


def mahjong_display(dict_smpz: dict, min_shanten):
    out_str = ""
    for letter in ['s', 'm', 'p']:
        for num in range(1, 10):
            if dict_smpz[letter][num][1] == 0:
                continue
            else:
                print(f"{num}{letter}: {min_shanten}向听", end=' ')
                out_str += f"|{num}{letter}|{min_shanten}向听|"
                dict_smpz[letter][num][0] = list(dict_smpz[letter][num][0])
                for content_num in range(len(dict_smpz[letter][num][0])):
                    dict_smpz[letter][num][0][content_num] = dict_smpz[letter][num][0][content_num][::-1]
                # 将dict_smpz[letter][num][0]中的所有字符串倒序
                dict_smpz[letter][num][0].sort()
                # print(dict_smpz[letter][num][0])
                # 将倒序的字符串排序
                for content_num in range(len(dict_smpz[letter][num][0])):
                    dict_smpz[letter][num][0][content_num] = dict_smpz[letter][num][0][content_num][::-1]
                # 将倒序的字符串倒序
                for num_2 in dict_smpz[letter][num][0]:
                    print(f"{num_2}", end=' ')
                    out_str += f"{num_2} "
                print(f"{len(dict_smpz[letter][num][0])}种{dict_smpz[letter][num][1]}枚")
                out_str += f"|{len(dict_smpz[letter][num][0])}种{dict_smpz[letter][num][1]}枚|\n"

    for letter in ['z']:
        for num in range(1, 8):
            if dict_smpz[letter][num][1] == 0:
                continue
            else:
                print(f"{num}{letter}: {min_shanten}向听", end=' ')
                out_str += f"|{num}{letter}|{min_shanten}向听|"
                dict_smpz[letter][num][0] = list(dict_smpz[letter][num][0])
                for content_num in range(len(dict_smpz[letter][num][0])):
                    dict_smpz[letter][num][0][content_num] = dict_smpz[letter][num][0][content_num][::-1]
                # 将dict_smpz[letter][num][0]中的所有字符串倒序
                dict_smpz[letter][num][0].sort()
                # print(dict_smpz[letter][num][0])
                # 将倒序的字符串排序
                for content_num in range(len(dict_smpz[letter][num][0])):
                    dict_smpz[letter][num][0][content_num] = dict_smpz[letter][num][0][content_num][::-1]
                # 将倒序的字符串倒序
                for num_2 in dict_smpz[letter][num][0]:
                    print(f"{num_2}", end=' ')
                    out_str += f"{num_2} "
                print(f"{len(dict_smpz[letter][num][0])}种{dict_smpz[letter][num][1]}枚")
                out_str += f"|{len(dict_smpz[letter][num][0])}种{dict_smpz[letter][num][1]}枚|\n"
    return out_str


def Reverse(l: list):
    length = len(l)
    for i in range(length):
        l[i] = 4 - l[i]
    return l


def paishan(list_s, list_p, list_m, list_z):
    global output_dict
    c_list_s = Reverse(list_s.copy())
    c_list_p = Reverse(list_p.copy())
    c_list_m = Reverse(list_m.copy())
    c_list_z = Reverse(list_z.copy())
    s_dict = {'s': c_list_s, 'p': c_list_p, 'm': c_list_m, 'z': c_list_z}
    # if list_s == [0,0,0,1,1,1,0,0,0]
    # c_list_s == [4,4,4,3,3,3,4,4,4]
    # s_dict['s'] is a list!
    for letter in ['s', 'p', 'm', 'z']:
        for num in output_dict[letter]:
            if output_dict[letter][num][0]:
                Sum = sum([s_dict[i[1]][int(i[0]) - 1] for i in output_dict[letter][num][0]])
                # list_t[letter][num][0] is a set,list_t[letter][num][1] is a num!
                # for exmaple i == '5s'
                # i[1] == 's', int(i[0]) == 5
                output_dict[letter][num][1] = Sum


def initial_dict():
    '''
    the resulf of initial()
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


def main_test(list_s, list_m, list_p, list_z):
    out_str = ""
    if shanten(list_s, list_m, list_p, list_z) >= 0:
        for counter in range(9):
            ukeire('s', counter)
        for counter in range(9):
            ukeire('m', counter)
        for counter in range(9):
            ukeire('p', counter)
        for counter in range(7):
            ukeire('z', counter)
        paishan(list_s, list_p, list_m, list_z)
        out_str = mahjong_display(output_dict, shanten(list_s, list_m, list_p, list_z))

    if shanten(list_s, list_m, list_p, list_z) == -1:
        print("和牌！")
    return out_str


def list_transfer_smp(list_smp: list):
    # ['1', '2', '3', '4', '5', '6', '7', '8', '9'] -> [1,1,1,1,1,1,1,1,1]
    dict_smp = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}
    list_smp_ = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for string in list_smp:
        list_smp_[dict_smp[string]] += 1
    return list_smp_


def list_transfer_z(list_z: list):
    dict_z = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6}
    list_z_ = [0, 0, 0, 0, 0, 0, 0]
    for string in list_z:
        list_z_[dict_z[string]] += 1
    return list_z_


def mahjong_Isreasonable():
    # 判断输入的牌型是否为14张，若符合则返回值是True，反之为False
    if len(mahjong_s_list) + len(mahjong_m_list) + len(mahjong_p_list) + len(mahjong_z_list) != 14:
        print("你输入的牌的总数不是14张！请重新运行程序！")
        return False
    else:
        # print("您输入的牌的总数为14张！")
        return True


def mahjong_transferation(mahjong):
    out_str = ""
    # mahjong -> mahjong_m/s/p/z_list
    j = 0
    global mahjong_s_list, mahjong_m_list, mahjong_p_list, mahjong_z_list
    global list_s, list_m, list_p, list_z
    for i in range(len(mahjong)):
        if mahjong[i] == 's' or mahjong[i] == 'm' or mahjong[i] == 'p' or mahjong[i] == 'z':
            first_digit = j
            end_digit = i
            if mahjong[i] == 's':
                mahjong_s_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'm':
                mahjong_m_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'p':
                mahjong_p_list = list(mahjong[first_digit:end_digit])
            if mahjong[i] == 'z':
                mahjong_z_list = list(mahjong[first_digit:end_digit])
            j = i + 1

    # 赤宝牌的转化0 -> 5
    for i in range(len(mahjong_s_list)):
        if mahjong_s_list[i] == '0':
            mahjong_s_list[i] = '5'
    for i in range(len(mahjong_m_list)):
        if mahjong_m_list[i] == '0':
            mahjong_m_list[i] = '5'
    for i in range(len(mahjong_p_list)):
        if mahjong_p_list[i] == '0':
            mahjong_p_list[i] = '5'
    # type(mahjong_s/m/p/z) is list
    list_s = list_transfer_smp(mahjong_s_list)
    list_m = list_transfer_smp(mahjong_m_list)
    list_p = list_transfer_smp(mahjong_p_list)
    list_z = list_transfer_z(mahjong_z_list)

    if mahjong_Isreasonable():
        out_str = main_test(list_s, list_m, list_p, list_z)
    return out_str


def visualization_handcard(s):
    p2 = re.compile('([1-9]{,14})p')
    p3 = re.compile('([1-9]{,14})m')
    p4 = re.compile('([1-9]{,14})s')
    p5 = re.compile('([1-9]{,14})z')
    image_str = ""
    for p in [p3, p2, p4, p5]:
        if p.findall(s):
            for i in p.findall(mahjong)[0]:
                if p == p2:
                    image_str += f"![pin{i}-66-90-s-emb](./pai-images/pai-images/pin{i}-66-90-s.png)"
                if p == p3:
                    image_str += f"![man{i}-66-90-s-emb](./pai-images/pai-images/man{i}-66-90-s.png)"
                if p == p4:
                    image_str += f"![sou{i}-66-90-s-emb](./pai-images/pai-images/sou{i}-66-90-s.png)"
                if p == p5:
                    image_str += f"![ji{i}-66-90-s-emb](./pai-images/pai-images/ji{i}-66-90-s.png)"
    out_put = f"手牌：{image_str}\n"
    return out_put


def visualization(out, out_hand):
    regex = re.compile("[1-9][mpzs]")
    for i in regex.findall(out):

        if i[1] == "m":
            type = "man"
        if i[1] == "p":
            type = "pin"
        if i[1] == "s":
            type = "sou"
        if i[1] == "z":
            type = "ji"

        out = regex.sub(
            f"![{type}{i[0]}-66-90-s-emb](./pai-images/pai-images/{type}{i[0]}-66-90-s.png)",
            out, count=1)
    # out = out.replace(" ", "|")
    # out = out.replace("\n", "")

    with open("visualization.md", 'w') as output:
        output.write(out_hand)
        output.write("| 打  | 向听数 | 进章 |      |\n| :--: | :-- | :---- | ---- |\n")
        output.write(out)


start_time = time.time()
for _ in range(100):
    resultdict_list = [{'mentsu': 0, 'taatsu': 0, 'toitsu': 0}]
    output_dict = initial_dict()
    # print(shanten(list_s, list_m, list_p, list_z))
    mahjong_s_list, mahjong_p_list, mahjong_m_list, mahjong_z_list = [], [], [], []
    list_s, list_m, list_p, list_z = [], [], [], []
    """mahjong = input('''
    - m=萬子(1-9), p=筒子, s=索子, z=字牌(东南西北白发中对应1-7), (0=赤(5))
    - 一般形=４面子+１雀頭 
    - 和了役の判定はありません/ 標準形=一般形＋七対形＋国士形
    - 暗槓はできません
    ''')"""
    mahjong = generate_random_mahjong()
    # mahjong = '334567m22234p123s'
    out_str = mahjong_transferation(mahjong)
    out_hand = visualization_handcard(mahjong)
    visualization(out_str, out_hand)
end_time = time.time()
print(end_time - start_time)
