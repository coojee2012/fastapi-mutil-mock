# Guess And SSR

## 项目在开发阶段

#### 介绍
Guess And SSR
前后端分离抽奖系统
* 后端框架：
>1. Python Web 框架：FastAPI
>2. ORM：SQLAlchemy

* 前端框架：Vue
>1. 手机界面：BootstrapVue
>2. 管理界面：ElementUI

#### 启动 

*后端*

* python版本 3.7.x
pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r .\requirements.txt
>1. 在GUESS_SSR目录下backend
>2. pip install -r requirements.txt
>3. python main.py
>4. 数据库迁移https://www.cnblogs.com/turingbrain/p/6372086.html

*前端*

* node版本: 12.13.x
* 安装好node和vue-cli

>1.  在fastapi-vue-blog/frontend目录下
>2.  安装依赖: npm install
>3.  启动开发: npm run dev
>4.  打包命令: npm run build 


#### 功能

*手机*

>1. 可以看到所有文章
>2. 可以看到所有分类
>3. 可以根据分类筛选文章列表
>4. 在文章中可以看到评论
>5. *可以根据关键词搜索文章

*管理员*

>1. 文章管理
>2. 分类管理
>3. 评论管理
>4. 使用MarkDown编写文章

#### 前端URL

##### 游客

*首页*

* /posts?page=1&limit=10 显示所有文章›
* /post?category=python 分类文章显示
* /posts/<post_id: int> 文章详细

*分类*

* /categories 显示所有分类

##### 管理员

* /manage/posts       文章管理
* /manage/post?       文章编辑/创建
* /manage/categories  分类管理
* /manage/category?   分类编辑/创建
* /manage/comments    评论管理
* /manage/comment     评论编辑

#### 后端API

*文章*

* GET /api/v1/posts/?category=python&page=1&limit=10 显示所有文章 分类文章显示
* POST /api/v1/posts/                 创建文章
* GET /api/v1/posts/<int: post_id>    获取单个文章
* PUT /api/v1/posts/<int: post_id>    修改文章
* DELETE /api/v1/posts/<int: post_id> 删除文章

*评论*

* GET     /api/v1/comments/? 所有评论
* POST    /api/v1/comments/ 创建评论
* DELETE  /api/v1/comments/ 删除评论
* GET     /api/v1/comments/<int: comment_id> 获取单个
* PUT     /api/v1/comments/<int: comment_id> 编辑单个评论

*分类*

* GET     /api/v1/categories/ 所有分类
* POST    /api/v1/categories/ 添加分类

*登录*

* GET /api/v1/login/access-token 登录获取token

#### 插图

![avatar](./introduce/frontend_posts.jpg)
![avatar](./introduce/frontend_categories.jpg)
![avatar](./introduce/frontend_about.jpg)
![avatar](./introduce/frontend_post_create.png)
![avatar](./introduce/frontend_manage_categories.jpg)
![avatar](./introduce/backend_api_photo.png)

#### 使用alembic

自动创建版本
使用alembic revision -m “注释” 创建数据库版本，上面我们修改了配置文件alembic/env.py，指定了target_metadata，这里可以使用–autogenerate参数自动生成迁移脚本。

$ alembic revision --autogenerate -m “initdb”

其他常用参数
更新数据库
$ alembic upgrade 版本号

更新到最新版
alembic upgrade head

降级数据库
$ alembic downgrade 版本号

更新到最初版
alembic downgrade head

离线更新（生成sql）
alembic upgrade 版本号 --sql > migration.sql

从特定起始版本生成sql
alembic upgrade 版本一:版本二 --sql > migration.sql

查询当前数据库版本号

init：创建一个 alembic 仓库。
revision：创建一个新的版本文件。
--autogenerate：自动将当前模型的修改，生成迁移脚本。
-m：本次迁移做了哪些修改，用户可以指定这个参数，方便回顾。
upgrade：将指定版本的迁移文件映射到数据库中，会执行版本文件中的 upgrade 函数。如果有多个迁移脚本没有被映射到数据库中，那么会执行多个迁移脚本。
[head]：代表最新的迁移脚本的版本号。
downgrade：会执行指定版本的迁移文件中的 downgrade 函数。
heads：展示head指向的脚本文件版本号。
history：列出所有的迁移版本及其信息。
current：展示当前数据库中的版本号。另外，在你第一次执行 upgrade 的时候，就会在数据库中创建一个名叫 alembic_version 表，这个表只会有一条数据，记录当前数据库映射的是哪个版本的迁移文件。

查看alembic_version表。
清除所有版本
将versions删掉，并删除alembic_version表
