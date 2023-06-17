from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, query
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:DCchengding2003@localhost/lab3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def info_transform(output):
    gend = ""
    if output["teacher"]["gender"] == 1:
        gend = "男"
    else:
        gend = "女"
    # 1-博士后，2-助教，3-讲师，4-副教授，5-特任教授，6-教授，
    #7-助理研究员，8-特任副研究员，9-副研究员，10-特任研究员，11-研究员\
    title = ""
    if output["teacher"]["title"] == 1:
        title = "博士后"
    elif output["teacher"]["title"] == 2:
        title = "助教"
    elif output["teacher"]["title"] == 3:
        title = "讲师"
    elif output["teacher"]["title"] == 4:
        title = "副教授"
    elif output["teacher"]["title"] == 5:
        title = "特任教授"
    elif output["teacher"]["title"] == 6:
        title = "教授"
    elif output["teacher"]["title"] == 7:
        title = "助理研究员"
    elif output["teacher"]["title"] == 8:
        title = "特任副研究员"
    elif output["teacher"]["title"] == 9:
        title = "副研究员"
    elif output["teacher"]["title"] == 10:
        title = "特任研究员"
    elif output["teacher"]["title"] == 11:
        title = "研究员"
    info = ''
    info += '<thead>' + '\n' + '<tr>\n' + '<th scope="col">工号</th>\n'+ '<th scope="col">姓名</th>\n' + '<th scope="col">性别</th>\n'+\
        '<th scope="col">职称</th>\n'+ '</tr>\n'+ '</thead>\n'
    info += f'<tbody>\n<tr>\n<th scope="row">{output["teacher"]["id"]}</th>\n<td>{output["teacher"]["name"]}</td>\n\
      <td>{gend}</td>\n<td>{title}</td>\n</tr>\n'
    info += "</tbody>"
    return info

def course_transform(output):
    
    info = ''
    info += '<thead>' + '\n' + '<tr>\n' + '<th scope="col">课程号</th>\n'+ '<th scope="col">课程名</th>\n' + '<th scope="col">主讲学时</th>\n'+\
        '<th scope="col">学期</th>\n'+ '</tr>\n'+ '</thead>\n'
    for course in output['courses']:
        term = ""
        if course['term'] == 1:
            term = "春"
        elif course['term'] == 2:
            term = "夏"
        elif course['term'] == 3:
            term = "秋"
        info += f'<tbody>\n<tr>\n<th scope="row">{course["id"]}</th>\n<td>{course["name"]}</td>\n\
            <td>{course["per_hours"]}</td>\n<td>{course["year"]}{term}</td>\n</tr>\n'
        info += "</tbody>"
    return info

def paper_transform(output):
    
    info = ''
    info += '<thead>' + '\n' + '<tr>\n' + '<th scope="col">论文名称</th>\n'+ '<th scope="col">发表源</th>\n' + '<th scope="col">时间</th>\n'+\
        '<th scope="col">等级</th>\n'+ '<th scope="col">排名</th>\n'+'<th scope="col">是否是通讯</th>\n'+'</tr>\n'+ '</thead>\n'
    for paper in output['papers']:
        # 1-CCF-A，2-CCF-B，3-CCF-C，4-中文 CCF-A，5-中文 CCF-B，6-无级别
        level = ""
        if paper['level'] == 1:
            level = "CCF-A"
        elif paper['level'] == 2:
            level = "CCF-B"
        elif paper['level'] == 3:
            level = "CCF-C"
        elif paper['level'] == 4:
            level = "中文 CCF-A"
        elif paper['level'] == 5:
            level = "中文 CCF-B"
        elif paper['level'] == 6:
            level = "无级别"
        if paper['is_corr'] == True:
            is_c = "是"
        else:
            is_c = "否"
        info += f'<tbody>\n<tr>\n<th scope="row">{paper["name"]}</th>\n<td>{paper["source"]}</td>\n\
            <td>{paper["date"]}</td>\n<td>{level}</td>\n<td>{paper["author_rank"]}</td>\n<td>{is_c}</td>\n</tr>\n'
        info += "</tbody>"
    return info

def project_transform(output):
    
    info = ''
    info += '<thead>' + '\n' + '<tr>\n' + '<th scope="col">项目名称</th>\n'+ '<th scope="col">项目来源</th>\n' + '<th scope="col">项目类型</th>\n'+\
        '<th scope="col">项目时间</th>\n'+ '<th scope="col">总经费</th>\n'+'<th scope="col">承担经费</th>\n'+'</tr>\n'+ '</thead>\n'
    for project in output['projects']:
        # 项目类型为整数：1-国家级项目，2-省部级项目，3-市厅级项目，4-企业合作项目，5-其它类型项目。
        ptype = ""
        if project['type'] == 1:
            ptype = "国家级项目"
        elif project['type'] == 2:
            ptype = "省部级项目"
        elif project['type'] == 3:
            ptype = "市厅级项目"
        elif project['type'] == 4:
            ptype = "企业合作项目"
        elif project['type'] == 5:
            ptype = "其它类型项目"
        info += f'<tbody>\n<tr>\n<th scope="row">{project["name"]}</th>\n<td>{project["source"]}</td>\n\
            <td>{ptype}</td>\n<td>{project["begin"]}-{project["end"]}</td>\n<td>{project["total_fund"]}</td>\n<td>{project["per_fund"]}</td>\n</tr>\n'
        info += "</tbody>"
    return info

class Teacher(db.Model):
    __tablename__ = 'teacher'
    
    id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(256))    
    gender = db.Column(db.Integer)
    title = db.Column(db.Integer)

class Paper(db.Model):
    __tablename__ = 'paper'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    source = db.Column(db.String(256))
    date = db.Column(db.Date)
    type = db.Column(db.Integer)
    level = db.Column(db.Integer)

class Project(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    source = db.Column(db.String(256))
    type = db.Column(db.Integer)
    fund = db.Column(db.Float)
    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256))
    hours = db.Column(db.Integer)
    property = db.Column(db.Integer)
    
class PaperPublish(db.Model):
    __tablename__ = 'paper_publish'
    teacher_id = db.Column(db.String(5), primary_key=True)
    paper_id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    corr = db.Column(db.Boolean)
    
class ProjectParticipate(db.Model):
    __tablename__ = 'project_participate'
    teacher_id = db.Column(db.String(5), primary_key=True)
    project_id = db.Column(db.String(256), primary_key=True)
    rank = db.Column(db.Integer)
    per_fund = db.Column(db.Float)
    
class CourseTeach(db.Model):
    __tablename__ = 'course_teach'
    teacher_id = db.Column(db.String(5), primary_key=True)
    course_id = db.Column(db.String(256), primary_key=True)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    per_hours = db.Column(db.Integer)
    
# paper 查询
@app.route('/paper/query', methods=['POST'])
def get_papers():
    id = request.form.get('id')
    res = {}
    papers = PaperPublish.query.filter(PaperPublish.teacher_id == id).all()
    if Teacher.query.get(id) is None:
        return render_template("get_fail.html", msg = "教师不存在")
    paper_data = []
    for paper in papers:
        paper_id = paper.paper_id
        paper_info = Paper.query.get(paper_id)
        paper_data.append({'id':paper_info.id, 'name':paper_info.name, 'source':paper_info.source, 'date':paper_info.date, 'type':paper_info.type, 'level':paper_info.level, 'author_rank':paper.rank, 'is_corr':paper.corr})
            
    res["papers"] = paper_data
    
    return render_template("paper_query.html", paper=paper_transform(res))
    
# paper 增加
@app.route('/paper/add/po', methods=['POST'])
def add_paper():
    id = request.form.get('paper_id')
    name = request.form.get('paper_name')
    source = request.form.get('source')
    date = request.form.get('date')
    ptype = request.form.get('ptype')
    level = request.form.get('level')

    paper = Paper(id=id, name=name, source=source, date=date, type=ptype, level=level)
    
    db.session.add(paper)
    db.session.commit()
    
    teachers = request.form.get('teachers')
    corr = request.form.get('corre')
    teachers = teachers.split(" ")
    rank = 0
    for teacher in teachers:
        # 判断teacher是否已经存在Teacher表中
        if len(teacher) != 5:
            return render_template("add_fail.html", msg="教师id长度不为5")
        if Teacher.query.get(teacher) is None:
            return render_template("add_fail.html", msg="教师id不存在")
        rank += 1
        teacher_id = teacher
        if teacher_id == corr:
            corr = True
        else:
            corr = False
        paper_publish = PaperPublish(teacher_id=teacher_id, paper_id=id, rank=rank, corr=corr)
        db.session.add(paper_publish)
        db.session.commit()
    
    return render_template("add_success.html")
    
# paper 删除
@app.route('/paper/delete/po', methods=['POST'])
def delete_paper():
    paper_id = request.form.get('paper_id')
    if Paper.query.get(paper_id) is None:
        return render_template("delete_fail.html", msg="论文不存在")
    deletePaper = Paper.query.get(paper_id)
    db.session.delete(deletePaper)
    db.session.commit()
    deletePaperPub = PaperPublish.query.filter(PaperPublish.paper_id == paper_id).all()
    for paperPub in deletePaperPub:
        db.session.delete(paperPub)
        db.session.commit()
    
    return render_template("delete_success.html")
    
# paper 修改
@app.route('/paper/update/po', methods=['POST'])
def update_paper():
    id = request.form.get('paper_id')
    if Paper.query.get(id) is None:
        return render_template("update_fail.html", msg="论文不存在")
    deletePaper = Paper.query.get(id)
    db.session.delete(deletePaper)
    deletePaperPub = PaperPublish.query.filter(PaperPublish.paper_id == id).all()
    for paperPub in deletePaperPub:
        db.session.delete(paperPub)
        db.session.commit()
    
    name = request.form.get('paper_name')
    source = request.form.get('source')
    date = request.form.get('date')
    ptype = request.form.get('ptype')
    level = request.form.get('level')

    paper = Paper(id=id, name=name, source=source, date=date, type=ptype, level=level)
    
    db.session.add(paper)
    db.session.commit()
    
    teachers = request.form.get('teachers')
    corr = request.form.get('corre')
    teachers = teachers.split(" ")
    rank = 0
    for teacher in teachers:
        # 判断teacher是否已经存在Teacher表中
        if len(teacher) != 5:
            return render_template("update_fail.html", msg="教师id长度不为5")
        if Teacher.query.get(teacher) is None:
            return render_template("update_fail.html", msg="教师id不存在")
        rank += 1
        teacher_id = teacher
        if teacher_id == corr:
            corr = True
        else:
            corr = False
        paper_publish = PaperPublish(teacher_id=teacher_id, paper_id=id, rank=rank, corr=corr)
        db.session.add(paper_publish)
        db.session.commit()
    
    return render_template("update_success.html")
        
# project 查询
@app.route('/project/query', methods=['POST'])
def get_projects():
    id = request.form.get('id')
    res = {}
    if Teacher.query.get(id) is None:
        return render_template("get_fail.html", msg = "教师不存在")
    projects = ProjectParticipate.query.filter(ProjectParticipate.teacher_id == id and project_info.begin_date >= int(begin_date) and project_info.end_date <= int(end_date)).all()
    
    project_data = []
    for project in projects:
        project_id = project.project_id
        project_info = Project.query.get(project_id)
        project_data.append({'id':project_info.id, 'name':project_info.name, 'source':project_info.source, 'type':project_info.type, 'total_fund':project_info.fund, 'begin':project_info.begin_date, 'end':project_info.end_date, 'teacher_rank':project.rank, 'per_fund':project.per_fund})

    res["projects"] = project_data
    return render_template("project_query.html", project=project_transform(res))
    
# project 增加
@app.route('/project/add/po', methods=['POST'])
def add_project():
    id = request.form.get('project_id')
    name = request.form.get('project_name')
    source = request.form.get('source')
    ptype = request.form.get('ptype')
    begin_date = request.form.get('begin_date')
    end_date = request.form.get('end_date')
    total_fund = request.form.get('total_fund')

    project = Project(id=id, name=name, source=source, type=ptype, fund=total_fund, begin_date=begin_date, end_date=end_date)
    
    db.session.add(project)
    db.session.commit()
    
    teachers = request.form.get('teachers')
    per_fund = request.form.get('per_fund')
    teachers = teachers.split(" ")
    per_fund = per_fund.split(" ")
    per_fund = [float(i) for i in per_fund]
    if (sum(per_fund) - float(total_fund)) > 0.0001:
        return render_template("add_fail.html", msg="经费总数与分担经费之和不匹配")
    if len(teachers) != len(per_fund):
        return render_template("add_fail.html", msg="教师id与经费数目不匹配")
    for teacher in teachers:
        # 判断teacher是否已经存在Teacher表中
        if len(teacher) != 5:
            return render_template("add_fail.html", msg="教师id长度不为5")
        if Teacher.query.get(teacher) is None:
            return render_template("add_fail.html", msg="教师id不存在")
        teacher_id = teacher
        project_par = ProjectParticipate(teacher_id=teacher_id, project_id=id, per_fund=per_fund[teachers.index(teacher)])
        db.session.add(project_par)
        db.session.commit()
    
    return render_template("add_success.html")
    
# project 删除
@app.route('/project/delete/po', methods=['POST'])
def delete_project():
    project_id = request.form.get('project_id')
    if Project.query.get(project_id) is None:
        return render_template("delete_fail.html", msg="项目不存在")
    deleteProject = Project.query.get(project_id)
    db.session.delete(deleteProject)
    db.session.commit()
    deleteProjectPar = ProjectParticipate.query.filter(ProjectParticipate.project_id == project_id).all()
    for projectPar in deleteProjectPar:
        db.session.delete(projectPar)
        db.session.commit()
    
    return render_template("delete_success.html")
    
# project 修改
@app.route('/project/update/po', methods=['POST'])
def update_project():
    id = request.form.get('project_id')
    if Project.query.get(id) is None:
        return render_template("update_fail.html", msg="项目不存在")
    deleteProject = Project.query.get(id)
    db.session.delete(deleteProject)
    db.session.commit()
    deleteProjectPar = ProjectParticipate.query.filter(ProjectParticipate.project_id == id).all()
    for projectPar in deleteProjectPar:
        db.session.delete(projectPar)
        db.session.commit()
    
    name = request.form.get('project_name')
    source = request.form.get('source')
    ptype = request.form.get('ptype')
    begin_date = request.form.get('begin_date')
    end_date = request.form.get('end_date')
    total_fund = request.form.get('total_fund')

    project = Project(id=id, name=name, source=source, type=ptype, fund=total_fund, begin_date=begin_date, end_date=end_date)
    
    db.session.add(project)
    db.session.commit()
    
    teachers = request.form.get('teachers')
    per_fund = request.form.get('per_fund')
    teachers = teachers.split(" ")
    per_fund = per_fund.split(" ")
    if len(teachers) != len(per_fund):
        return render_template("add_fail.html", msg="教师id与经费数目不匹配")
    for teacher in teachers:
        # 判断teacher是否已经存在Teacher表中
        if len(teacher) != 5:
            return render_template("add_fail.html", msg="教师id长度不为5")
        if Teacher.query.get(teacher) is None:
            return render_template("add_fail.html", msg="教师id不存在")
        teacher_id = teacher
        project_par = ProjectParticipate(teacher_id=teacher_id, project_id=id, per_fund=per_fund[teachers.index(teacher)])
        db.session.add(project_par)
        db.session.commit()
    
    return render_template("add_success.html")
    
# course 查询
@app.route('/course/query', methods=['POST'])
def get_courses():
    id = request.form.get('id')
    res = {}
    if Teacher.query.get(id) is None:
        return render_template("get_fail.html", msg = "教师不存在")
    courses = CourseTeach.query.filter(CourseTeach.teacher_id == id).all()
    
    course_data = []
    for course in courses:
        course_id = course.course_id
        course_info = Course.query.get(course_id)
        course_data.append({'id':course_info.id, 'name':course_info.name, 'hours':course_info.hours, 'year':course.year, 'term':course.term, 'per_hours':course.per_hours})
    res["courses"] = course_data

    return render_template('course_query.html', course=course_transform(res))
    
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
    
# course 删除
@app.route('/course/delete/po', methods=['POST'])
def delete_course():
    course_id = request.form.get('course_id')
    if Course.query.get(course_id) is None:
        return render_template("delete_fail.html", msg="课程不存在")
    deleteCourseTeach = CourseTeach.query.filter(CourseTeach.course_id == course_id).all()
    for course in deleteCourseTeach:
        db.session.delete(course)
        db.session.commit()

    return render_template("delete_success.html")
    
# course 修改
@app.route('/course/update/po', methods=['POST'])
def update_course():
    course_id = request.form.get('course_id')
    year = request.form.get('year')
    term = request.form.get('term')
    deleteCourse = CourseTeach.query.filter(CourseTeach.course_id == course_id, CourseTeach.year == year, CourseTeach.term == term).all()
    
    for course in deleteCourse:
        db.session.delete(course)
        db.session.commit()
    # 判断course是否已经存在Course表中
    if Course.query.get(course_id) is None:
        return render_template("update_fail.html", msg="课程不存在")

    teachers = request.form.get('teachers')
    per_hours = request.form.get('per_hours')
    teachers = teachers.split(" ")
    per_hours = per_hours.split(" ")
    total_hours = Course.query.get(course_id).hours
    per_hours = [int(i) for i in per_hours]
    if sum(per_hours) != total_hours:
        return render_template("update_fail.html", msg="总课时不等于教师课时之和")
    if len(teachers) != len(per_hours):
        return render_template("update_fail.html", msg="教师id与课时数目不匹配")
    
    for teacher in teachers:
        teacher_id = teacher
        per_hour = per_hours[teachers.index(teacher)]
        course_teach = CourseTeach(teacher_id=teacher_id, course_id=course_id, year=year, term=term, per_hours=per_hour)
        db.session.add(course_teach)
        db.session.commit()

    return render_template("update_success.html")
    
# 综合查询，根据teacher id和begin_date以及end_date查询所有信息
@app.route('/comp_query', methods=['POST'])
def comprehensive_query():
    id = request.form.get("id")
    if len(id) != 5:
        return render_template("query_fail.html", msg="教师id长度不为5")
    if Teacher.query.get(id) is None:
        return render_template("query_fail.html", msg="教师不存在")
    begin_date = request.form.get('begin_date')
    end_date = request.form.get('end_date')
    output = {}
    # 查询教师信息
    teacher = Teacher.query.get(id)
    teacher_data = {}
    teacher_data['id'] = teacher.id
    teacher_data['name'] = teacher.name
    teacher_data['gender'] = teacher.gender
    teacher_data['title'] = teacher.title
    
    # 查询老师所教课程信息
    courses = CourseTeach.query.filter(CourseTeach.teacher_id == id and course.year >= int(begin_date) and course.year <= int(end_date)).all()
    
    course_data = []
    for course in courses:
        course_id = course.course_id
        course_info = Course.query.get(course_id)
        course_data.append({'id':course_info.id, 'name':course_info.name, 'hours':course_info.hours, 'year':course.year, 'term':course.term, 'per_hours':course.per_hours})
    
    # 查询老师所发表论文信息
    papers = PaperPublish.query.filter(PaperPublish.teacher_id == id and paper_info.date >= int(begin_date) and paper_info.date <= int(end_date)).all()
    
    paper_data = []
    for paper in papers:
        paper_id = paper.paper_id
        paper_info = Paper.query.get(paper_id)
        paper_data.append({'id':paper_info.id, 'name':paper_info.name, 'source':paper_info.source, 'date':paper_info.date, 'type':paper_info.type, 'level':paper_info.level, 'author_rank':paper.rank, 'is_corr':paper.corr})
            
    # 查询老师所参与的项目信息
    projects = ProjectParticipate.query.filter(ProjectParticipate.teacher_id == id and project_info.begin_date >= int(begin_date) and project_info.end_date <= int(end_date)).all()
    
    project_data = []
    for project in projects:
        project_id = project.project_id
        project_info = Project.query.get(project_id)
        project_data.append({'id':project_info.id, 'name':project_info.name, 'source':project_info.source, 'type':project_info.type, 'total_fund':project_info.fund, 'begin':project_info.begin_date, 'end':project_info.end_date, 'teacher_rank':project.rank, 'per_fund':project.per_fund})
    
    output['teacher'] = teacher_data
    output['courses'] = course_data
    output['papers'] = paper_data
    output['projects'] = project_data
    

    return render_template('query.html', info=info_transform(output), course=course_transform(output), paper=paper_transform(output), project=project_transform(output))

@app.route('/comp_query/show', methods=['GET'])
def show_html():
    return render_template('query_show.html')

@app.route('/paper/show', methods=['GET'])
def paper_show_html():
    return render_template('paper_show.html')

@app.route('/project/show', methods=['GET'])
def project_show_html():
    return render_template('project_show.html')

@app.route('/course/show', methods=['GET'])
def course_show_html():
    return render_template('course_show.html')

@app.route('/course/get', methods=['GET'])
def course_get_html():
    return render_template('course_get.html')

@app.route('/project/get', methods=['GET'])
def project_get_html():
    return render_template('project_get.html')

@app.route('/paper/get', methods=['GET'])
def paper_get_html():
    return render_template('paper_get.html')

@app.route('/paper/add', methods=['GET'])
def paper_add_html():
    return render_template('paper_add.html')

@app.route('/project/add', methods=['GET'])
def project_add_html():
    return render_template('project_add.html')

@app.route('/course/add', methods=['GET'])
def course_add_html():
    return render_template('course_add.html')

@app.route('/paper/delete', methods=['GET'])
def paper_delete_html():
    return render_template('paper_delete.html')

@app.route('/paper/update', methods=['GET'])
def paper_update_html():
    return render_template('paper_update.html')

@app.route('/course/delete', methods=['GET'])
def course_delete_html():
    return render_template('course_delete.html')

@app.route('/course/update', methods=['GET'])
def course_update_html():
    return render_template('course_update.html')

@app.route('/project/delete', methods=['GET'])
def project_delete_html():
    return render_template('project_delete.html')

@app.route('/project/update', methods=['GET'])
def project_update_html():
    return render_template('project_update.html')

@app.route('/')
def index_show():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)