import json
from flask import jsonify, request
from app.models.base import queryBySQL, db as DB
from app.models.task import task as TASK
from app.libs.redprint import Redprint
from app.config import setting as CONFIG
from app.api.v1 import tools as TOOLS
import json
import time

api = Redprint('task')

# create task
@api.route('', methods=['POST'])
def create_task():
    result = {
        "code": 1,
        "data": None,
        "msg": "修改或创建成功！"
    }
    # check params
    if not request.json:
        result["code"] = 0
        result["msg"] = "参数解析错误"
        return jsonify(result)
    paramsDic = request.json
    params = json.loads(json.dumps(paramsDic))

    if result["code"] == 0:
        return result
    if 'task_id' in params:
        task_ids = params['task_id']
        if not isinstance(task_ids, list):
            result['code'] = 0
            result['msg'] = '任务列表参数不是数组。'
            return jsonify(result)
        if ('state' not in params and 'status' not in params) or ('state' in params and 'status' in params):
            result['code'] = 0
            result['msg'] = '不支持的修改。'
            return jsonify(result)
        for task_id in task_ids:
            task = TASK.query.filter_by(task_id=task_id).first_or_404()
            if not task:
                continue
            if 'state' in params:
                task.state = params['state']
            if 'status' in params:
                task.status = params['status']
            with DB.auto_commit():
                DB.session.add(task)
        return jsonify(result)
    else:
        if 'extent' not in params or 'user_id' not in params or 'area_code' not in params:
            result['code'] = 0
            result['msg'] = '缺少必要的参数。'
            return jsonify(result)
        extent = params['extent']
        user_id = params['user_id']
        area_code = params['area_code']
        with DB.auto_commit():
            task = TASK()
            task.extent = extent
            task.user_id = user_id
            task.area_code = area_code
            DB.session.add(task)
            return jsonify(result)

# get task list of {count}rows or {page}pages
@api.route('', methods=['GET'])
def get_task_list():
    result = {
        "code": 1,
        "data": None,
        "msg": "获取列表成功"
    }
    # code = request.args.get('code')
    page = request.args.get('page') or '1'
    count = request.args.get('count') or '10'
    # state = request.args.get('state')
    area_code = request.args.get('area_code')
    user_id = request.args.get('user_id')
    # check params
    if not page.isdigit():
        result["code"] = 0
        result["msg"] = "page not numbers"
        return jsonify(result)
    if not count.isdigit():
        result["code"] = 0
        result["msg"] = "count not numbers"
        return jsonify(result)
    # if not state.isdigit():
    #     result["code"] = 0
    #     result["msg"] = "state not numbers"
    #     return jsonify(result)
    if not area_code.isdigit():
        result["code"] = 0
        result["msg"] = "area_code not numbers"
        return jsonify(result)
    if not user_id.isdigit():
        result["code"] = 0
        result["msg"] = "user_id not numbers"
        return jsonify(result)
    # 查询该用户所有任务
    start = (int(page) - 1) * int(count)
    sql = '''SELECT task_id, extent, user_id, area_code, state, created_at, updated_at from task WHERE 1=1 '''
    # if state:
    #     sql = sql + ''' AND state='''+"'"+state+"'"
    if user_id:
        sql = sql + ''' AND user_id='''+"'"+user_id+"'"
    if area_code:
        sql = sql + ''' AND area_code='''+"'"+area_code+"'"
    sql = sql + ''' ORDER BY updated_at desc LIMIT {count} OFFSET {start}'''
    queryData = queryBySQL(sql.format(start=start, count=count))  # 参数format
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    rows = queryData.fetchall()
    # 查询目前排队情况
    sql_order = '''select task_id from task where state = 1 ORDER BY task_id LIMIT 1'''
    queryData_order = queryBySQL(sql_order)  # 参数format
    first_task = queryData_order.fetchone()
    if first_task:
        first_id = first_task.task_id
        tasks = []
        for row in rows:
            d = dict(row.items())
            if row.state == 1:
                d['rank'] = row.task_id - first_id + 1
            else:
                d['rank'] = None
            tasks.append(d)
        result['data'] = tasks
    else:
        result["data"] = rows

    return jsonify(result)

# get job in line
@api.route('/count', methods=['GET'])
def get_job_num():
    result = {
        "code": 1,
        "data": None,
        "msg": "任务数量查询成功"
    }
    sql = '''SELECT count(*) from task WHERE state = 1 or state =2'''
    queryData = queryBySQL(sql)
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    rows = queryData.fetchall()
    result["data"] = rows

    return jsonify(result)

# get job in line
@api.route('/job_id', methods=['GET'])
def get_processing_job():
    result = {
        "code": 1,
        "data": None,
        "msg": "任务查询成功"
    }
    sql = '''SELECT task_id,user_id from task WHERE state =2'''  # ,task.created_at 返回任务创建时间
    queryData = queryBySQL(sql)
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    rows = queryData.fetchall()
    result["data"] = rows
    if result["data"] == []:
        result["data"] = "没有正在执行的任务"
    return jsonify(result)

# get task list where id={id}
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


# update task state or status(confirmed)
@api.route('/<task_id>', methods=['POST'])
def update_task(task_id):
    result = {
        "code": 1,
        "data": None,
        "msg": "update_task_ok"
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
        if 'extent' in params:  # user-inputed unnecessary extent
            task.extent = params['extent']
        if 'user_id' in params:
            task.user_id = params['user_id']
        if 'state' in params:
            task.state = params['state']
        if 'status' in params:
            task.status = params['status']
        DB.session.add(task)
        return jsonify(result)

# 删除任务id=1的信息
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
    if row:
        return row
    else:
        return None


def do_job(task_id, state):
    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        if task:
            if state == 2:
                IPADDR = CONFIG.IPADDR
                task.handler = IPADDR
            elif state == 3:
                task.end_at = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            task.state = state
            DB.session.add(task)


def doing_job():
    IPADDR = CONFIG.IPADDR
    sql = '''SELECT * FROM "task" where state='2' and handler='''+"'" + IPADDR + "'"
    queryData = queryBySQL(sql)
    row = queryData.fetchone()
    if row:
        return True
    else:
        return False
