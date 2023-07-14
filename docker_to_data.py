#使用命令行，将docker中固定位置的文件拉取到本地服务器
#要在root账户里运行

import sys
import subprocess

id = sys.argv[1:]
subprocess.getoutput(f"docker cp 7f860eb94b4b:/etc/nginx/certificates/cert-{id}/cert.key /etc/nginx/certificates/cert-{id}/")
subprocess.getoutput(f"docker cp 7f860eb94b4b:/etc/nginx/certificates/cert-{id}/fullchain.cer /etc/nginx/certificates/cert-{id}/")
