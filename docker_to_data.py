#使用命令行，将docker中固定位置的文件拉取到本地服务器
#要在root账户里运行
import subprocess

subprocess.getoutput("docker cp 7f860eb94b4b:/etc/nginx/certificates/cert-ny5jx0l5nq7r7m6p/cert.key /etc/nginx/test/")
subprocess.getoutput("docker cp 7f860eb94b4b:/etc/nginx/certificates/cert-ny5jx0l5nq7r7m6p/fullchain.cer /etc/nginx/test/")
