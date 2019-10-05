# 家国梦自动拾取金币、自动完成运货
# 核心工作模块
# Author: LuRenJiasWorld (https://github.com/LuRenJiasWorld) <loli@lurenjia.in>
# Dependency: adb(Shell)

from utils import *
import time
import tkinter
import tkinter.messagebox
from tkinter import ttk
from PIL import Image, ImageTk


class Work:
	# 截图文件位置
	__snapshot_file = ""

	# 当前打点模式
	__current_mode = "home"

	# 是否完成配置
	__config_status = False

	# 建筑物坐标点
	__home_spot = [[-1,-1], [-1,-1], [-1,-1],
				   [-1,-1], [-1,-1], [-1,-1],
				   [-1,-1], [-1,-1], [-1,-1]]
	# 列车坐标点
	__train_spot = [[-1,-1], [-1,-1], [-1,-1]]

	# 在图片上增加指示器
	__indicator_group = [None, None, None, None, None, None, None, None, None]

	# 清空临时目录
	def __empty_dir(self):
		# 清空临时目录
		try:
			remove_dir("./tmp")
			os.mkdir("./tmp", mode=0o755)
		except Exception:
			raise PermissionError("清空临时目录过程中出现错误")

	# 截图
	def __snapshot(self):
		out, err, exception = exec_command("adb shell screencap -p /sdcard/test.png")
		if exception is None:
			print("终端截图成功，存储于终端/sdcard/test.png")
			file_name = "snapshot{}.png".format(str(int(time.time())))
			out, err, exception = exec_command("adb pull /sdcard/test.png tmp/{}".format(file_name))
			if exception is None:
				print("截图拷贝成功，存储于本机当前目录tmp/{}".format(file_name))
				return file_name
			else:
				raise OSError("拷贝截图命令执行失败")
		else:
			raise OSError("终端截图命令执行失败")

	# 显示窗体
	def __show_frame(self):
		frame = tkinter.Tk()

		frame.title("选择关键点")
		frame.geometry("480x800+400+100")
		frame.resizable(width=False, height=False)
		frame.configure(bg="#ececec")

		# 提示文本
		label = tkinter.Label(
			frame,
			text="请点击图中的所有建筑物",
			fg="black",
			bg="#ececec",
			font=("黑体", 14),
			width=400,
			height=1,
			justify="center",
			anchor="center",
		)
		label.pack()

		# 图片框
		img = Image.open("tmp/{}".format(self.__snapshot_file))
		frame.update()
		img_resized = resize_image(frame.winfo_width(), frame.winfo_height() - label.winfo_height() - 40, img)
		orig_image = ImageTk.PhotoImage(img)
		image = ImageTk.PhotoImage(img_resized)

		image_label = tkinter.Label(
			frame,
			width=frame.winfo_width(),
			image=image,
			bg="#ececec",
			cursor="dot"
		)
		image_label.pack(expand=True)

		# 图片点击事件
		def image_click(event):
			def add_image_label(x, y, orig_image_x, orig_image_y):
				if self.__indicator_group[-1] is None:
					index = self.__indicator_group.index(None)

					trigger_submit_status(index)

					self.__indicator_group[index] = ttk.Button(
						image_label,
						text=index + 1,
						width=1
					)

					self.__indicator_group[index].update()

					self.__indicator_group[index].place(
						relx=(x / image_label.winfo_width()),
						rely=(y / image_label.winfo_height())
					)
					if self.__current_mode == "home":
						self.__home_spot[index] = [orig_image_x, orig_image_y]
					elif self.__current_mode == "train":
						self.__train_spot[index] = [orig_image_x, orig_image_y]

				else:
					tkinter.messagebox.showwarning("无法继续打点", "你已经打满了{}个点，如果有打错的点，请直接点击重置。".format(str(len(self.__indicator_group))))

			# 事件点击坐标
			click_x = event.x
			click_y = event.y
			# 缩放后的图片长宽
			image_width = image.width()
			image_height = image.height()
			# Label容器的长宽
			real_width = image_label.winfo_width()
			real_height = image_label.winfo_height()
			# 图片本来的长宽
			orig_image_width = orig_image.width()
			orig_image_height = orig_image.height()
			image_x = click_x - ((real_width - image_width) / 2)
			image_y = click_y - ((real_height - image_height) / 2)
			orig_image_x = round(image_x * (orig_image_width / image_width), 2)
			orig_image_y = round(image_y * (orig_image_height / image_height), 2)
			add_image_label(click_x, click_y, orig_image_x, orig_image_y)

		def reset_image_label():
			for each in self.__indicator_group:
				if each is not None:
					each.place_forget()

			self.__home_spot = [[-1, -1]] * len(self.__home_spot)
			self.__indicator_group = [None] * len(self.__indicator_group)

		def recap_image():
			global img, img_resized, orig_image, image
			self.__snapshot_file = self.__snapshot()

			img = Image.open("tmp/{}".format(self.__snapshot_file))
			img_resized = resize_image(frame.winfo_width(), frame.winfo_height() - label.winfo_height() - 40, img)
			orig_image = ImageTk.PhotoImage(img)
			image = ImageTk.PhotoImage(img_resized)

			image_label["image"] = image

		image_label.bind("<Button-1>", image_click)

		# 按钮容器
		button_container = tkinter.Frame(
			width=frame.winfo_width(),
			height=40,
			bg="#ececec"
		)
		button_container.pack()

		padding_1 = tkinter.Frame(
			button_container,
			width=frame.winfo_width(),
			height=5,
			bg="#ececec"
		)
		padding_1.grid(row=0, columnspan=3)

		# 重置按钮
		button_reset = ttk.Button(
			button_container,
			text="重置",
			width=12,
			command=reset_image_label
		)
		button_reset.grid(row=1, column=0)

		# 重截图按钮
		button_recap = ttk.Button(
			button_container,
			text="重截图",
			width=12,
			command=recap_image
		)
		button_recap.grid(row=1, column=1)

		# 提交按钮
		button_submit = ttk.Button(
			button_container,
			text="下一步",
			width=12,
			state="disabled"
		)

		def trigger_submit_status(index):
			if index == 1:
				button_submit["state"] = "disabled"
			else:
				button_submit["state"] = "normal"

		def finish():
			self.__config_status = True
			frame.destroy()

		def next_step():
			label["text"] = "请点击图中的三个列车车厢"
			for each in self.__indicator_group:
				if each is not None:
					each.place_forget()
			self.__indicator_group = [None, None, None]
			self.__current_mode = "train"
			button_submit["text"] = "完成"
			button_submit["command"] = finish

		button_submit["command"] = next_step
		button_submit.grid(row=1, column=2)

		padding_2 = tkinter.Frame(
			button_container,
			width=frame.winfo_width(),
			height=5,
			bg="#ececec"
		)
		padding_2.grid(row=2, columnspan=3)

		frame.mainloop()

	# 触发建筑物点击事件，收取金币
	def __click_home(self):
		for each in self.__home_spot:
			if each is not [-1, -1]:
				command = "adb shell input tap {} {}".format(str(int(each[0])), str(int(each[1])))
				print(command)
				exec_command(command)
				time.sleep(0.1)

	# 拖放列车上的快递
	# TODO: 拖放成功率优化，目前遍历的方式太暴力了
	def __drag_item(self):
		for each_home in self.__home_spot:
			for each_train in self.__train_spot:
				if each_home is not [-1, -1] and each_train is not [-1, -1]:
					command = "adb shell input swipe {} {} {} {} 550".format(
						str(int(each_train[0])),
						str(int(each_train[1])),
						str(int(each_home[0])),
						str(int(each_home[1]))
					)
					print(command)
					exec_command(command)

	# 工作流
	def work(self):
		i = 0
		try:
			self.__empty_dir()
			self.__snapshot_file = self.__snapshot()
			self.__show_frame()

			if self.__config_status == True:
				while True:
					print("第{}轮开始：".format(i))
					i += 1
					self.__click_home()
					self.__drag_item()

		except PermissionError as e:
			print("出现权限错误，错误原因为『{}』，请检查是否授予本软件当前目录读写权限！".format(e))
			return False
