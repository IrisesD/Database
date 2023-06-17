from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, query
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:DCchengding2003@localhost/lab3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    
    db.session.commit()