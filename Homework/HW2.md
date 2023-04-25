## 数据库 HW2

PB20000215 丁程

**1、三级模式结构在SQL中分别对应什么对象？三级模式结构在SQL中分别通过哪些DDL语句进行操纵？**


外模式：对应 SQL 中的视图。

概念模式：这一层对应 SQL 中的基本表。

内模式：这一层对应 SQL 中的文件和索引等存储方式。

在 SQL 中，可以使用以下 DDL（数据定义语言）语句来操作这三级模式结构：

外模式：
```
创建视图：CREATE VIEW
删除视图：DROP VIEW
```
概念模式：
```
创建表：CREATE TABLE
修改表：ALTER TABLE
删除表：DROP TABLE
```
内模式：
```
创建索引：CREATE INDEX
删除索引：DROP INDEX
```
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
    term INT CHECK (term >= 1 AND term <= 8),
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
SELECT Student.sno, Student.sname
FROM Student, Course, SC
WHERE Student.sno = SC.sno
	AND Course.cno = SC.cno
	AND Course.type = 0
	AND SC.score IS NULL
ORDER BY Student.sno;
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
SELECT sno, sname 
FROM Student
WHERE NOT EXISTS(
    SELECT * FROM Course WHERE TYPE = 2 AND NOT EXISTS(
        SELECT * FROM SC 
        WHERE sno = Student.sno 
        AND cno = Course.cno
        AND score >= 60
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
