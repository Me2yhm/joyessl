#使用命令行，将docker中固定位置的文件拉取到本地服务器
import subprocess

subprocess.run('登录')
subprocess.communicate(input = '密码')
subprocess.run('docker run -d -p 80:80 -v /etc/nginx/cert-ny5jx015nq7r7m6p:/etc/nginx/cert-ny5jx015nq7r7m6p nginx')