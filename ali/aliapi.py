# -*- coding: utf-8 -*-
import os
import sys
from typing import List

from client import clientType, api_gateway_client, api_sslplate_client


from alibabacloud_cas20200407 import models as cas_20200407_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cloudapi20160714 import models as cloud_api20160714_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

accesskey_ID = os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"]
accesskey_secret = os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"]


class aliapi:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
        client_type: clientType,
    ) -> clientType:
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
        config.endpoint = client_type.endpoint
        return client_type(config)

    @staticmethod
    def get_apigroups_info():
        # 代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。故使用环境变量获取 AccessKey 的方式进行调用
        client = aliapi.create_client(
            accesskey_ID,
            accesskey_secret,
            api_gateway_client,
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
            accesskey_ID,
            accesskey_secret,
            api_gateway_client,
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
            accesskey_ID,
            accesskey_secret,
            api_gateway_client,
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

    @staticmethod
    def upload_ssl(
        certName: str,  # 文件名
        certPath: str,  # .fullchain文件存储路径
        keyPath: str,  # .key文件存储路径
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。
        client = aliapi.create_client(
            accesskey_ID,
            accesskey_secret,
            api_sslplate_client,
        )
        with open(certPath, "r") as f:
            cert_body = f.read()
        with open(keyPath, "r") as f:
            cert_key = f.read()
        upload_user_certificate_request = (
            cas_20200407_models.UploadUserCertificateRequest(
                name=certName,
                cert=cert_body,
                key=cert_key,
            )
        )
        runtime = util_models.RuntimeOptions()
        try:
            cert = client.upload_user_certificate_with_options(
                upload_user_certificate_request, runtime
            )
            cert = cert.to_map()
        except Exception as error:
            print(UtilClient.assert_as_string(error.message))

    @staticmethod
    def get_sslmessage_list() -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = aliapi.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
            api_sslplate_client,
        )
        list_user_certificate_order_request = (
            cas_20200407_models.ListUserCertificateOrderRequest(order_type="upload")
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            ssl_message = client.list_user_certificate_order_with_options(
                list_user_certificate_order_request, runtime
            ).to_map()
            ssl_list = ssl_message["body"]["CertificateOrderList"]
            return ssl_list

        except Exception as error:
            # 如有需要，请打印 error
            print(UtilClient.assert_as_string(error.message))

    @staticmethod
    def has_ssl(certName: str) -> bool:
        ssl_list = aliapi.get_sslmessage_list()
        flag = False
        for ssl in ssl_list:
            if ssl["Name"] == certName:
                return True
        return flag

    @staticmethod
    def get_sslId(certName: str) -> int:
        ssl_list = aliapi.get_sslmessage_list()
        if aliapi.has_ssl(certName):
            for ssl in ssl_list:
                if ssl["Name"] == certName:
                    return ssl["CertificateId"]
        else:
            raise ValueError("ssl not exist")

    @staticmethod
    def del_ssl(certId: int) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = aliapi.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
            api_sslplate_client,
        )
        delete_user_certificate_request = (
            cas_20200407_models.DeleteUserCertificateRequest(certId)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.delete_user_certificate_with_options(
                delete_user_certificate_request, runtime
            )
        except Exception as error:
            # 如有需要，请打印 error
            print(UtilClient.assert_as_string(error.message))


if __name__ == "__main__":
    aliapi.get_apigroups_info()
