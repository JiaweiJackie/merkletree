import math
import hashlib
import random
import sys


def message_(l):  # length 代表要求生成节点的数目
    choosen = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    m = []
    for k in range(l):
        for j in range(5):
            a = ''.join(random.choice(choosen))  # 随机选择字符
        m.append(a)
    return m


def create(message):
    node_number = len(message)  # 节点个数
    depth = math.ceil(math.log(node_number, 2)) + 1  # 二叉树深度
    merkletree = []
    merkletree.append([hashlib.sha256(i.encode()).hexdigest() for i in message])
    for i in range(depth - 1):
        merkletree_part = []  # 用于merkletree的层结构
        length_each = math.floor(len(merkletree[i]) / 2)  # 上一层节点的个数
        merkletree_part.extend(
            [hashlib.sha256(merkletree[i][j * 2].encode() + merkletree[i][j * 2 + 1].encode()).hexdigest() for j in
             range(length_each)])
        if length_each * 2 != len(merkletree[i]):  # 如果下层节点无法满足两两归一的要求，将多余的节点直接往上提
            merkletree_part.append(merkletree[i][-1])
            # del merkletree[i][-1] 
        merkletree.append(merkletree_part)  # 添加进总树的存储结构之中
    return merkletree


def verify(message, a, merkletree):
    message_hash = (hashlib.sha256(message.encode())).hexdigest()  # 将消息进行hash用于匹配
    place = merkletree[0].index(message_hash)
    proof = []  # 存储需要用于验证的相关节点数据，审核节点
    for i in range(len(merkletree) - 1):  # 根节点无需验证
        if place % 2 == 0:  # 左侧的兄弟节点
            if place != len(merkletree[i]) - 1:  # 如果本身不位于当前层的最后一落单节点(无兄弟节点)
                proof.append(['0', merkletree[i][place + 1]])
        else:  # 位置在两兄弟节点的右侧
            proof.append([merkletree[i][place - 1], '0'])
        place = math.floor(place / 2)
    c = (hashlib.sha256(message.encode())).hexdigest()  # 进行hash用于验证
    length = len(proof)
    m = 0
    while (m < length):
        i = proof[m]
        if i[0] == '0':
            c = hashlib.sha256(c.encode() + i[1].encode()).hexdigest()
        else:
            c = hashlib.sha256(i[0].encode() + c.encode()).hexdigest()
        m = m + 1
    if c == a:
        print("in this merkle tree")
    else:
        print("fail,isn't in this merkle tree")


m = input("please enter the number of nodes:")
message = message_(int(m))
tree = create(message)
'''
for i in tree_1: #打印节点内容
    print(i, "\n")
'''
number = int(input("please enter the number to choose a message:"))
'''
number = random.randint(0, int(m) - 1) #或者随机生成一个节点数
'''
print("message is:", message[number])
'''
for i in proof_node:
    print(i)
'''
verify(message[number], tree[-1][0], tree)
