import json
from flask import jsonify, request
from app.models.base import queryBySQL, db as DB
from app.models.task import task as TASK
from app.libs.redprint import Redprint
# from app.api.v1.job import scheduler
import json

api = Redprint('task')


@api.route('', methods=['GET'])
def get_task_list():
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    page = request.args.get('page') or '1'
    count = request.args.get('count') or '10'
    state = request.args.get('state')
    # check params
    if not page.isdigit():
        result["code"] = 0
        result["msg"] = "page not numbers"
        return jsonify(result)
    if not count.isdigit():
        result["code"] = 0
        result["msg"] = "count not numbers"
        return jsonify(result)

    start = (int(page) - 1) * int(count)
    sql = '''SELECT task_id, extent, user_id, state, created_at, updated_at from task WHERE 1=1 '''
    if state:
        sql = sql + " AND state={state}"
    sql = sql + ''' ORDER BY updated_at desc LIMIT {count} OFFSET {start}'''
    queryData = queryBySQL(sql.format(start=start, count=count))
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    rows = queryData.fetchall()
    result["data"] = rows

    return jsonify(result)


@api.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    # check params
    if not task_id.isdigit():
        result["code"] = 0
        result["msg"] = "task_id not numbers"
        return jsonify(result)

    sql = '''SELECT task_id, extent, user_id, state, created_at, updated_at from task  WHERE task_id = {task_id}'''
    queryData = queryBySQL(sql.format(task_id=task_id))
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    row = queryData.fetchone()
    result["data"] = row

    return jsonify(result)


@api.route('', methods=['POST'])
def create_task():
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    # check params
    paramsDic = request.json
    params = json.loads(json.dumps(paramsDic))
    extent = params['extent']
    user_id = params['user_id']

    # insert into
    with DB.auto_commit():
        task = TASK()
        task.extent = extent
        task.user_id = user_id
        DB.session.add(task)
        return jsonify(result)


@api.route('/<task_id>', methods=['POST'])
def update_task(task_id):
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    # check params
    if not task_id.isdigit():
        result["code"] = 0
        result["msg"] = "task_id not numbers"
        return jsonify(result)
    paramsDic = request.json
    params = json.loads(json.dumps(paramsDic))

    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        if 'extent' in params:
            task.extent = params['extent']
        if 'user_id' in params:
            task.user_id = params['user_id']
        if 'state' in params:
            task.state = params['state']
        if 'status' in params:
            task.status = params['status']
        DB.session.add(task)
        return jsonify(result)


@api.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    # check params
    if not task_id.isdigit():
        result["code"] = 0
        result["msg"] = "task_id not numbers"
        return jsonify(result)

    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        task.delete()
        return jsonify(result)

# for scheduler job


def get_one_job():
    sql = '''SELECT task_id, extent, user_id, state, created_at, updated_at from task WHERE STATE =1 ORDER BY created_at ASC LIMIT 1'''
    queryData = queryBySQL(sql)
    row = queryData.fetchone()


def start_job(task_id):
    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        if task:
            task.state = 2
            DB.session.add(task)


def done_job(task_id):
    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        if task:
            task.state = 3
            DB.session.add(task)
