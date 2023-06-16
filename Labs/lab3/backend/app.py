import re
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
    
with app.app_context():
    db.drop_all()
    db.create_all()

    # 预先在表中插入一些数据
    teacher1 = Teacher(id="00001", name="张三", gender=1, title=1)
    teacher2 = Teacher(id="00002", name="李四", gender=2, title=2)
    teacher3 = Teacher(id="00003", name="李五", gender=1, title=3)
    db.session.add_all([teacher1, teacher2, teacher3])
    
    paper1 = Paper(id=1, name="论文1", source="来源1", date="2021-01-01", type=1, level=1)
    paper2 = Paper(id=2, name="论文2", source="来源2", date="2021-01-02", type=2, level=2)
    paper3 = Paper(id=3, name="论文3", source="来源3", date="2021-01-03", type=3, level=3)
    db.session.add_all([paper1, paper2, paper3])
    
    project1 = Project(id="00001", name="项目1", source="来源1", type=1, fund=10000, begin_date="2021-01-01", end_date="2021-01-02")
    project2 = Project(id="00002", name="项目2", source="来源2", type=2, fund=20000, begin_date="2021-01-02", end_date="2021-01-03")
    project3 = Project(id="00003", name="项目3", source="来源3", type=3, fund=30000, begin_date="2021-01-03", end_date="2021-01-04")
    db.session.add_all([project1, project2, project3])
    
    course1 = Course(id="00001", name="课程1", hours=20, property=1)
    course2 = Course(id="00002", name="课程2", hours=60, property=2)
    course3 = Course(id="00003", name="课程3", hours=100, property=3)
    db.session.add_all([course1, course2, course3])
    
    paper_publish1 = PaperPublish(teacher_id="00001", paper_id=1, rank=1, corr=True)
    paper_publish2 = PaperPublish(teacher_id="00001", paper_id=2, rank=2, corr=False)
    paper_publish3 = PaperPublish(teacher_id="00002", paper_id=3, rank=3, corr=True)
    paper_publish4 = PaperPublish(teacher_id="00002", paper_id=1, rank=2, corr=False)
    paper_publish5 = PaperPublish(teacher_id="00003", paper_id=2, rank=3, corr=True)
    db.session.add_all([paper_publish1, paper_publish2, paper_publish3, paper_publish4, paper_publish5])
    
    project_participate1 = ProjectParticipate(teacher_id="00001", project_id="00001", rank=1, per_fund=7000)
    project_participate2 = ProjectParticipate(teacher_id="00001", project_id="00002", rank=2, per_fund=12000)
    project_participate3 = ProjectParticipate(teacher_id="00002", project_id="00003", rank=3, per_fund=30000)
    project_participate4 = ProjectParticipate(teacher_id="00002", project_id="00001", rank=2, per_fund=3000)
    project_participate5 = ProjectParticipate(teacher_id="00003", project_id="00002", rank=3, per_fund=8000)
    db.session.add_all([project_participate1, project_participate2, project_participate3, project_participate4, project_participate5])
    
    course_teach1 = CourseTeach(teacher_id="00001", course_id="00001", year=2020, term=1, per_hours=10)
    course_teach2 = CourseTeach(teacher_id="00001", course_id="00002", year=2020, term=1, per_hours=20)
    course_teach3 = CourseTeach(teacher_id="00002", course_id="00003", year=2020, term=1, per_hours=100)
    course_teach4 = CourseTeach(teacher_id="00002", course_id="00001", year=2020, term=1, per_hours=10)
    course_teach5 = CourseTeach(teacher_id="00003", course_id="00002", year=2020, term=1, per_hours=40)
    db.session.add_all([course_teach1, course_teach2, course_teach3, course_teach4, course_teach5])
    db.session.commit()

# teacher 查询
@app.route('/teacher', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    output = []
    for teacher in teachers:
        teacher_data = {}
        teacher_data['id'] = teacher.id
        teacher_data['name'] = teacher.name
        teacher_data['gender'] = teacher.gender
        teacher_data['title'] = teacher.title

        output.append(teacher_data)

    return jsonify({'teachers': output})

# teacher 增加
@app.route('/teacher', methods=['POST'])
def add_teacher():
    id = request.json['id']
    name = request.json['name']
    gender = request.json['gender']
    title = request.json['title']

    teacher = Teacher(id=id, name=name, gender=gender, title=title)

    db.session.add(teacher)
    db.session.commit()

    return jsonify({'result': 'success'})
    
# teacher 删除
@app.route('/teacher/<id>', methods=['DELETE'])
def delete_teacher():
    teacher = Teacher.query.get(id)
    db.session.delete(teacher)
    db.session.commit()

    return jsonify({'result': 'success'})
    
# teacher 修改
@app.route('/teacher', methods=['PUT'])
def update_teacher():
    teacher = Teacher.query.get(id)

    name = request.json['name']
    gender = request.json['gender']
    title = request.json['title']

    teacher.name = name
    teacher.gender = gender
    teacher.title = title

    db.session.commit()

    return jsonify({'result': 'success'})
    
# paper 查询
@app.route('/paper', methods=['GET'])
def get_papers():
    id = request.form.get('id')
    res = {}
    papers = PaperPublish.query.filter(PaperPublish.teacher_id == id).all()
    
    paper_data = []
    for paper in papers:
        paper_id = paper.paper_id
        paper_info = Paper.query.get(paper_id)
        paper_data.append({'id':paper_info.id, 'name':paper_info.name, 'source':paper_info.source, 'date':paper_info.date, 'type':paper_info.type, 'level':paper_info.level, 'author_rank':paper.rank, 'is_corr':paper.corr})
            
    res["papers"] = paper_data
    
    return render_template("paper_query.html", papers=paper_transform(paper_data))
    
# paper 增加
@app.route('/paper', methods=['POST'])
def add_paper():
    name = request.json['name']
    source = request.json['source']
    date = request.json['date']
    ptype = request.json['type']
    level = request.json['level']

    paper = Paper(id, name, source, date, ptype, level)
    
    db.session.add(paper)
    db.session.commit()
    
    teachers = request.json['teachers']
    for teacher in teachers:
        teacher_id = teacher['id']
        rank = teacher['rank']
        corr = teacher['corr']
        paper_publish = PaperPublish(teacher_id, id, rank, corr)
        db.session.add(paper_publish)
        db.session.commit()
    
    return jsonify({'result': 'success'})
    
# paper 删除
@app.route('/paper/<id>', methods=['DELETE'])
def delete_paper():
    paper = Paper.query.get(id)
    db.session.delete(paper)
    db.session.commit()

    return jsonify({'result': 'success'})
    
# paper 修改
@app.route('/paper', methods=['PUT'])
def update_paper():
    paper = Paper.query.get(id)

    name = request.json['name']
    source = request.json['source']
    date = request.json['date']
    ptype = request.json['type']
    level = request.json['level']

    paper.name = name
    paper.source = source
    paper.date = date
    paper.type = ptype
    paper.level = level

    db.session.commit()
    
    return jsonify({'result': 'success'})
        
# project 查询
@app.route('/project', methods=['GET'])
def get_projects():
    id = request.form.get('id')
    res = {}
    projects = ProjectParticipate.query.filter(ProjectParticipate.teacher_id == id and project_info.begin_date >= int(begin_date) and project_info.end_date <= int(end_date)).all()
    
    project_data = []
    for project in projects:
        project_id = project.project_id
        project_info = Project.query.get(project_id)
        project_data.append({'id':project_info.id, 'name':project_info.name, 'source':project_info.source, 'type':project_info.type, 'total_fund':project_info.fund, 'begin':project_info.begin_date, 'end':project_info.end_date, 'teacher_rank':project.rank, 'per_fund':project.per_fund})

    res["projects"] = project_data
    return render_template("project_query.html", project=project_transform(project_data))
    
# project 增加
@app.route('/project', methods=['POST'])
def add_project():
    id = request.json['id']
    name = request.json['name']
    source = request.json['source']
    ptype = request.json['type']
    fund = request.json['fund']
    begin_date = request.json['begin_date']
    end_date = request.json['end_date']

    project = Project(id, name, source, ptype, fund, begin_date, end_date)

    db.session.add(project)
    db.session.commit()
    
    teachers = request.json['teachers']
    for teacher in teachers:
        teacher_id = teacher['id']
        rank = teacher['rank']
        per_fund = teacher['per_fund']
        project_participate = ProjectParticipate(teacher_id, id, rank, per_fund)
        db.session.add(project_participate)
        db.session.commit()

    return jsonify({'result': 'success'})
    
# project 删除
@app.route('/project/<id>', methods=['DELETE'])
def delete_project():
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()

    return jsonify({'result': 'success'})
    
# project 修改
@app.route('/project', methods=['PUT'])
def update_project():
    project = Project.query.get(id)

    name = request.json['name']
    source = request.json['source']
    type = request.json['type']
    fund = request.json['fund']
    begin_date = request.json['begin_date']
    end_date = request.json['end_date']

    project.name = name
    project.source = source
    project.type = type
    project.fund = fund
    project.begin_date = begin_date
    project.end_date = end_date

    db.session.commit()

    return jsonify({'result': 'success'})
    
# course 查询
@app.route('/course/query', methods=['POST'])
def get_courses():
    id = request.form.get('id')
    res = {}
    courses = CourseTeach.query.filter(CourseTeach.teacher_id == id).all()
    
    course_data = []
    for course in courses:
        course_id = course.course_id
        course_info = Course.query.get(course_id)
        course_data.append({'id':course_info.id, 'name':course_info.name, 'hours':course_info.hours, 'year':course.year, 'term':course.term, 'per_hours':course.per_hours})
    res["courses"] = course_data

    return render_template('course_query.html', course=course_transform(res))
    
# course 增加
@app.route('/course', methods=['POST'])
def add_course():
    name = request.json['name']
    hours = request.json['hours']
    property = request.json['property']

    course = Course(name, hours, property)

    db.session.add(course)
    db.session.commit()
    
    teachers = request.json['teachers']
    for teacher in teachers:
        teacher_id = teacher['id']
        year = teacher['year']
        term = teacher['term']
        per_hours = teacher['per_hours']
        course_teach = CourseTeach(teacher_id, id, year, term, per_hours)
        db.session.add(course_teach)
        db.session.commit()

    return jsonify({'result': 'success'})
    
# course 删除
@app.route('/course/<id>', methods=['DELETE'])
def delete_course():
    course = Course.query.get(id)
    db.session.delete(course)
    db.session.commit()

    return jsonify({'result': 'success'})
    
# course 修改
@app.route('/course', methods=['PUT'])
def update_course():
    course = Course.query.get(id)

    name = request.json['name']
    hours = request.json['hours']
    property = request.json['property']

    course.name = name
    course.hours = hours
    course.property = property

    db.session.commit()

    return jsonify({'result': 'success'})
    
# 综合查询，根据teacher id和begin_date以及end_date查询所有信息
@app.route('/comp_query', methods=['POST'])
def comprehensive_query():
    id = request.form.get("id")
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

@app.route('/')
def test():
    return render_template('index.html')

@app.route('/', methods = ["GET","POST"])
def ret():
    if request.method == "POST":
        id = request.form.get("id")
        teacher = Teacher.query.get(id)
        return teacher.name



if __name__ == '__main__':
    app.run(debug=True)
    


