# 本地
docker build -t multi_mock .
docker save mock_mutil:2.0 -o multi_mock.tar
# 上传到服务器
docker load < multi_mock.jar
docker run --name multi_mock  --network mybridge -d -p 8091:8000 mock_mutil:2.0