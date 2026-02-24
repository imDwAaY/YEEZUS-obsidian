## 内容须知
### Node版本差异
前后端所用 [[Node]] 版本不一样
前端 Node 版本为<span class="bold">{node: 'v22.21.1', npm: '10.9.4'}</span>
由于全局[[Node]]版本为v16.20.2，需要借助nvm工具来实现前后端不同Node版本。

### 实现过程
进入bash后输入临时切换局域Node版本
```
nvm use 22
```
借助yarn启动服务
```
yarn serve
```
端口输出
```
  App running at:
  - Local:   http://localhost:3001/ 
  - Network: http://10.69.162.198:3001/
```
