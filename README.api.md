# 字幕优化 API 服务
优化(重新断句、优化字幕、翻译字幕)srt字幕文件，提供api服务

## 安装依赖
```sh
pip3 install -r requirements_api.txt
```
## 使用
### 启动api服务
```sh
python3 ./api.py
```
### cli
```sh
python3 ./api.py ./testdata/1.srt
```

## Docker
### 构建镜像
```sh
docker build -t srt-api -f api.Dockerfile .
```
### 运行容器
```sh
docker run -d -v $(pwd)/.env:/app/.env -p 5000:5000 srt-api
```

## 接口示例
```sh
sh ./example.sh ./testdata/1.srt
```