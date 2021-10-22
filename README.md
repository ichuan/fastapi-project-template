# Fastapi Project Template

Includes:
- fastapi
- supervisor
- sqlite
- comandline scripts

## Usage

```sh
mkdir hello_world && cd hello_world
wget https://github.com/ichuan/fastapi-project-template/archive/master.tar.gz -O - | tar --strip-components 1  -xf -
# Choose a name for your fastapi project (package)
bash bootstrap.sh
```

## Additional
Consider using [fastapi-bearer-auth](https://github.com/ichuan/fastapi-bearer-auth) for JWT token auth.
