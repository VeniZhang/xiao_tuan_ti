#!coding:utf8
#group_num = input("how many groups  you want to create?")
#node_num = input("how many nodes in one group") #print group_num, node_num
import time
import math
class Network_():
    def __init__(self):
        self.group_num = 0
        self.node_num_per_group = 0
        self.groups = {}

    def groupConsensus(self):
        for gk, gv in self.groups.items():
            gv.consensus()
            
    def startSayHello(self):
        for gk, gv  in self.groups.items():
            for nk, nv in gv.nodes.items():
                print "befoer hello",nv.name,nv.value
                nv.hello()
                print "after hello",nv.name, nv.value,  nv.result_ask_node
        
    def update(self, times):
        for gk, gv in self.groups.items():
            for n,v  in gv.nodes.items() :
                print "befor update", n ,v.value,v.result_ask_node
                v.update(times)
                print "after update",v.value
                v.result_ask_node = []

    def consensus(self):
        i = 0
        while(not self.isConsensus()):
            i += 1
            self.startSayHello()
            self.update(i)
            time.sleep(1)

    def isConsensus(self):
        v = list((i.getValue()  for i in self.groups.values()))
        v.sort()
        print 'IN CONSENSUS',v
        if v[0] == v[-1]:
            return True
        else:
            return False

    def getValue(self):
        if self.isConsensus():
            return self.groups.values()[0]
        else:
            return None

    def getAll(self):
        for gv in self.groups.values():
            print gv.name, "--", gv.getValue()
            for nv in gv.nodes.values():
                print nv.name, ":",nv.value

    def getInfoFromFile(self):
        '''
            第一行： 组数 每个组的节点数
            第二行： 第一组的组名
            第三行： （第一组的成员）节点编号 节点值 
            。。。
            第  行： 第二组的组名
            。。。
            第  行： 各组之间的关系
        '''
        with open('xiaotuanti.zdq', 'r') as f:
            line = f.readline().split()
            self.group_num = int(line[0])
            self.node_num_per_group = int(line[1])
            for g in range(self.group_num):
                group_name = f.readline().strip()
                self.groups[group_name] = Group(group_name)
                for n in range(self.node_num_per_group):
                    node = Node()
                    node.name, node.value, node.attr = f.readline().split()
                    node.value = float(node.value)
                    node.attr = node.attr.strip()
                    if ":" in node.attr:
                        node.attr, node.updateFun = node.attr.split(":")
                    node.group = self.groups[group_name]
                    self.groups[group_name].nodes[node.name] = node
            #以上代码 输入了组，和组内的节点信息
            #以下代码 处理各组之间的关系
            #组名加节点名  组名加节点名
            for l in f.readlines():
                line = l.split()
                g_f, n_f = line[0].split('.')
                g_s, n_s = line[1].split(".")
                #self.groups.setdefault(g_f,
                self.groups[g_f].adj_groups.setdefault(g_s, {})
                dict_ = {n_s: self.groups[g_s].nodes[n_s]}
                self.groups[g_f].adj_groups[g_s][n_f] = dict_
                 
                dict_ = {n_f: self.groups[g_f].nodes[n_f]}
                self.groups[g_s].adj_groups.setdefault(g_f, {})
                self.groups[g_s].adj_groups[g_f][n_s] = dict_

class Group():
    def __init__(self, name=""):
        self.name = name
        self.nodes = {}
        self.adj_groups = {}
        self.value = 0

    def getValue(self):
        self.value = self.__getValue() 
        return self.value

    def __getValue(self):
        tem = list(( i.value  for i in self.nodes.values()))
        tem.sort()
        if len(tem) % 2 == 0:
            value = tem[len(tem)/2] + tem[len(tem)/2-1]
        else:
            value = tem[len(tem)/2]
        return value
   
    def __updateNode(self, name, value):
        if self.nodes[name].attr == "N":
            self.nodes[name].value = value

    def consensus(self):
        value = self.__getValue()
        for nk, nv  in self.nodes.items():
            self.__updateNode(nv.name, value)

class Node():
    def __init__(self):
        self.group = None
        self.value = 0
        self.name = 0
        self.attr = 0
        self.updateFun = None
        self.result_ask_node = []

    def getMates(self):
        return self.group.nodes
    
    def hello(self):
        for k, v in self.group.adj_groups.items():
            #adj_node = v[self.name]
            self.ask(k)

    def ask(self, group):
        nodes = self.group.nodes
        for node_k, node_v in nodes.items():
            node_ask = self.group.adj_groups[group][node_k]
            for nk, nv in node_ask.items():
                node_value = nv
                if nv.attr == "N":
                    self.result_ask_node.append(nv.group.getValue())
                else:
                    self.result_ask_node.append(nv.value)

    def update(self, times):
        if self.attr == "B":
           x = times
           self.value = eval(self.updateFun)
           print "zzz",self.value
        elif self.attr == "N": 
            values = self.result_ask_node
            values.sort()
            v = 0
            length = len(values)
            if length % 2 == 0:
                v = (values[length/2] + values[length/2 -1]) / 2
            else :
                v = values[length/2]
            self.value = 0.5 * self.value + 0.5 *v
        

if __name__ =="__main__":
    network_ = Network_()
    network_.getInfoFromFile()
    network_.groupConsensus()
    network_.consensus()
    print network_.getValue()
    print network_.getAll()
    """
    print "*************"
    print network_.groups["A"].adj_groups
    for i in network_.groups["A"].nodes:
        print i.name, i.value, i.group.name
    #print network_.groups["A"].nodes
    print network_.groups["B"].adj_groups

    """

    
    #print network_.groups["A"].getValue()
