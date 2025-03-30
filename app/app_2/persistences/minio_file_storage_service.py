from minio import Minio

class MinioFileStorageService:
    def __init__(self):
       self.minio_client = Minio("minio-server:9000", access_key="minio", secret_key="minio123", secure=False)

       self.bucket_name = "backend-carlemany-s3-bucket"

    def put_file(self, local_path, remote_path):
        self.minio_client.fput_object(
            self.bucket_name,
            object_name=remote_path,
            file_path=local_path
        )
        return "localhost:9000/" + self.bucket_name + "/" + remote_path

    def remove_file(self, remote_path):
        self.minio_client.remove_object(
            self.bucket_name,
            remote_path
        )
