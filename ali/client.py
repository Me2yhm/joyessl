from abc import ABC, abstractmethod
from alibabacloud_cas20200407.client import Client as cas20200407Client
from alibabacloud_cloudapi20160714.client import Client as CloudAPI20160714Client
from alibabacloud_tea_openapi import models as open_api_models


class clientType(ABC):
    endpoint: int  # 指定访问的域名

    @abstractmethod
    def __new__(cls, config: open_api_models.Config):
        """
        创建api账户并且初始化
        """


class api_gateway_client(clientType):
    endpoint = f"apigateway.cn-hongkong.aliyuncs.com"

    def __new__(cls, config: open_api_models.Config) -> CloudAPI20160714Client:
        return CloudAPI20160714Client(config)


class api_sslplate_client(clientType):
    endpoint = f"cas.aliyuncs.com"

    def __new__(cls, config: open_api_models.Config) -> cas20200407Client:
        return cas20200407Client(config)
