# 使用命令行，将docker中固定位置的文件拉取到本地服务器
# 要在root账户里运行

import sys
import subprocess


def ssl_from_docker(certName: str):
    subprocess.getoutput(
        f"docker cp 7f860eb94b4b:/etc/nginx/certificates/{certName}/cert.key /etc/nginx/certificates/{certName}/"
    )
    subprocess.getoutput(
        f"docker cp 7f860eb94b4b:/etc/nginx/certificates/{certName}/fullchain.cer /etc/nginx/certificates/{certName}/"
    )
