#!/usr/bin/env python3
# encoding: utf-8
from __future__ import annotations

import os
import sys
# setup access to the local .site-packages
sys.path.insert(0, os.path.dirname(__file__) + "/.site-packages")  # noqa
import requests
from workflow import Workflow3

COOKIE = os.getenv('cookie')

def query_people_detail_info(employee_name):
    url = "https://mmm-boe-va.bytedance.net/apps/bsm_web/back_end/employee/search/"
    req = {
        "pageNo": 1,
        "type": 0,
        "pageSize": 30,
        "employeeName": employee_name,
        "version": 1669299606797
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": COOKIE
    }
    return requests.post(url=url, json=req, headers=headers, timeout=10000)


def main(wf: Workflow3):
    try:
        if len(wf.args):
            query = wf.args[0]
        else:
            return
        cached_name = f"people_query_{query}"
        resp = wf.cached_data(cached_name, query_people_detail_info, {'employee_name': query}, max_age=6000)
        employee_list = resp.json()['data']['employeeList']
        if len(employee_list) == 0:
            wf.add_item(title="无搜索结果",
                        subtitle="no result")
            wf.send_feedback()
            return
        for employee in employee_list:
            # 部门信息规范
            department_info = "no related department"
            if "departmentName" in employee.keys() and len(employee['departmentName']) != 0 :
                department_info = employee['departmentName']
            # 姓名规范
            name = "佚名"
            if "name" in employee.keys():
                name = employee['name']
            elif "enName" in employee.keys():
                name = employee['enName']

            wf.add_item(title=f"{name}  {employee['id']}",
                        subtitle=department_info,
                        arg=employee['id'],
                        valid=True)
            wf.rerun
        wf.send_feedback()

    except Exception as e:
        wf.logger.exception(e)
        raise


if __name__ == "__main__":
    wf = Workflow3()
    wf.logger.info(__name__)
    sys.exit(wf.run(main))
    # rep = query_people_detail_info("金聪聪")
    # print(rep.json())
