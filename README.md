This needs the ensmallen Conan recipe from [here](https://github.com/hheld/ensmallen-conan). Build like this:

```shell
conan create -s build_type=Debug -pr:b=default .
conan create -s build_type=Release -pr:b=default .
```