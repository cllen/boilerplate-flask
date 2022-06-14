# 简介

这是接口文档。

# 约定

1. 所有接口都要在前面加上`http://<域名>`。

# base模块接口

略

# wechat模块接口

#### 微信小程序登录

- URL: `/boilerplate/wechat/api/v1/user`
- METHOD: `POST`
- CONTENT-TYPE: `application/json`
- REQUEST-PARAM:
```JSON
{
    'code':<str, 用户的微信小程序code>,
}
```
- RESPONSE:
```JSON
{
    'error_code':<int, 错误代码>,
    'token':<str, 用户token>,
}
```
- NOTE:
    1. 返回的token，在请求其他接口时候，格式为`headers={'authorization':'wechat <token>'}`，如`headers={'authorization':'wechat xxx'}`

#### 微信小程序更新用户信息（授权，包括敏感信息）

- URL: `/boilerplate/wechat/api/v1/user`
- METHOD: `PUT`
- CONTENT-TYPE: `application/json`
- REQUEST-HEADERS:
```JSON
{
    'content-type':'application/json',
    'authorization':'wechat <token>',
}
```
- REQUEST-PARAM:
```JSON
{
    'iv':<str, 微信服务器返回的iv，参考微信小程序文档，登录部分>,
    'encrypted_data':<str, 微信服务器返回的encrypted_data，参考微信小程序文档，登录部分>,
}
```
- RESPONSE:
```JSON
{
    'error_code':<int, 错误代码>,
    'user':{
        'id':<int, 微信用户id>,
        'nickname':<str, 微信用户昵称>,
        'avatar':<str, 微信用户头像，是一个url>,
        'gender':<int, 微信用户性别>,
    }
}
```
- NOTE:
    1. 返回的token，在请求其他接口时候，格式为`headers={'authorization':'wechat <token>'}`

#### 微信公众号授权接口

略

#### 微信公众号授权回调接口

略

#### 微信公众号网关接口（接收来自微信服务器的消息，如关注、取消关注等事件）

略

# cms模块接口

略