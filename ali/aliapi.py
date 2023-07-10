# -*- coding: utf-8 -*-
import os
import sys

from typing import List

from alibabacloud_cloudapi20160714.client import Client as CloudAPI20160714Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cloudapi20160714 import models as cloud_api20160714_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"] = 'ID'
os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"] = 'secret'

class aliapi:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> CloudAPI20160714Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret,
        )
        # 访问的域名
        config.endpoint = f"apigateway.cn-hongkong.aliyuncs.com"
        return CloudAPI20160714Client(config)

    @staticmethod
    def get_apigroups_info() -> None:
        # 代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。故使用环境变量获取 AccessKey 的方式进行调用
        client = aliapi.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        )
        describe_api_groups_request = (
            cloud_api20160714_models.DescribeApiGroupsRequest()
        )
        runtime = util_models.RuntimeOptions()

        try:
            # 复制代码运行请自行打印 API 的返回值
            groups_describe = client.describe_api_groups_with_options(
                describe_api_groups_request, runtime
            )
            groups = groups_describe.to_map()
            groups_attribute = groups["body"]["ApiGroupAttributes"]["ApiGroupAttribute"]
            # print(len(groups_attribute))
            # for v in groups_attribute:
            #     print(v)
            return groups_attribute
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # 绑定域名和ssl证书需要知道分组id
    @staticmethod
    def get_apigroupid(
        groupname: str,
    ) -> str:
        groups = aliapi.get_apigroups_info()
        try:
            for v in groups:
                if v["GroupName"] == groupname:
                    return v["GroupId"]

        except Exception as error:
            UtilClient.assert_as_string(error.message)

    # 给指定分组绑定自定义域名
    @staticmethod
    def connect_domin(
        group_id: str,
        domain_name: str,  # 域名
        DomainType: str = "INTERNET",  # 指定是公网类型还是内网类型，可选值：INTERNET：公网类型; INTRANET:内网类型。当指定了内网类型后，该域名就不允许从内网请求过来
    ) -> None:
        client = aliapi.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        )
        set_domain_request = cloud_api20160714_models.SetDomainRequest(
            group_id=group_id,
            domain_name=domain_name,
            SetDomainRequest=DomainType,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.set_domain_with_options(set_domain_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # 绑定指定证书
    @staticmethod
    def set_domain_ssl(
        groupid: str,
        domainName: str,
        sslName: str,  # 证书名字
        certPath: str,  # .fullchain文件存储路径
        keyPath: str,  # .key文件存储路径
    ) -> None:
        client = aliapi.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        )
        with open(certPath, "r") as f:
            cert = f.read()
        with open(keyPath, "r") as f:
            key = f.read()
        set_domain_certificate_request = (
            cloud_api20160714_models.SetDomainCertificateRequest(
                group_id=groupid,
                domain_name=domainName,
                certificate_name=sslName,
                certificate_body=cert,
                certificate_private_key=key,
            )
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.set_domain_certificate_with_options(
                set_domain_certificate_request, runtime
            )
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


if __name__ == "__main__":
    aliapi.get_apigroups_info()
