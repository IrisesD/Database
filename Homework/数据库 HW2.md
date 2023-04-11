## 数据库 HW1

PB20000215 丁程

**1、三级模式结构在SQL中分别对应什么对象？三级模式结构在SQL中分别通过哪些DDL语句进行操纵？**
三级模式结构在数据库中通常指的是 ANSI/SPARC 三级模式架构，该架构把数据库管理系统划分为三个层次：外模式（用户视图）、概念模式（全局视图）和内模式（物理存储）。在 SQL 中，这三个层次分别对应以下对象：

外模式（用户视图）：这一层对应 SQL 中的视图（View）。视图是基于一张或多张基本表的虚拟表，它提供了一种自定义的数据查询和表示方式，使用户可以更加简便地访问底层数据。

概念模式（全局视图）：这一层对应 SQL 中的表（Table）。表是存储数据的基本结构，由行（记录）和列（字段）组成。概念模式描述了数据库中所有实体及其相互之间的关系。

内模式（物理存储）：这一层对应 SQL 中的存储结构和索引等。它主要描述了数据在数据库中的物理存储方式，例如存储空间、文件组织方式等。在 SQL 中，这层次的概念通常不直接暴露给开发者。

在 SQL 中，可以使用以下 DDL（数据定义语言）语句来操作这三级模式结构：

外模式（用户视图）：

创建视图：CREATE VIEW view_name AS SELECT ...
修改视图：ALTER VIEW view_name ...
删除视图：DROP VIEW view_name
概念模式（全局视图）：

创建表：CREATE TABLE table_name (column1 datatype, column2 datatype, ...)
修改表：ALTER TABLE table_name ...
删除表：DROP TABLE table_name
内模式（物理存储）：

在 SQL 中，内模式的操作通常是由 DBMS 自动处理的，因此，开发者不需要直接操纵内模式。但是，开发者可以通过优化 SQL 语句、创建和调整索引等方式，间接地影响内模式的物理存储结构。

**2.(1)请写出定义上述三个表的 create table 语句**
```sql
CREATE TABLE Student (
    sno CHAR(10) PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birthdate DATE
);

CREATE TABLE Course (
    cno CHAR(10) PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    type INT DEFAULT 0,
    credit FLOAT
);

CREATE TABLE SC (
    sno CHAR(10),
    cno CHAR(10),
    score FLOAT CHECK (score >= 0 AND score <= 100),
    term INT CHECK (term BETWEEN 1 AND 8),
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES Student(sno),
    FOREIGN KEY (cno) REFERENCES Course(cno)
);

```
**2.(2)**
1）
```sql
SELECT birthdate
FROM Student
WHERE sname = '张三';
```
2）
```sql
SELECT sno, sname, gender
FROM Student
WHERE sname LIKE '李%';
```
3）
```sql
SELECT s.sno, s.sname
FROM Student s
JOIN SC sc ON s.sno = sc.sno
JOIN Course c ON sc.cno = c.cno
WHERE c.type = 0 AND sc.score IS NULL
ORDER BY s.sno;
```
4）
```sql
SELECT s.sname
FROM Student s
JOIN SC sc ON s.sno = sc.sno
JOIN Course c ON sc.cno = c.cno
WHERE c.type = 0
GROUP BY s.sno, s.sname
HAVING SUM(c.credit) > 16 AND AVG(sc.score) >= 75;
```
5）
```sql
SELECT s.sno, s.sname
FROM Student s
WHERE NOT EXISTS (
    SELECT 1
    FROM Course c
    WHERE c.type = 2 AND NOT EXISTS (
        SELECT 1
        FROM SC sc
        WHERE sc.sno = s.sno AND sc.cno = c.cno AND sc.score >= 60
    )
);
```
6）
```sql
SELECT c.cno, c.cname, c.type,
       AVG(sc.score) AS avg_score,
       COUNT(CASE WHEN sc.score < 60 THEN 1 END) / COUNT(*) * 100 AS fail_rate
FROM Course c
JOIN SC sc ON c.cno = sc.cno
GROUP BY c.cno, c.cname, c.type
ORDER BY c.type;
```
7）
```sql
SELECT DISTINCT s.sno, s.sname, c.cno, c.cname
FROM Student s
JOIN SC sc ON s.sno = sc.sno
JOIN Course c ON sc.cno = c.cno
WHERE sc.score < 60 AND EXISTS (
    SELECT 1
    FROM SC sc2
    WHERE sc2.sno = s.sno AND sc2.cno = c.cno AND sc2.score < sc.score
);
```

**3.给定关系模式 R(A,B)、S(B,C)和 T(C,D)，已知有下面的关系代数表达式，其中 p 是 仅涉及属性 R.A 的谓词，q 是仅涉及 R.B 的谓词，m 是涉及仅 S.C 的谓词。请写出与此关系代数表达式对应的 SQL 查询语句：πD(σq(σp(R)⋈σm(S))⋈T)**

SQL查询语句如下：
```sql
SELECT DISTINCT T.D
FROM (
    SELECT R.A, R.B
    FROM R
    WHERE p
) AS filtered_R
JOIN (
    SELECT S.B, S.C
    FROM S
    WHERE m
) AS filtered_S ON filtered_R.B = filtered_S.B
JOIN T ON filtered_S.C = T.C
WHERE q;
```
