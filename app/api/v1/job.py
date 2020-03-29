from flask import jsonify, request
from flask_apscheduler import APScheduler
import json
from app.models.base import queryBySQL, db as DB
from app.api.v1 import task as TASK, predict as PREDICT
from app.libs.redprint import Redprint

api = Redprint('job')

scheduler = APScheduler()


@scheduler.task(trigger='interval', id='predict_job', seconds=5)
def task_job():
    # check doing failed job.
    TASK.job_listen()

    # check doing job by this server
    isDoingJob = TASK.doing_job()
    if isDoingJob:
        return

    # get one new job
    newTask = TASK.get_one_job()
    if not newTask:
        return

    # start one job
    print("start one job.")
    TASK.do_job(newTask.task_id, 2)  # update task state
    # do the predict by robosat
    result = PREDICT.predict_job(newTask)

    if result['code'] == 0:
        TASK.do_job(newTask.task_id, 4)  # 任务失败
        print('job faild！')
    else:
        TASK.do_job(newTask.task_id, 3)  # 任务完成并修改完成时间
        print('job success!')


@api.route('/pause', methods=['GET'])
def pause_job(id):  # 暂停
    job_id = request.args.get('id') or id
    scheduler.pause_job(str(job_id))
    return "pause success!"


@api.route('/resume', methods=['GET'])
def resume_job(id):  # 恢复
    job_id = request.args.get('id') or id
    scheduler.resume_job(str(job_id))
    return "resume success!"


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
    return 'add job success'
