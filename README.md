# 执行命令
```bash
docker run --name demo -v /data/ex_data_file:/app/res -d image_name:0.0.1  
```
docker -v: 将待处理的数据文件(xml/txt)挂载至容器下/app/res目录