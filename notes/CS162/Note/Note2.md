---
tags:
  - CS162
  - "#Thread"
  - "#Address_Space"
  - "#Process"
  - "#Protection_And_Isolation"
  - "#Dual_Mode_Operation"
  - "#Time_Multiplexing"
  - "#Abstraction"
---
这次介绍的是四大基本OS概念:`Thread`, `Address Space`, `Process`, `Dual Mode Operation`。这次的Note内容是对上一次[Note](notes/CS162/Note/Note1.md)的一些补充和扩展,比如对于`Thread`等概念进行了阐述。
# Thread
在原课件中的定义是:
> Thread: Single unique execution context:
> Program Counter, Registers, Execution Flags, Stack, Memory State

这里就是在描述，**线程是程序执行时的上下文**，它完整描述着程序的状态:
- Program Counter( PC )
- Registers
- Execution Flags
- Stack
知道上面这四样东西，就知道程序本身就正在处于什么状态。这也是为什么`thread`的核心不是代码本身，而是**当前的执行状况**。
当一个`thread`正在某个core上执行的时候，它的状态是`resident in processor registers`，也就是寄存器保存了线程的根状态( 上下文 ):
- PC在寄存器里
- 寄存器内容就是它的执行状态
- stack pointer也在寄存器里
- CPU正在按照这个线程的上下文执行
下面这张图展现了程序执行时真正的流程
![[截屏2026-03-29 23.24.05.png]]
## Core单核跑多线程原理
原理很简单，因为`OS`在做`Time Multiplexing #Time_Multiplexing 
![[截屏2026-03-29 23.43.38.png|218]]![[截屏2026-03-29 23.44.03.png|463]]
如果我们以足够细的颗粒度来执行每个thread，就会看起来像是有很多虚拟CPU跑线程。在这个过程中也传递了PC，SP还有registers:
- OS 保存 vCPU1 的 PC、SP、registers 到它的 TCB
- OS 从 vCPU2 的 TCB 恢复 PC、SP、registers
- CPU 跳转到 vCPU2 的 PC 开始执行
OS通过时间复用( Time Multiplexing )让多个线程轮流占用物理core，于是每个线程都看起来像有一个自己的core。
> 需要提醒的是: **thread本身就是virtual CPU**
## TCB
当`thread`不执行的时候，它的上下文就不会驻留在CPU里，而是保存到内存中，通常会保存在一个专门的数据结构里面:
- **TCB = Thread Control Block**
这也让线程可能处于两种位置:
- 在物理核心上执行
- 在内存中的TCB里被保存
这也是**线程是虚拟CPU**的根本原因
- - -
# Address Space
在原课件中的定义是:

>Address space = the set of accessible addresses + associated state：
> 32 位：$2^{32}$ 地址  
> 64 位：$2^{64}$地址

这句话表明的是地址空间是程序能够访问的地址集合，以及与这些地址相关的状态。注意不是简单的内存区域，与地址相关的状态涉及到了:
- 哪些地址程序能读，哪些地址程序能写
- 对这些地址访问有什么效果
典型的地址空间布局如下图所示
![[截屏2026-03-30 16.10.27.png|196]]![[截屏2026-03-30 16.13.07.png|441]]

地址空间这个概念存在的必要性，正是体现在**限制程序可见和可访问的内存范围**这一方面，确保每个程序只看到属于自己的那部分地址。
我们先前提及到的 #Time_Multiplexing,每个vCPU都有权限访问非CPU资源，每个线程都可以读写内存，这就导致了线程很有可能篡改`OS`的内容？也有可能篡改别的线程的内容？我们就思考硬件该怎么帮助`OS`免受进程的非法篡改？这就引出了`B&B`，是一种限制线程访问内存权限的方法
![[截屏2026-03-30 16.48.02.png]]
## Base And Bound
![[截屏2026-03-30 16.30.21.png]]
这是一种很基础的机制，我们有两个`register`，分别是`base register`和`bound register`。程序发出的地址不会直接拿去访问物理内存，而是会先检查:
- 是否在合法范围内
- 或者和base做转换后是否落在允许的区域内( 段基址+偏移地址 )
## Virtural Address Space
这是一种更一般的思想:
> 程序运行在一个和物理内存不同的地址空间里: 程序看到的是virtual address，真正访问的是physical address，中间要经过translation

![[截屏2026-03-30 16.49.08.png]]
这带来了两个巨大好处:
- 程序看不到不该看的内存
- 程序不再需要连续放在物理内存里
## Paged Virtual Address Space
![[截屏2026-03-30 16.52.37.png]]
这是一种分页思想，把整个虚拟地址空间分成固定大小的块，同时把整个物理内存也切成同样大小的块，然后由硬件通过`page table`完成映射。
需要注意的是：
- 每个 virtual page 可以映射到任意 physical frame
- 页面大小固定，管理更方便
- 如果某页不在内存里，访问会触发 **page fault**
其中虚拟地址可以看成`<Page #> + <Page Offset>`，其中`<Page #>`用来查page table，`<Page Offset>`直接保留，最后组合出了真实的physical address
**这是进程隔离最重要的底层机制之一**
- - -
# Process
原课件的定义:
> execution environment with Restricted Rights
	> - **(Protected)** Address Space with One or More Threads
	> - Owns memory **(address space)**
	> - Owns file descriptors, file system context, …
	> - Encapsulate one or more threads sharing process resources

为什么需要Process这个定义？
- Process彼此隔离
- OS也需要被保护
- 进程提供内存保护边界
还需要注意的一点是**进程内通信容易，进程间通信更难**，原因也很简单:同一进程的多个线程共享很多资源；不同进程彼此隔离不共享`Address Space`，要通信就必须通过`OS`提供的机制
## Single and Multithreaded Processes
![[截屏2026-03-30 17.32.00.png]]
为什么一个进程要有多个线程？
1. Parallelism: 利用多核硬件并行执行
2. Concurrrency: 更容易处理 I / O和多个同时发生的事件
## PCB
每个`Process`有一个`PCB`,这可以看成`thread`在内核中的官方档案，`TCB`则更偏向于线程执行状态档案。`TCB may be inside PCB` PCB包含了:
- 状态( running, ready, blocked )
- registers状态 
- Process ID( PID ), User, Executbable, Priority
- 执行时间
- 内存空间和地址翻译信息
- - -
# Protection And Isolation
我们再次回顾一下刚才放的一张图，这就是我们采取保护和隔离的目的
![[截屏2026-03-30 16.48.02.png]]
但是仅有地址空间隔离还不够，即使有page table/ address translation，为什么进程不能自己改page table ptr？为什么不能直接发I/O指令绕过OS？我们就必须再加上权限控制，这就引入了:`Dual Mode Operation`
- - -
# Dual Mode Operation
`Dual Mode Operation`的含义是硬件至少提供两种模式: Kernel Mode和User Mode。User Mode权限受限，不能做敏感操作；Kernel Mode拥有完整硬件访问能力。
课件中列出的User mode不能做的东西包括:
- changing the page table pointer
- disabling interrupts
- interacting directly with hardware
- writing to kernel memory
我们可以通过Unix System Structure的结构来理解`Dual Mode Operation`，下图所示的便是Unix。
![[截屏2026-03-30 18.12.33.png]]
![[截屏2026-03-30 18.23.34.png]]
## User -> Kernel 的三种方式
### Syscall
进程主动请求系统服务，比如:
- exit
- open
- read
- write
### Interrupt
外部的异步事件触发，比如:
- timer interrupt
- I/O device interrupt
### Trap/Exception
进程内部的同步异常触发，比如:
- divide by 0
- protection violation( segment fault )
这是一种因为硬件/异常机制强制切换控制流
- - -
# OS加载进程的真实过程
## 第一步: OS在kernel mode下准备进程
 OS会在这一步设置一些基本的`Base`, `Bound`, `user PC`,`other oregisters`
 需要注意的是`B&B`只有在`sysmode = 1`的时候才可以填写
## 第二步: RTU( Return to User )
OS执行返回User mode，开始从用户PC执行用户程序
## 第三步: 执行用户代码
此时程序运行在受保护的地址空间里，内核暂时放手
## 第四步: 内核重新拿回控制权
通过`timer interrupt`还有`I/O request / interrupt`还有`exception / trap`来重新拿回控制权，这在[User -> Kernel](notes/CS162/Note/Note2.md#User%20->%20Kernel%20的三种方式)是提及到过的
## 第五步: 发生中断后
硬件会：
- 保存用户 PC
- 切换到 kernel mode
- 跳到 interrupt vector 对应的 handler
## 第六步: OS可能进行调度
如果决定换一个线程/进程来运行:
- 就会选择保存当前`thread`到`TCB`
- 恢复下一个`thread`的`TCB`
- 再`RTU`