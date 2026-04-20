# 转换aync
- 由于`learning-site`的内容真正保存目录为`content`目录，我的`sub module`目录在`sources`内部
- 并且文件路径读取机制的原因，`learning-site`的文件路径读取相比`YEEZUS-obsidian`多了一层`content`的路径
需要对于原`sub module`的两个板块`yeezus`和`imdwaay-learning`进行aync转换，运行脚本的命令如下( 当前在`learning-site`根目录 )
```bash
bash scripts/sync-content.sh
```