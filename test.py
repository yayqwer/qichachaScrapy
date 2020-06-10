
def main():
    members = ['北斗阳明贪狼星', '北斗阴精巨门星', '北斗真人禄存星', '北斗玄冥文曲星', '北斗丹元廉贞星', '北斗北极武曲星', '北斗天关破军星']


    # '北斗阳明贪狼星' 在列表中吗？
    res = '北斗阳明贪狼星' not in members
    print(res)

    # '行初心' 不在列表中吗？
    res = '行初心' not in members
    print(res)

    ls1 = [[6]]
    for i in range(10):
        ls = []

        ls.append(i)
        ls1.append(ls)
        print(ls)
        print(ls1)
        res = ls not in ls1
        print(res)
        # print(ls1)


    ls3 = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
    #
    # for i in ls3:
    #
    #     res = i not in ls3
    #     print(res)

if __name__ == '__main__':
    main()