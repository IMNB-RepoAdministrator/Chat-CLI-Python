from shared import sock_create

def create_tcp_connection(serv_addr : tuple[str, int]):
    tcp_serv_sock, tcp_serv_addr = sock_create.create_TCPsocket(serv_addr)
    tcp_serv_sock.connect(serv_addr)
    
    return tcp_serv_sock, tcp_serv_addr