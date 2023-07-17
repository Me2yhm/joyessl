# -*- coding: utf-8 -*-
import os
import sys
import subprocess

# 为了让run.py文件可以导入aliapi.py模块，将父级目录的父级目录添加至环境变量
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from joyessl.ali.aliapi import aliapi
from docker_to_data import ssl_from_docker


# 从本地nginx中获得证书，路径为"/etc/nginx/certificates/certname/"
def get_ssl_path(certname: str):
    base = "/"
    cert_path = os.path.join(base, f"etc/nginx/certificates/{certname}/fullchain.cer")
    keypath = os.path.join(base, f"etc/nginx/certificates/{certname}/cert.key")
    if os.path.exists(cert_path) and os.path.exists(keypath):
        return cert_path, keypath
    else:
        raise FileNotFoundError("cert files not exist")


# certname 和groupname,domain如何提前知道？-脚本运行时外部传参， 传参顺序为: groupname，domainname， sslname


# 将域名绑定到指定api分组
def ssl_upto_apigroup(groupname: str, domainname: str, sslname: str) -> None:
    groupid = aliapi.get_apigroupid(groupname=groupname)
    cert_path, keypath = get_ssl_path(sslname)
    aliapi.set_domain_ssl(
        groupid=groupid,
        domainName=domainname,
        sslName=sslname,
        certPath=cert_path,
        keyPath=keypath,
    )


# 如果函数计算已经有域名和证书，更新证书
def ssl_upto_fc(domainname: str, sslname: str) -> None:
    cert_path, keypath = get_ssl_path(sslname)
    aliapi.update_function_ssl(
        domainName=domainname,
        sslName=sslname,
        certPath=cert_path,
        keyPath=keypath,
    )


def ssl_upload_apigateway(certname: str) -> None:
    certpath, keypath = get_ssl_path(certname)
    aliapi.upload_ssl(certname, certpath, keypath)


# 更新证书到ali数字证书服务上
def update_ssl(certname: str) -> None:
    # 如果已经有同名证书，删除旧的，替换新的
    if aliapi.has_ssl(certName=certname):
        cert_id = aliapi.get_sslId(certName=certname)
        aliapi.del_ssl(certId=cert_id)
        ssl_upload_apigateway(certname=certname)
    # 如果没有，直接上传
    else:
        ssl_upload_apigateway(certname=certname)


# 如果函数计算没有创建域名，创建一个，并使用https
def ssl_upload_fc(domainName: str, sslName: str):
    cert_path, keypath = get_ssl_path(sslName)
    aliapi.creat_fc_domain(
        domainName=domainName,
        sslName=sslName,
        certPath=cert_path,
        keyPath=keypath,
    )


def update_fc_ssl(domainName: str, sslName: str):
    if aliapi.fc_has_domain(domainName=domainName):
        ssl_upto_fc(domainname=domainName, sslname=sslName)
    else:
        ssl_upload_fc(domainName=domainName, sslName=sslName)


if __name__ == "__main__":
    restart_docker = os.path.join(os.path.dirname(__file__), "restart_docker.sh")
    subprocess.run(["sh", restart_docker])  # 重启docker，ohttps会将最新的证书部署到docker
    ssl_from_docker(sys.argv[2])  # 将证书文件从docker同步更新到本地nginx
    update_fc_ssl(*sys.argv[1:])  # 将证书更新到函数计算上，从外部接受两个参数，domain和certname
    update_ssl(sys.argv[2])  # 将证书更新到阿里云数字证书服务上
