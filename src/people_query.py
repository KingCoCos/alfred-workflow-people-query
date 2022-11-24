#!/usr/bin/env python3
# encoding: utf-8
from __future__ import annotations

import os
import sys
# setup access to the local .site-packages
sys.path.insert(0, os.path.dirname(__file__) + "/.site-packages")  # noqa
import requests
from workflow import Workflow3


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
        "Cookie": "region=CHN; admin-csrf-token=UN86OqWEcJ6xd+LSddu3gBSlY+M77QC0vO+nmNvQYUp75LXFQyIU/NOr1RDqXa4NBE0rnqACwMinP7sLsgrc3Iy2ASXOq5zomZYn2xoTdYKBNHVNaXLzmfT62b3K74u4T9bmUg==; MONITOR_WEB_ID=bce2d130-f929-435e-8f5e-46eec7301b20; _tea_utm_cache_1508={%22utm_source%22:%22startup%22%2C%22utm_medium%22:%22chrome%22}; X-Risk-Browser-Id=4ef04ada21ae5fb2fd2f944a1a9184bf958bec282cff506f05e25dbd6e2b7174; _ga=GA1.2.1422160463.1662714804; SLARDAR_WEB_ID=5317297; toutiao_sso_user=a8c6f85615d260ade817e6bab19da549; sso_uid_tt=ff2141ea17bf56a462df9522f1f9e5b95c5c517410b572b17fb16a239507aef7; sso_uid_tt_ss=012ac5e25e91e927a147fed40070f97bbc556f1f83a5f65fa91032b4e9a650a1; toutiao_sso_user_ss=1151e9ed704b3c40f19c631553e5dac2; ssid_ucp_sso_v1=1.0.0-KDFmMTlkYTg4NDAyNDFlMDBkNTViYTZkMTY3YTJkNzVkZTgxMjU5ZDIKGAiGiPu-mNLZl2EQlu3VmQYYrww4AUDrBxB-Ggdib2VpMThuIiAxMTUxZTllZDcwNGIzYzQwZjE5YzYzMTU1M2U1ZGFjMg; sessionid_ss=1151e9ed704b3c40f19c631553e5dac2; sid_tt=a8c6f85615d260ade817e6bab19da549; MONITOR_WEB_ID=e2d047d4-5a4c-4294-923a-f715fbdfd251; i18next=zh; lang=zh; _gid=GA1.2.1593292430.1669183298; mmm_scenes=china; _tea_utm_cache_3412=undefined; login_token=0c0680c7-d548-463e-bae1-cf1cb831061f",
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

        for employee in employee_list:
            wf.add_item(title=f"{employee['name']}  {employee['id']}",
                        subtitle=employee['departmentName'],
                        arg=employee['id'])
            wf.send_feedback()
    except Exception as e:
        wf.logger.exception(e)
        raise


if __name__ == "__main__":
    wf = Workflow3()
    wf.logger.info(__name__)
    wf.run(main)
    # rep = query_people_detail_info("金聪聪")
    # print(rep.json())
