#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <errno.h>
#include <unistd.h>
#include <syslog.h>
#include <time.h>
#include <sys/stat.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <string>

/**
g++ ssl_client_enc_noauth.cpp -o ssl_client_enc_noauth -lcrypto -lssl
*/

void hostname_to_ip(const char *hostname, char *ip)
{
    int sockfd;
    struct addrinfo hints, *servinfo;
    struct sockaddr_in *h;
    int rv;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ( (rv = getaddrinfo(hostname , NULL , &hints , &servinfo)) != 0)
    {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        exit(1);
    }

    h = (struct sockaddr_in *) servinfo->ai_addr;
    strcpy(ip , inet_ntoa( h->sin_addr ));

    freeaddrinfo(servinfo);
}

void init_openssl()
{
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
}

void cleanup_openssl()
{
    EVP_cleanup();
}

int main(int argc, char **argv)
{
    int sock, port = 465;

    const char *hostname = "smtp.gmail.com";
    char ip_addr[1024], buff[1024];

    hostname_to_ip(hostname, ip_addr);

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    inet_aton(ip_addr, &server_addr.sin_addr);

    // create regular socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket");
        exit(1);
    }

    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1)
    {
        perror("connect");
        exit(1);
    }

    // init openssl
    init_openssl();

    // ssl context
    SSL_CTX *ctx = SSL_CTX_new(TLSv1_2_method());
    if (!ctx)
        return -1;

    // create secure socket
    SSL *ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);

    // connect using secure socket
    int result = SSL_connect(ssl);

    if (result == 0)
    {
        long error = ERR_get_error();
        const char* error_str = ERR_error_string(error, NULL);
        printf("%s\n", error_str);
        return 0;
    }

    std::string greeting = "EHLO user\r\n";

    SSL_write(ssl, greeting.c_str(), greeting.size());
    SSL_read(ssl, buff, 1024);

    printf("%s\n", buff);
    memset(buff, 0, 1024);

    close(sock);
    SSL_CTX_free(ctx);

    cleanup_openssl();

    return 0;
}
