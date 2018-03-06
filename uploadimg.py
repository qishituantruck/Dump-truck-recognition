from ftplib import FTP
import os
import os.path
#上传文件到FTP服务器
def ftp_upload(filename, save_filename):
    ftp = FTP()
    ftp.set_debuglevel(0)                   # 打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.connect('192.168.1.111', 2121, 60)  # FTP主机 端口 超时时间
    ftp.login('ftpadmin', 'Che19940624')           # 登录，如果匿名登录则用空串代替即可

    remote_dir = save_filename.split("/")
    newfilename = remote_dir.pop()

    if remote_dir :
        for dir_name in remote_dir :
            if dir_name == '.' or dir_name == '' :
                continue
            else :
                #尝试创建目录
                try:
                    ftp.mkd(dir_name)
                    ftp.cwd(dir_name)
                except:
                    ftp.cwd(dir_name)
    target_path = '/'.join(remote_dir)
    print('保存文件名:', newfilename)
    print ('上传目录:', target_path)
    print ('当前目录:', ftp.pwd())
    print ('待上传文件名: %s' % os.path.basename(filename))
    bufsize = 1024                       # 设置缓冲块大小
    file_handler = open(filename, 'rb')  # 以读模式在本地打开文件
    ftp.storbinary('STOR %s' % newfilename, file_handler, bufsize)
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print ("本地文件 ", filename, " 成功上传至 ", save_filename)

#举个栗子
ftp_upload('C:/Users/chezh/PycharmProjects/opencv_project/dog.jpg', '123.jpg')  #上传文件到根目录下
# ftp_upload('D:/python/test/ex1/7.jpg', 'test/123/456/123.jpg');
