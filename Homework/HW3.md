## 数据库 HW3

**PB20000215 丁程**

**1、已知有关系模式 R(A, B, C, D, E)，R 上的一个函数依赖集如下：**
**F={A→BC, B→CD, A→E, AB→C, AC→DE, BE→AD }**

**(1)求出 F 的最小函数依赖集（要求写出求解过程）**
* 将右边写成单属性并去除重复FD
F={A→B,A→C,B→C,B→D,A→E,AB→C,AC→D,AC→E,BE→A,BE→D}
* 消去左部冗余属性
A→B,AB→C可推出A→C
A→C,AC→D,AC→E可推出A→D, A→E
F={A→B,A→C,B→C,B→D,A→E,A→D,BE→A,BE→D}
* 消去冗余函数依赖
A→C,A→D,BE→D冗余
F_min={A→B,B→C,B→D,A→E,BE→A}

**(2)求 R 的候选码，并给出证明**

U = {A, B, C, D, E}
A→U,并且不存在A的真子集X使得X→U
BE→U,并且不存在BE的真子集Y使得Y→U
因此R的候选码为A, BE

**(3)判断 R 属于第几范式？为什么**
R的非主属性C,D都完全函数依赖于主属性A, BE，满足2NF要求
非主属性C,D之间不存在传递依赖关系，因此满足3NF要求
存在非平凡函数依赖B→C,B→D,其中B不是R的超码,因此不满足BCNF
因此R属于第三范式3NF


**2、现有关系模式: R(A, B, C, D, E, F, G)，R 上的一个函数依赖集：**
**F={ A→B, B→C, AC→DE, E→F, AB→E, AC→G}**

**(1)求出 F 的最小函数依赖集（要求写出求解过程）**
* 将右边写成单属性并去除重复FD
F={A→B,B→C,AC→D,AC→E,E→F,AB→E,AC→G}
* 消去左部冗余属性
A→B,B→C可推出A→C
A→C,AC→D,AC→E可推出A→D, A→E
A→B,AB→E可推出A→E
A→C,AC→G可推出A→G
F={A→B,B→C,A→C,A→D,A→E,E→F,A→G}

* 消去冗余函数依赖
A→C冗余
F_min={A→B,B→C,A→D,A→E,E→F,A→G}

**(2)求 R 的候选码，并给出证明**
U = {A, B, C, D, E, F, G}
{A}是唯一的最小的使得闭包为U的集合，因此R的候选码为{A}

**(3)判断 R 属于第几范式？为什么？**
R的非主属性B,C,D,E,F,G都完全函数依赖于主属性A，满足2NF要求
并且由A→B,B→C可知，C传递依赖于主属性A，不满足3NF要求。
因此R属于第二范式。

**(4)请将关系模式 R 无损连接并且保持函数依赖地分解到 3NF，要求给出具体步骤**
F_min={A→B,B→C,A→D,A→E,E→F,A→G}
所有属性均在F中出现
对F按相同左部分组，得到q={R1(A,B,D,E,G),R2(B,C),R3(E,F)}
主码为{A}
P =q U R(A,F,G)={R1(A,B,E),R2(B,C),R3(C,D),R(A)}
因为A ⊆ ABE, 所以去掉R(A)
所求分解P = {R1(A,B,E),R2(B,C),R3(C,D)}


**3、现有关系模式: R(A, B, C, D, E, F, G)，R 上的一个函数依赖集：**
**F={AB→E, A→B, B→C, C→D}**

**(1)该关系模式满足第几范式? 为什么?**
AB→E,A→B可推出A→E
F_min = {A→E, A→B, B→C, C→D}
候选码为{A,F,G}，存在局部依赖A→B
所以该关系模式属于第一范式1NF

**(2)请将关系模式 R 无损连接地分解到 BCNF，要求给出步骤.**
* 先消除A->E，得到R1(A,E),R2(A,B,C,D,F,G)
A->B,B->C,C->D是连续的传递依赖，消除的先后顺序会影响最终结果。
* 消除R2中的A->B:R1(A,E),R2(A,B),R3(A,C,D,F,G),依赖为A->C,C->D
答案1:消除A->C:R1(A,E),R2(A,B),R3(A,C),R4(A,D),R5(A,F,G)
答案2:消除C->D:R1(A,E),R2(A,B),R3(C,D),R4(A,C),R5(A,F,G)
* 消除R2中的B->C:R1(A,E),R2(B,C),R3(A,B,D,F,G),依赖为A->B,B->D.
答案3:消除A->B:R1(A,E),R2(B,C),R3(A,B),R4(A,D),R5(A,F,G)
答案4:消除B->D:R1(A,E),R2(B,C),R3(B,D),R4(A,B),R5(A,F,G)
* 消除R2中的C->D:R1(A,E),R2(C,D),R3(A,B,C,F,G),依赖为A->B,B->C
答案5:消除A->B:R1(A,E),R2(C,D),R3(A,B),R4(A,C),R5(A,F,G)
答案6:消除B->C:R1(A,E),R2(C,D),R3(B,C),R4(A,B),R5(A,F,G)

