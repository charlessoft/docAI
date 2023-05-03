# 接口修改记录

1. word2vec_train
```
[{"w":"中国"},{"w":"机器学习"}]
修改:
[{"word":"中国"},{"word":"机器学习"}]
```

Makeifile
myapp
find . -name "*.py" |xargs sed -i '' 's/textminer/myapp/g'

增加新接口.
在index.py目录下增加,并写入__init__.py中
myapp/api/v1/resources

```
from . import index
```
