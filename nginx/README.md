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
