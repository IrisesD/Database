## 数据库大作业 实验报告

**PB20000215 丁程**

本实验为完成一个完整的包括前后端的数据库应用。
本项目使用B/S框架，后端使用Python Flask + SQLALCHEMY完成，前端使用HTML + Bootstrap样板库用于美化。

下面简要介绍代码框架：
Flask允许使用路由，即对于其前端返回的地址，编写自动相应函数，在函数中使用SQLALCHEMY对数据库中的数据进行操作，之后渲染一个前端网页返回给前端即可完成。
前端则是在每个组件的点击事件中设置相应的地址跳转（路由），这样产生的信息可以被后端得到，从而被自动相应函数操作。

下面分别以前端和后端的一段代码为例讲解：
后端：
```Python
# course 增加
@app.route('/course/add/po', methods=['POST'])
def add_course():
    course_id = request.form.get('course_id')
    year = request.form.get('year')
    term = request.form.get('term')
    # 判断course是否已经存在Course表中
    if Course.query.get(course_id) is None:
        return render_template("add_fail.html", msg="课程不存在")

    teachers = request.form.get('teachers')
    per_hours = request.form.get('per_hours')
    teachers = teachers.split(" ")
    per_hours = per_hours.split(" ")
    total_hours = Course.query.get(course_id).hours
    per_hours = [int(i) for i in per_hours]
    if sum(per_hours) != total_hours:
        return render_template("add_fail.html", msg="总课时不等于教师课时之和")
    if len(teachers) != len(per_hours):
        return render_template("add_fail.html", msg="教师id与课时数目不匹配")
    
    for teacher in teachers:
        teacher_id = teacher
        per_hour = per_hours[teachers.index(teacher)]
        course_teach = CourseTeach(teacher_id=teacher_id, course_id=course_id, year=year, term=term, per_hours=per_hour)
        db.session.add(course_teach)
        db.session.commit()

    return render_template("add_success.html")
```
这个函数最开始的`@app.route()`修饰符就是Flask自带的路由功能，其在前端路由为/course/add/po,methods="POST"时会自动执行该函数的操作。
这个函数从前端的表单form中得到相应信息，之后首先做一些错误处理，对诸如课程信息在数据库中不存在、总课时不等于教师课时之和、教师id和课程数目不匹配等问题返回对应的错误信息。
如果错误处理全部通过，则通过启用事务，在数据库中插入一条对应信息并提交，之后返回渲染过后的显示成功信息的网页。

前端：
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" 
rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" 
integrity="sha384-/mhDoLbDldZc3qpsJHpLogda//BVZbgYuw6kof4u2FrCedxOtgRZDTHgHUhOCVim" crossorigin="anonymous"></script>        
<h1 class="display-6">增加记录</h1>
<form action="/course/add/po", method='POST'>
            <div class="mb-3">
                <label for="exampleEmail1" class="form-label">Course ID</label>
                <input type="text" class="form-control" name="course_id">
              </div>
              <div class="mb-3">
                <label for="exampleEmail1" class="form-label">Year</label>
                <input type="text" class="form-control" name="year">
              </div>
              <div class="mb-3">
                <label for="exampleEmail1" class="form-label">Term</label>
                <select class="form-select" aria-label="Default select example" name="term">
                  <option selected>选择学期</option>
                  <option value="1">春季学期</option>
                  <option value="2">夏季学期</option>
                  <option value="3">秋季学期</option>
                </select>
              </div>
              <!--对多位作者的处理-->
              <div class="mb-3">
                <label for="exampleEmail1" class="form-label">Teacher ID(请按顺序输入老师工号,中间用空格隔开)</label>
                <input type="text" class="form-control" name="teachers">
              </div>
  
              <div class="mb-3">
                <label for="exampleEmail1" class="form-label">Burden Hours(请按顺序输入老师主讲学时)</label>
                <input type="text" class="form-control" name="per_hours">
              </div>
              <div class="col-12">
            <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </form>
        <a class="btn btn-primary" href="/course/show" role="button">返回上一页</a>
```
这里使用表单来提交信息到后端，使用CDN加载Bootstrap样板库使得页面更为美观，这里点击提交之后，路由会跳转到/course/add/po，对应刚刚提到的后端的自动相应程序，这样就能做到前后端统一，从而是应用达到想要的效果。

本项目做了较多错误处理，具体包括但不限于课程信息在数据库中不存在、总课时不等于教师课时之和、教师id和课程数目不匹配、教师id长度不为5、教师id不存在、经费总数与分担经费之和不匹配、项目不存在等等。在鲁棒性上做得较好，对于大部分输入能做到容错。

本项目使用方法：
在目录下使用
```shell
python3 app.py
```
在看到如下信息后：
```shell
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 126-109-513
```
即可在http://127.0.0.1:5000进行操作，这里注意如果5000端口已被绑定，可能需要手动kill占用5000端口的程序或者更改flask的相关配置，使得其使用其他未占用端口。