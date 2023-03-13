#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Randy'
import re
from datetime import datetime
test_date = '他的生日是2016-12-12 14:34,是个可爱的小宝贝.二宝的生日是2016-12-21 11:34,好可爱的.'
test_datetime = '他的生日是2016-12-12 14:34,是个可爱的小宝贝.二宝的生日是2016-12-21 11:34,好可爱的.'
test_datetime = '2012-09-09T12:56:37Z'
test_datetime = '2015-11-09T00:42:57.527404Z'
test_datetime = '2016-11-06T15:32:17.000000'
test_datetime = 'aaaaaaaaaaaaaadddd dasd'
# date
mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",test_date)
print(mat.groups())
# ('2016-12-12',)
print(mat.group(0))
# 2016-12-12
date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",test_date)
for item in date_all:
  print(item)
# 2016-12-12
# 2016-12-21
# datetime
mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2})",test_datetime)
if mat:
  print(mat.groups())
  # ('2016-12-12 14:34',)
  print(mat.group(0))
  # 2016-12-12 14:34
else:
  print('TTTTTTTTTT')
date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",test_datetime)
for item in date_all:
  print(item)
# 2016-12-12 14:34
# 2016-12-21 11:34
## 有效时间
# 如这样的日期2016-12-35也可以匹配到.测试如下.
test_err_date = '如这样的日期2016-12-35也可以匹配到.测试如下.'
print(re.search(r"(\d{4}-\d{1,2}-\d{1,2})",test_err_date).group(0))
# 2016-12-35
# 可以加个判断
def validate(date_text):
  try:
    if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
      raise ValueError
    return True
  except ValueError:
    # raise ValueError("错误是日期格式或日期,格式是年-月-日")
    return False
print(validate(re.search(r"(\d{4}-\d{1,2}-\d{1,2})",test_err_date).group(0)))
# false
# 其他格式匹配. 如2016-12-24与2016/12/24的日期格式.
date_reg_exp = re.compile('\d{4}[-/]\d{2}[-/]\d{2}')
test_str= """
   平安夜圣诞节2016-12-24的日子与去年2015/12/24的是有不同哦.
   """
# 根据正则查找所有日期并返回
matches_list=date_reg_exp.findall(test_str)
# 列出并打印匹配的日期
for match in matches_list:
 print(match)
# 2016-12-24
# 2015/12/24