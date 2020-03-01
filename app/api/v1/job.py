import json
from flask import jsonify, request
from flask_apscheduler import APScheduler
from app.models.base import queryBySQL, db as DB
from app.api.v1 import task
from app.libs.redprint import Redprint
import json

api = Redprint('job')

scheduler = APScheduler()


# @scheduler.task(trigger='interval', id='task_job', seconds=5)
# def task_job():
#     task.start_job(2)
#     print('hello world')


@api.route('/pause', methods=['GET'])
def pause_job():  # 暂停
    job_id = request.args.get('id')
    scheduler.pause_job(str(job_id))
    return "pause success!"


@api.route('/resume', methods=['GET'])
def resume_job():  # 恢复
    job_id = request.args.get('id')
    scheduler.resume_job(str(job_id))
    return "Success!"


@api.route('/get_jobs', methods=['GET'])
def get_task():  # 获取
    # job_id = request.args.get('id')
    jobs = scheduler.get_jobs()
    print(jobs)
    return 'jobs:'+str(jobs)


@api.route('/remove_job', methods=['GET'])
def remove_job():  # 移除
    job_id = request.args.get('id')
    scheduler.remove_job(str(job_id))
    return 'remove success'

# /add_job?id=2
@api.route('/add_job', methods=['GET'])
def add_task():
    data = request.args.get('id')
    if data == '1':
        # trigger='cron' 表示是一个定时任务
        scheduler.add_job(func=task_job, id='1', args=(1, 1), trigger='cron', day_of_week='0-6', hour=18, minute=24,
                          second=10, replace_existing=True)
    return 'sucess'
