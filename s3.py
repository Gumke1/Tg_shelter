import asyncio
from contextlib import asynccontextmanager
import uuid
import os

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
access_key = "YCAJE3Hz1hrCLhDcoMnKNhgx5"
secret_key = "YCO4Wy5ZqPCmlrVbWMF1WcWeGhLYxKSuGEeJebp3"
endpoint_url = "https://storage.yandexcloud.net/"
bucket_name = "alekseyhouse"
region_name = "ru-central1"


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.endpoint_url = endpoint_url

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file_obj(
            self,
            file_path: str,
            object_name: str = None
    ) -> str:
        if object_name is None:
            object_name = f"images/{uuid.uuid4()}.jpg"
        try:
            async with self.get_client() as client:
                with open(file_path, 'rb') as f:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=f,
                        ContentType='image/jpeg' # Укажем Content-Type
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")
                return f"{self.endpoint_url}{self.bucket_name}/{object_name}"
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return None

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")



async def s3_photo(file_path: str) -> str:
    """
    Загружает изображение в S3 и возвращает URL.

    Args:
        file_path: Путь к файлу изображения.

    Returns:
        URL изображения в S3, или None в случае ошибки.
    """
    s3_client = S3Client(
        access_key=access_key,
        secret_key=secret_key,
        endpoint_url=endpoint_url,
        bucket_name=bucket_name,
    )
    try:
        file_url = await s3_client.upload_file_obj(file_path)  #Используем upload_file_obj
        return file_url
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


async def main():
    # # Проверка, что мы можем загрузить, скачать и удалить файл
    # await s3_client.upload_file("photos/5be1fd07-0498-4858-afd4-89c236a82f37.jpg")
    test_file = "photos/5be1fd07-0498-4858-afd4-89c236a82f37.jpg"
    photo_url = await s3_photo(test_file)
    print(f"Uploaded to: {photo_url}")
    return photo_url

