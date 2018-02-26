# Dump-truck-recognition
1.在以下网站下载Python程序：
https://www.python.org/downloads/windows/
这里选择3.6.3版本


2
下载后按照默认安装。
然后安装Numpy模块。 按Win+R输入CMD，进入安装目录下的Lib\site-packages子目录，在联网状态下输入pip install numpy并回车，Python自动下载numpy模块并安装


3
下载Opencv 3.4模块（看清楚win和win-amd后缀 不一样的我下的是win后缀的，我笔记本不是amd的）
https://pypi.python.org/pypi/opencv-python/3.4.0.12#downloads


4
拷贝下载的Opencv 3.4模块到Python的安装目录Lib\site-packages下，运行  pip install opencv_python-3.4.0.12-cp36-cp36m-win32.whl
然后程序自动安装Opencv模块。

5
测试。打开记事本，拷贝以下内容，并保存为test.py.(可拷贝任意图片到文件存放目录下，并更改图片名与程序一致）
import cv2
import numpy as np
image = cv2.imread("20122-large.jpg")
cv2.imshow("Image",image)
cv2.waitKey(0)


6
在命令行下输入test.py,就会弹出窗口显示指定的图片。说明配置成功。


7
如果出现ImportError: DLLL load failed.
请安装对应的Visual C++ Redistributable for Visual Studio 2015，下载地址：https://www.microsoft.com/zh-cn/download/details.aspx?id=48145





