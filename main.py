# 家国梦自动拾取金币、自动完成运货
# Author: LuRenJiasWorld (https://github.com/LuRenJiasWorld) <loli@lurenjia.in>
# Dependency: adb(Shell)

import time
from utils import *
from work import Work


if __name__ == "__main__":
	if check_adb():
		while True:
			if not check_connection():
				sleep_time = 5
				print("未连接设备")
				for each in range(sleep_time):
					print("\t将于{}秒后重试......".format(str(sleep_time - each)))
					time.sleep(1)
			else:
				break
		print("连接成功，设备ID为{}".format(check_connection().split("\t")[0]))
		Work().work()
	else:
		print("没有找到adb命令，请安装adb命令行工具后重试")
		exit(0)
