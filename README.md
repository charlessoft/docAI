## 项目说明
基于openai和开源的后台管理系统开发的基本demo.

openai服务:使用flask提供一个openai的api接口和语料的保存(目前语料是保存在本地)

后台管理系统:使用golang提供一些语料验证的demo界面.

## 依赖环境
1. golang >=1.18.4
2. python 3.10
3. vue3 
4. node 16.17
5. mysql 5.7 (golang后台的基础配置)


## 编译步骤


### 编译管理服务端
```
cd gpt-admin
nvm install v16.17
nvm use v16.17
make build-web-local
make build-server-local
make build-local
编译后可执行文件生成在build目录下
```

### 编译python环境

```
cd gptengine-app
pip3 install -r requirements.txt
```



## 部署步骤

1. 运行服务端

```
cd gpt-admin/build
cp ../server/config.yaml .
./server
```

2. 运行api服务

```
替换azure openai的key

编辑 docAI/gptengine-app/gptengine/api/v1/resources/index.py 文件
openai.api_key = os.getenv("OPENAI_API_KEY", 'azure openai key')

cd gptengine-app
python3 gptengine/main.py 
```


## 测试
账号: test1
密码: 123456