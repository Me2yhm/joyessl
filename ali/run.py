# -*- coding: utf-8 -*-
import os
import sys
from aliapi import aliapi


# 文件路径的问题需要仔细考虑，同时考虑ssl证书更新时的备份问题。
def get_ssl_path(certname: str):
    base = os.getcwd()
    cert_path = os.path.join(
        base, f"etc\\nginx\\certificate\\{certname}\\fullchain.cer"
    )
    keypath = os.path.join(base, f"etc\\nginx\\certificate\\{certname}\\cert .key")
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


def ssl_upload_apigateway(certname: str) -> None:
    certpath, keypath = get_ssl_path(certname)
    aliapi.upload_ssl(certname, certpath, keypath)


if __name__ == "__main__":
    ssl_upload_apigateway(*sys.argv[1:])
