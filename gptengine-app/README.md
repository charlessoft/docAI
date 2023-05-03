# app

## 快速启动 
1. uwsgi 启动
    ```
    cd app;uwsgi --plugin python --ini ./uwsgi.ini
    ```
2. 直接启动

    ```
    cd app;python3 myapp/main.py
    ```
    
3. docker 启动

    ```
    docker build -t myimage .

	docker run -d --name mycontainer -p 8888:80 myimage
    日志文件需要挂着
    ```
    


## 开发步骤
1. 修改工程名字
例如把flask-app修改成textract-app
```
cp -r flask-app textract-app
cd textract-app
find . -name "*.py" |xargs sed -in-place -e 's/myapp/textract/g'
sed -in-place -e 's/flask-app/textract-app/g' ./scripts/build_docker.sh
sed -in-place -e 's/myapp/textract/g' ./Dockerfile
sed -in-place -e 's/myapp/textract/g' ./uwsgi.ini
sed -in-place -e 's/myapp/wxcrawl/g' ./Makefile
sed -in-place -e 's/flask-app/textract-app/g' ./Makefile
sed -in-place -e 's/flask-app/textract-app/g' ./scripts/config.sh
mv myapp textract
```


```
eg:----
export PROJ_NAME=onlinestudy-app
export APP_NAME=onlinestudy
cp -r flask-app ${PROJ_NAME}
find ./${PROJ_NAME} -name "*.py" |xargs sed -i "" "s/myapp/${APP_NAME}/g"
sed -in-place -e "s/flask-app/${PROJ_NAME}/g" ./${PROJ_NAME}/scripts/build_docker.sh
sed -in-place -e "s/myapp/${APP_NAME}/g" ./${PROJ_NAME}/Dockerfile
sed -in-place -e "s/myapp/${APP_NAME}/g" ./${PROJ_NAME}/uwsgi.ini
sed -in-place -e "s/flask-app/${PROJ_NAME}/g" ./${PROJ_NAME}/Makefile
sed -in-place -e "s/myapp/${APP_NAME}/g" ./${PROJ_NAME}/Makefile
sed -in-place -e "s/flask-app/${PROJ_NAME}/g" ./${PROJ_NAME}/scripts/config.sh
mv ${PROJ_NAME}/myapp ${PROJ_NAME}/${APP_NAME}
```

回退
```
cp -r wxcrawl-app flask-app 
cd flask-app 
find . -name "*.py" |xargs sed -in-place -e 's/wxcrawl/myapp/g'
sed -in-place -e 's/wxcrawl-app/flask-app/g' ./scripts/build_docker.sh
sed -in-place -e 's/wxcrawl/myapp/g' ./Dockerfile
sed -in-place -e 's/wxcrawl/myapp/g' ./uwsgi.ini
sed -in-place -e 's/wxcrawl/myapp/g' ./Makefile
sed -in-place -e 's/wxcrawl-app/flask-app/g' ./Makefile
sed -in-place -e 's/wxcrawl-app/flask-app/g' ./scripts/config.sh
mv wxcrawl myapp 
```
2. 修改Dockerfile
myapp 修改成新工程名字

3. 修改uwsgi.ini
myapp 修改成新工程名字

3. 日志修改logging_config.ini配置,改变日志保存方式

4. restful api接口 2两种写法, 在myapp/api/v1/resources目录中增加新接口

5. 修改端口

```
1. uwsgi中修改端口,如果使用uwsgi方式启动
2. setting.py FLASK_PORT,
```

6. 编译
```
docker build -t myimage .
```


方式1
```python
from flask import Blueprint, request, json, current_app, Response
app = Blueprint('index', __name__)

@app.route('/echo')
def health():
    return 'running ok!'
```

方式2

```python
from flask_restful import Resource, Api
from flask import current_app as app
from flask_restful import Resource,Api
from textminer.api.v1 import api
from textminer.core.crf.crfmgr import CRFMgr

api_wrap = Api(api)


@api_wrap.resource('/echo')
class MainPage(Resource):
    def get(self):
        app.logger.error('flask  log. begin.....')
        app.logger.debug('A value for debugging')
        app.logger.warning('A warning occurred (%d apples)', 1)
        app.logger.error('test echo errorr!!')
        app.logger.error('flask  log. end.....')
        crf=CRFMgr()
        crf.write()
        return "running ok"

```




## 功能列表 
1. echo 

## 健康检查

```
curl localhost:18883/api/v1/echo
```


2. 接口列表

```
curl localhost:18883/api/docs
```
## 数据库命令
flask db init
flask db migrate
flask db upgrade

### 创建用户
```
user=User(username='xx',pwd='xx')

```

### 查询用户
```
User.query.all()
user = User.query.filter_by(username=self.username.data).first()
```

### 删除用户
```
user.delete
```
## 备注:
参考项目
https://github.com/guaosi/flask-api
cookiecutter-flask
## 命名规范
### 变量
```
long_task
```
### 函数
```
say_hello()
```


### shen生成表结构
```
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_role --outfile "auth_role.py" --flask
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_admin --outfile "auth_admin.py" --flask
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_permission --outfile "auth_permission.py" --flask
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_permission_rule --outfile "auth_permission_rule.py" --flask
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_role --outfile "auth_role.py" --flask
flask-sqlacodegen "mysql+pymysql://cqtest:Pa44w0rd%21%40%23%24@106.52.100.60/MyEducationSys?charset=utf8mb4" --tables auth_role_admin --outfile "auth_role_admin.py" --flask

```

### unpacka_obj
```aidl
a = Model.first()
unpack_obj(a,'id','name','city.id','city.name','user.name')
```
