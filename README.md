# 简介

这是flask应用模板。

# 功能

1. basic http登录。
2. 微信小程序登录、微信公众号登录、微信支付。
3. 文章管理（实例功能，暂时没有更新）。

# 第三方

1. flask
2. flask-sqlalchemy
3. flask-restx
4. Flask-Bootstrap
5. marshmallow

# 版本

1. 代码未经过测试，尚未有稳定版本。

# 使用

##### 安装、运行、卸载（安装在宿主机器上）

1. 修改配置文件：

```shell
cp config.conf.example config.conf

vim config.conf
```

2. 执行安装脚本：

```
bash install.sh
```

3. 安装成功，如需卸载，执行卸载脚本：

```shell
bash uninstall.sh
```

##### 安装、运行、卸载（安装在docker容器里）

略

```
