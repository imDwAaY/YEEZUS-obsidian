---
tags:
  - "#CS144"
  - "#IP"
  - "#UDP"
  - "#互联网四层模型"
source: Week 1 Friday _ Week 2 Monday_ Reliability
---
# 互联网四层模型
![[notes/CS144/static/截屏2026-03-10 09.04.10.png]]
- - -
# Internet Protocol
Internet Protocal简称`IP`，是互联网四层模型中`Network Layer`中一层的概念
## IP的功能
- 输入：(目标 IP 地址, 数据载荷( payload ))
- 输出：IP数据报，包含了：
	- - source IP address（源 IP 地址）
	- destination IP address（目标 IP 地址）
	- TTL( Time to LIve )
	- payload( 真正传输的数据 )
	- protocol
## Best-effort Delivery
`Best-effort Delivery`是IP的一个特点，它表示网络尽力而为的特性，但是不承诺结果
note 里列出了多种可能情况：
- Delivered once  
    送达一次
- Never delivered  
    根本没送到
- Delivered n > 1 times  
    送达了多次
- Delivered with altered or truncated payload  
    内容被改了，或者被截断了
- Delivered to wrong destination  
    送错地方了
- Delivered after another datagram that was sent later  
    后发的包先到了，顺序乱了
- - -
# UDP( User Datagram Protocol )
UDP 接收的输入比 IP 多一个东西：
- 目标 IP 地址
- 目标端口号 dst port
- payload
UDP 会把它封装成一个 **User Datagram**，里面包含
- source port
- destination port
- payload
然后这个 UDP 数据报会作为 **IP 的 payload**，再交给 IP 去发送。
## IP和UDP的主要区别
> The fundamental difference between UDP and IP is that UDP is port-to-port, while IP is host-to-host.

操作系统为每个用户程序分配不同的端口，避免相互干扰.
需要注意的是，IP和UDP都是`unreliable`
- - -
# 常见问题与解答
## Q1: 数据在传输中被篡改怎么办？
- UDP 和 IP 都包含一个**轻量级校验和（checksum）**，用于检测数据是否被篡改。
- 如果校验失败，数据报可能被丢弃。
## Q2: Firefox 如何知道目标端口？
- 类似于知道目标 IP 地址，通常由应用程序（如浏览器）根据服务类型确定。
- 配置文件如 `/etc/services` 中记录了常见服务的端口号。
## Q3: Firefox 如何知道自己的源端口？
- 由操作系统内核自动分配，确保不与其它程序冲突。
## Q4: 如何接收数据？
- 使用 `UDPSocket::recv`，可以获取源地址和数据载荷。
## Q5: 是否必须使用 `/etc/services` 中指定的端口？
- 不一定，服务可以运行在任意端口上，只要客户端知道即可。
- - -
# 协议栈与模块化
- 协议栈由多个模块组成，每一层只与上下层交互，不需要知道整个世界的全部细节
- 每一层通过**服务抽象（service abstraction）向上层提供服务**
## UDP和IP的分层关系

![[notes/CS144/static/截屏2026-03-10 09.23.58.png]]
唯一需要注意的一点就是:
> Routers only look at the IP layer, not the application payload.
- - -
# 如何在 UDP 上构建可靠性？

## 示例：可靠的数据检索服务
- 服务名：`host cs144.keithw.org`
- 实现方式：
    - 客户端不断发送请求，直到收到响应
    - 最终要么返回结果，要么超时
- 这种“可靠检索”适合**只读操作**，重复请求不会造成问题
## 可靠检索 vs 可靠动作
- **可靠检索**：可以重复请求，适合查询类操作
- **可靠动作**：如“发射鱼雷”，必须确保只执行一次
- 服务的设计取决于它提供的**可靠性类型**