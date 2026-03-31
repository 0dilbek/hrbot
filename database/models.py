from tortoise import Model, fields
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

class TgUser(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField(unique=True)
    
    full_name = fields.CharField(max_length=255)
    phone_numbers = fields.JSONField(default=[])
    
    birth_date = fields.DateField()
    born_address = fields.CharField(max_length=255)
    live_address = fields.CharField(max_length=255)
    work_or_study_address = fields.CharField(max_length=255)
    where_find_us = fields.CharField(max_length=255, null=True, blank=True)
    branch = fields.CharField(max_length=255)

    profile_pic_file_id = fields.CharField(max_length=255, null=True, blank=True)
    profile_pic_path = fields.CharField(max_length=255, null=True, blank=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "tg_users"

    def __str__(self):
        return self.full_name

class TeacherResume(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.TgUser', related_name='resumes')
    subject = fields.CharField(max_length=255)
    university = fields.CharField(max_length=255)
    experience = fields.CharField(max_length=255)
    working_time = fields.CharField(max_length=255)
    position = fields.CharField(max_length=255)
    salary = fields.CharField(max_length=255)
    sertificates = fields.JSONField(default=[])
    last_work_place = fields.CharField(max_length=255)
    why_leave_work = fields.CharField(max_length=255)
    last_work_place_phone = fields.CharField(max_length=255)
    why_choice_us = fields.CharField(max_length=255)


    created_at = fields.DatetimeField(default=utcnow)
    
    class Meta:
        table = "teacher_resumes"

    def __str__(self):
        return self.subject

class AdminsResume(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.TgUser', related_name='admins_resumes')
    job = fields.CharField(max_length=255)
    foreign_languages = fields.JSONField(default=[])
    experience = fields.CharField(max_length=255)
    working_time = fields.CharField(max_length=255)
    last_work_place = fields.CharField(max_length=255)
    why_leave_work = fields.CharField(max_length=255)
    last_work_place_phone = fields.CharField(max_length=255)
    why_choice_us = fields.CharField(max_length=255)

    created_at = fields.DatetimeField(default=utcnow)
    
    class Meta:
        table = "admins_resumes"

    def __str__(self):
        return self.job

class VacanciesText(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    text = fields.TextField()
    last_text = fields.TextField(default="")

    class Meta:
        table = "vacancies_text"

    def __str__(self):
        return self.name

class Subjects(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    
class Sertificates(Model):
    id = fields.IntField(pk=True)
    subject = fields.ForeignKeyField('models.Subjects', related_name='sertificates')
    name = fields.CharField(max_length=255)
    ball_list = fields.JSONField(default=[])
    
class Quizs(Model):
    id = fields.IntField(pk=True)
    subject = fields.ForeignKeyField('models.Subjects', related_name='quizs')
    quizs = fields.JSONField(default=[])
    
class QuizAnswers(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.TgUser', related_name='quiz_answers')
    quiz = fields.ForeignKeyField('models.Quizs', related_name='quiz_answers')
    correct_answers = fields.IntField(default=0)
    