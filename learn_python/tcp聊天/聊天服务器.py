import socket


def main():
    # 1.创建套接字
    tcp_sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.插手机卡（绑定本地信息）
    tcp_sever_socket.bind(("", 7890))
    # 3.将手机设置为正常的响铃模式（让默认的套接字由主动变为被动listen）
    tcp_sever_socket.listen(128)

    while True:
        print("等待一个新的客户端的到来。。。")
        # 4.等待别人的电话到来（等待客户端的链接）
        new_client_socket, client_addr = tcp_sever_socket.accept()
        print("一个新的客户端已经到来%s" % str(client_addr))

        while True:
            # 接收客户端发送过来的请求
            recv_data = new_client_socket.recv(1024)
            print("客户端发送过来的请求是：%s" % recv_data.decode("utf-8"))
            # 回送一部分数据给客户端
            new_client_socket.send("hhhhhhh----ok----".encode("utf-8"))

            #如果recv堵塞，那么有2种方式
            # 1.客户端发送过来数据
            # 2.客户端调用close导致recv堵塞

            if recv_data:
                # 回送一部分给客户端
                new_client_socket.send("hhhhhh".encode("utf-8"))
            else:
                break

        # 关闭套接字
        new_client_socket.close()
        print("服务器已经完毕。。。")

    # 如果将监听套接字关闭，会导致accep失败
    tcp_sever_socket.close()


if __name__ == "__main__":
    main()
