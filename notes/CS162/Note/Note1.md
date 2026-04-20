---
tags:
  - "#CS162"
  - "#Operating_System"
  - "#Process"
  - "#Thread"
  - "#Address_Space"
  - "#File_System"
  - "#Socket"
  - "#Abstraction"
---
- 为应用程序提供**统一的硬件接口**，隐藏底层差异# Operating System
首先我们要清楚的是，操作系统并没有一个统一接受的权威定义:
- 有一种的广义定义:**"操作系统是厂商随计算机一并提供的所有软件的集合"**，但不同系统之间差异又非常大
- 还有一种狭义定义:**操作系统是计算机上始终运行的一个程序，是一个内核( kernel )，其余为系统程序或应用程序**
> 总的来说，核心理解是:
**OS is the special software layer between hardware and applications.**  它位于硬件和应用程序之间，负责向上提供抽象，向下管理硬件

![[notes/CS162/static/截屏2026-03-21 18.05.17.png]]
## OS的三个角色
### 1.Referee( 管理者 )
OS 要负责管理资源，并防止不同程序互相干扰，其中核心任务包括了:
- **protection（保护）**
- **isolation（隔离）**
- **sharing（共享）**
- **resource allocation（资源分配）**
- **communication（通信管理）**
`OS`在这里起到了协调各个程序之间冲突的功能，防止应用程序之间的互相干扰
### 2.Illusionist( 幻象制造者 )
这里的含义是`OS`会让程序感觉自己面对的是一个更简单，更干净的机器世界。`OS`在这个过程中把底层复杂，难用的硬件包装成了简单易使用的抽象
- 明明物理内存有限，但程序像在使用“很大的连续内存”
- 明明 CPU 要同时跑很多程序，但每个程序都像“独占 CPU”
- 明明底层是磁盘块、控制器、中断，但程序看到的是“文件”
- 明明底层是网卡、协议栈、缓冲区，但程序看到的是“socket”
这个过程叫做**Virtualization(虚拟化)**,本质就是在用抽象掩盖底层复杂性和限制
### 3.Glue( 粘合剂 )
`OS`会给很多应用提供很多公共服务，把整个系统粘合起来，主要包括了:
- **Storage**
- **Window system**
- **Networking**
- **Sharing**
- **Authorization**
从用户和应用角度看，操作系统往往承担一整套公共基础设施的角色。
## Hardware Interface And Software Interface
首先考虑一个问题: 什么是抽象 : **抽象为应用程序提供统一的硬件接口，隐藏底层差异**
OS 夹在硬件和程序之间，所以有两个接口层次：
- **Physical Machine Interface**：硬件本来的接口
- **Abstract Machine Interface**：OS 提供给程序的抽象接口
对于任何OS子领域，都要问两个问题:
1. 底层真实硬件接口是什么？
2. OS希望给软件提供更好的抽象？

例如:
- 物理处理器( Processor ) → OS 抽象成 **Thread**
- 物理内存( Memory ) → OS 抽象成 **Address space**
- 磁盘 / SSD( Disks/SSDs ) → OS 抽象成 **Files**
- 网络硬件( Networks ) → OS 抽象成 **Sockets**
- 整台机器资源( Machines ) → OS 抽象成 **Processes**
- - -
# 操作系统核心抽象
## 1.进程( Process )
我们把进程定义为:
>**Process: Execution environment with restricted rights provided by OS**  
  进程是 OS 提供的一种“受限权限的执行环境”。

一个进程包含了:
- **Address Space( 地址空间 )**
- **One or more threads of control**
- 以及附加系统状态，例如：
    - **Open files**
    - **Open sockets**
我们一定要注意一下`Program`还有`Process`的区别: 一个程序可以启动多个进程，同时每个进程都是一个独立运行实体。简单来说Process是动态的，是程序运行起来后的实例。而`Program`是静态的，它是一个可执行文件/代码。
## 2.线程( Thread )
这一讲没有进行过多的展开讲解，线程是进程内部的执行流，同时一个进程可以有一个或多个线程去掌控
## 3.地址空间( Address Space )
地址空间是`OS`提供给进程的内存视图，程序看到的是自己所占有的地址空间，而不是整个物理内存的真实分布状态.。通过这样可以实现如下的作用:
- 让程序觉得自己有一块连续、私有的内存
- 实现进程之间的隔离
- 支持保护和虚拟内存机制
## 4.文件系统( File System )
文件是对持久化存储的抽象。  底层其实是磁盘块、SSD 页面、控制器、缓存等复杂机制，但程序使用的是“打开文件、读写文件、关闭文件”这种简单接口.
## 5. 套接字( Socket )
socket 是对网络通信的抽象。  底层涉及网卡、协议栈、缓冲区、IP、端口等复杂内容，但 OS 抽象成统一通信接口。