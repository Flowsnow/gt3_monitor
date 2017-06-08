使用pyinstaller打包gt3_app
===

本次项目需要连接到数据库查询一些信息，因此使用pyinstaller打包时需要将数据库依赖加载到包中，否则打出来的包不支持会报错：Unable to acquire Oracle environment handle

## 解决pyinstaller自身依赖

使用pyinstaller打包报错找不到libpython2.7mu.so.1.0等文件，参考以下链接解决：https://segmentfault.com/q/1010000009512503

具体解决方案：重新编译打包服务器上的python2.7安装包，使用./configure --enable -shared，然后make && make install即可

## pyinstaller打包流程

### 第一步：无依赖打包

```shell
pyinstaller -F gt3_app
```

`-F`选项表示打包成一个可执行文件，不加-F会打包成一个文件夹

### 第二步：修改gt3_app.spec打包配置文件

在gt3_app.spec中加入数据库依赖

```python
# -*- mode: python -*-

block_cipher = None


a = Analysis(['gt3_app.py'],
             pathex=['/tmp/gt3_monitor'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.binaries = a.binaries + [('libclntsh.so', 'libclntsh.so.11.1','BINARY')]
a.binaries = a.binaries + [('libnnz11.so', 'libnnz11.so','BINARY')]
a.binaries = a.binaries + [('libocci.so', 'libocci.so.11.1','BINARY')]
a.binaries = a.binaries + [('libocijdbc11.so', 'libocijdbc11.so','BINARY')]
a.binaries = a.binaries + [('libociei.so', 'libociei.so','BINARY')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gt3_app',
          debug=False,
          strip=False,
          upx=True,
          console=True )

```

将五个so文件`libclntsh.so.11.1`，  `libnnz11.so`，  `libocci.so.11.1`，  `libociei.so`，  `libocijdbc11.so`按照二进制的方式加入到spec文件中。这5个文件需要和当前项目在同一级目录中，否则需要修改上述spec文件中的路径。如果没有这5个文件，可以通过安装oracle客户端得到，安装oracle客户端的步骤的命令

```shell
rpm -ivh oracle-instantclient11.2-basic-11.2.0.3.0-1.x86_64.rpm
```

安装好之后5个so文件存放在`/usr/lib/oracle/11.2/client64/lib`下，然后拷贝到当前目录即可。

### 第三步：按照spec文件重新打包

```shell
pyinstaller -F gt3_app.spec
```

打出的包存放在项目目录下的dist目录中。后续代码修改后只需要更新打包服务器上的代码，然后按spec文件再次打包即可。

> 注意：如果是按照无依赖打包执行之后会覆盖掉gt3_app.spec文件，记得备份