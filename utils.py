# 家国梦自动拾取金币、自动完成运货
# 辅助工具
# Author: LuRenJiasWorld (https://github.com/LuRenJiasWorld) <loli@lurenjia.in>
# Dependency: adb(Shell)

import subprocess
import os
import re
from PIL import Image


# 使用subprocess执行命令
# 返回：
# - stdout
# - stderr
# - Exception
def exec_command(command):
	try:
		popen = subprocess.Popen(
			command,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			bufsize=1
		)
		out, err = popen.communicate()
		out_str = bytes.decode(out)
		err_str = bytes.decode(err)
		return out_str, err_str, None

	except FileNotFoundError as e:
		return "", "", e


# 检查是否安装adb
def check_adb():
	out, err, exception = exec_command("adb")
	return not bool(exception)


# 检查是否有设备已连接
def check_connection():
	out, err, exception = exec_command("adb devices")

	try:
		if exception is None:
			match = re.findall(r"([\S]+)\t(device)", out)
			if len(match) == 0:
				raise TypeError("没有设备连接")
			else:
				return match[0][0]
		else:
			raise OSError("执行命令失败")

	except TypeError or OSError:
		return False


# 删除临时目录
def remove_dir(dir_path):
	if not os.path.isdir(dir_path):
		return
	files = os.listdir(dir_path)
	try:
		for file in files:
			file_path = os.path.join(dir_path, file)
			if os.path.isfile(file_path):
				os.remove(file_path)
			elif os.path.isdir(file_path):
				remove_dir(file_path)
		os.rmdir(dir_path)
	except Exception as e:
		return False


# 修改图像大小
def resize_image(w_box, h_box, pil_image):
	w, h = pil_image.size
	f1 = 1.0 * w_box / w
	f2 = 1.0 * h_box / h
	factor = min([f1, f2])
	width = int(w * factor)
	height = int(h * factor)
	return pil_image.resize((width, height), Image.ANTIALIAS)
