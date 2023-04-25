## 数据库 HW2

**PB20000215 丁程**

**1、已知有关系模式 R(A, B, C, D, E)，R 上的一个函数依赖集如下：**
**F={A→BC, B→CD, A→E, AB→C, AC→DE, BE→AD }**

**(1)求出 F 的最小函数依赖集（要求写出求解过程）**
将右边写成单属性并去除重复FD(分解率)
F={A→B,A→C,B→C,B→D,A→E,AB→C,AC→D,AC→E,BE→A,BE→D}
消去左部冗余属性
A→B 和 A→C 可以推导出 AB→C，所以删除 AB→C；
A→B、A→C 和 B→D 可以推导出 AC→D，所以删除 AC→D；
A→C 和 B→D 可以推导出 BE→D，所以删除 BE→D。
F = {A→B, A→C, B→C, B→D, A→E, AC→E, BE→A}
合并右部相同的函数依赖得到
F = {A→BCE, B→CD, AC→E, BE→A}


**(2)求 R 的候选码，并给出证明**
计算属性集合的闭包，得到：
A+ = {A, B, C, D, E}
B+ = {B, C, D}
C+ = {C}
D+ = {D}
E+ = {E}
AB+ = {A, B, C, D, E}
AC+ = {A, B, C, D, E}
AE+ = {A, B, C, D, E}
BC+ = {B, C, D}
BE+ = {A, B, C, D, E}

U = {A, B, C, D, E}
A是最小的闭包为U的集合，因此R的候选码为{A}

**(3)判断 R 属于第几范式？为什么**