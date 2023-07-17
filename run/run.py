# -*- coding: utf-8 -*-
import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from joyessl.ali.aliapi import aliapi
from docker_to_data import ssl_from_docker


# 文件路径的问题需要仔细考虑，同时考虑ssl证书更新时的备份问题。
def get_ssl_path(certname: str):
    base = "/"
    cert_path = os.path.join(base, f"etc/nginx/certificates/{certname}/fullchain.cer")
    keypath = os.path.join(base, f"etc/nginx/certificates/{certname}/cert.key")
    if os.path.exists(cert_path) and os.path.exists(keypath):
        return cert_path, keypath
    else:
        raise FileNotFoundError("cert files not exist")


# certname 和groupname,domain如何提前知道？-crantab 运行时传参， 传参顺序为：groupname，domainname， sslname


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


def update_ssl(certname: str) -> None:
    if aliapi.has_ssl(certName=certname):
        cert_id = aliapi.get_sslId(certName=certname)
        aliapi.del_ssl(certId=cert_id)
        ssl_upload_apigateway(certname=certname)
    else:
        ssl_upload_apigateway(certname=certname)


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
    subprocess.run(["sh", "restart_docker.sh"])
    ssl_from_docker(*sys.argv[1:])
    update_fc_ssl(*sys.argv[1:])
