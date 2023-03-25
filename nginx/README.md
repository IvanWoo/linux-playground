# NGINX

we use [OpenResty](https://openresty.org/en/).

## operations

### check the config

```sh
openresty -p $PWD/ -t
```

### start the server

```sh
openresty -p $PWD/
```

### check processes

```sh
ps aux | grep nginx
```

### ping the server

```sh
curl 'http://127.0.0.1:8080/ping'
```

### reload

```sh
/usr/local/openresty/nginx/sbin/nginx -s reload
```

## lifecycle

Nginx 处理请求的过程一共划分为 11 个阶段，按照执行顺序依次是 post-read、server-rewrite、find-config、rewrite、post-rewrite、preaccess、access、post-access、try-files、content 以及 log

## ref

- [agentzh 的 Nginx 教程](https://openresty.org/download/agentzh-nginx-tutorials-zhcn.html)
