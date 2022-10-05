### Create own CA (Certificate Authority) and self-signed certificate

We need to follow these steps to generate self-signed certifcate to secure the gRPC connection.

- Generate CA’s private key and its self-signed certificate.
- Generate server's private key and certificate signing request (CSR).
- Use CA’s private key and cert to sign the server’s CSR to generate server's self-signed certificate.

__Generate CA’s private key and its self-signed certificate__

First create a directory where you want to keep all the generated keys and certs. 

```bash
(main) expert@expert-cws:~/cisco-mdt-tig$ mkdir certs && cd certs
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

Run the following command to generate CA's private key and its cert. You can change the details in `-subj` flag if you like. 

```s
openssl req -x509 -newkey rsa:4096 -days 3650 -nodes \
        -keyout ca-key.pem -out ca-cert.pem \
        -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=devnetbro.com \ emailAddress=admin@devnetbro.com"
```

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl req -x509 -newkey rsa:4096 -days 3650 -nodes \
>         -keyout ca-key.pem -out ca-cert.pem \
>         -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=devnetbro.com \ emailAddress=admin@devnetbro.com"
Generating a RSA private key
..................................................................................++++
......++++
writing new private key to 'ca-key.pem'
-----
(main) expert@expert-cws:~/cisco-mdt-tig/certs$
```

View the `ca-cert.pem` in human readable format 

`openssl x509 -in ca-cert.pem -noout -text`

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl x509 -in ca-cert.pem -noout -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            20:e5:cd:ea:35:6b:50:53:81:aa:e0:74:93:51:10:59:ad:0e:57:19
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com  emailAddress=admin@devnetbro.com
        Validity
            Not Before: Oct  4 22:36:46 2022 GMT
            Not After : Oct  1 22:36:46 2032 GMT
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com  emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:c4:a7:5d:94:81:f8:21:19:c7:f6:99:54:5b:91:
                    07:0d:26:e6:4d:d0:ae:3c:0e:00:6b:d7:7e:3a:f7:
                    7d:26:69:2d:06:36:20:1d:f9:d8:ca:65:64:ca:a3:
                    9f:c8:75:9c:cc:96:b8:0b:e9:9a:ff:24:5e:f5:00:
                    42:ee:bf:e4:69:af:d0:52:3b:5b:b6:ac:6e:63:58:
                    29:0e:d0:a2:5b:59:cc:40:55:73:e3:88:a3:fe:4d:
                    02:67:7d:07:75:47:fb:c3:70:f5:4c:2e:b5:91:96:
                    0a:c4:29:d3:2a:4c:c3:11:f0:e2:e6:49:4a:08:be:
                    b0:e2:29:62:1f:01:a3:72:f5:59:0c:89:19:de:70:
                    f9:66:ab:a3:cd:f9:36:76:f0:70:c9:cd:23:47:0a:
                    3c:52:70:a8:84:1d:a2:68:6d:e7:f7:61:52:83:bb:
                    88:15:02:a3:b3:1e:44:63:4e:61:5a:27:ba:d9:15:
                    de:2f:58:ec:3a:5d:73:e5:6d:2f:d5:d6:3b:3d:23:
                    00:f5:89:a6:e3:ce:26:f7:2c:5c:03:63:bd:06:fa:
                    ad:fe:f2:be:b7:a5:4b:1a:2a:e7:e8:55:61:51:2f:
                    30:ce:e9:a4:a8:03:47:5a:a8:e2:76:2a:d2:e0:2b:
                    d2:98:51:2f:7b:61:0a:eb:5d:14:3b:74:e8:05:35:
                    dc:7e:24:02:23:a1:02:14:87:ff:c4:50:29:21:fd:
                    f5:c1:53:ee:13:9a:93:65:d4:fb:82:4a:f9:97:25:
                    1c:7b:d4:5b:09:b8:54:04:ee:92:fb:57:c6:20:dc:
                    f6:33:74:6e:61:28:36:28:b6:8e:df:97:0f:6a:fe:
                    2f:51:cc:ac:d8:b9:3d:49:81:14:ba:37:22:ba:ec:
                    3a:6a:b0:ec:02:b1:f1:28:50:bb:99:c6:69:71:8f:
                    1b:8b:b5:39:b4:dd:40:0f:1f:ef:1b:07:38:96:d9:
                    fb:7d:2a:0c:50:dc:2c:f4:a9:c7:51:c2:14:ff:6e:
                    74:2c:34:43:ac:ca:67:6c:3c:51:ec:e2:03:9f:f4:
                    bb:5e:ec:b7:20:56:17:1a:0d:dd:5c:85:5e:0e:57:
                    96:7f:ee:71:fd:62:fe:a4:dd:5f:c6:db:85:eb:82:
                    a1:7b:23:5c:59:fc:5e:39:77:04:81:f0:bd:4c:71:
                    47:6e:bd:a4:9b:21:b9:32:19:1d:d2:d6:4c:03:80:
                    bc:cb:ca:32:31:ea:0e:e8:be:ab:3a:b3:b9:22:3f:
                    12:ce:f5:c8:ce:61:c2:c9:ba:b6:e8:ca:c1:6c:27:
                    7b:b6:5c:ea:3d:94:63:a4:15:8c:c2:ba:78:d5:e3:
                    64:03:90:df:ad:15:54:7d:5c:80:17:1c:74:7c:9d:
                    90:07:29
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                DF:79:00:48:DA:E6:31:2A:1D:F3:2A:55:ED:13:6C:47:02:2A:87:18
            X509v3 Authority Key Identifier: 
                keyid:DF:79:00:48:DA:E6:31:2A:1D:F3:2A:55:ED:13:6C:47:02:2A:87:18

            X509v3 Basic Constraints: critical
                CA:TRUE
    Signature Algorithm: sha256WithRSAEncryption
         3b:a4:d9:96:43:c5:d7:b9:5c:70:c3:f0:8f:24:62:cd:d8:c0:
         6c:43:3f:b0:06:7f:a2:07:d2:b9:ad:4b:04:96:db:04:ad:84:
         fe:67:d4:f8:c0:79:24:06:30:4b:80:2a:55:c6:c6:42:03:36:
         fd:8a:cf:d4:98:c9:b1:a1:9d:65:a4:1d:5d:f6:49:e5:37:f5:
         01:21:b0:5f:36:3a:a2:1f:a7:53:a0:02:c9:61:7b:19:1e:92:
         09:be:c5:58:87:9e:ea:54:2c:2d:b0:d5:5e:83:fd:63:d0:d9:
         ec:3c:1d:3d:4e:b5:08:09:78:0e:a2:4e:aa:09:aa:4b:5d:05:
         43:24:2b:ca:a1:e0:f7:8d:4e:e6:3c:e0:09:e5:83:58:15:bf:
         11:7c:2e:9f:a3:79:07:f0:5b:42:72:50:c3:ab:1c:4d:8f:c0:
         0c:bd:2a:65:33:85:92:e9:40:c6:be:a3:1c:37:96:62:04:ff:
         22:ed:8b:de:f6:94:24:12:36:e0:42:11:47:e0:91:09:bd:bd:
         a0:15:25:7f:35:8e:fe:1c:55:2c:4d:de:fd:65:f1:9c:97:11:
         c2:f4:56:d9:6d:64:89:cf:e4:c2:f5:05:c2:e2:2a:b2:d3:78:
         40:45:ea:f9:3f:9a:1f:27:05:0b:37:ee:5d:9d:f5:cc:ca:33:
         1b:3b:ab:ba:71:6e:53:d9:96:1d:a7:26:94:6b:40:c8:7e:7b:
         1a:d0:a8:56:59:49:d9:86:ae:de:82:c8:4e:b9:ac:1f:b4:11:
         d2:00:19:ad:cd:f0:4d:9b:f8:58:99:76:80:72:e8:41:17:a3:
         f2:f8:a4:e8:27:e1:c7:22:72:b0:00:b0:58:1b:a0:78:43:c3:
         e9:28:6e:0a:46:49:66:f6:8f:98:9c:fe:ca:be:23:77:17:bd:
         38:56:fb:12:95:3d:da:83:e7:4f:5b:57:e6:9a:31:c5:f8:81:
         45:79:a4:ec:be:4b:fa:d6:4b:b3:59:72:8f:86:df:62:24:44:
         66:04:a9:50:ce:e3:fb:89:9d:8d:76:91:6b:ec:bb:f2:b6:bc:
         2c:f1:d5:88:c3:0e:a8:35:c2:56:16:18:d4:8c:56:f4:95:76:
         f0:ee:ca:c4:cd:6d:da:67:5e:7b:c3:f9:c7:83:3b:2e:b5:5c:
         85:f9:1a:75:71:cd:85:35:81:b3:e5:70:95:c4:9d:25:fe:49:
         26:2c:7e:e4:3a:3f:4b:fc:e5:91:f5:42:60:c9:5c:8c:03:9a:
         cf:4e:d1:f2:4f:8f:9f:bb:e5:fc:9b:40:10:d8:76:fb:c9:3d:
         c5:a2:86:55:64:b5:db:84:85:1c:95:30:e5:f7:38:36:40:fc:
         c7:81:5c:d3:61:9a:3e:3d
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

__Generate server's private key and certificate signing request (CSR)__

Run the following command to generate server's private key and CSR

```s
openssl req -newkey rsa:4096 -nodes \
        -keyout server.key -out server.csr \
        -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=grpc emailAddress=admin@devnetbro.com"
```

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl req -newkey rsa:4096 -nodes \
>         -keyout server.key -out server.csr \
>         -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=grpc emailAddress=admin@devnetbro.com"
Generating a RSA private key
..........................................++++
......................................................................++++
writing new private key to 'server.key'
-----
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

View the `server.csr` in human readable format 

`openssl req -in server.csr-noout -text`

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl req -in server.csr -noout -text
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:ef:d6:0e:5f:1c:29:37:29:72:39:6d:5a:21:3d:
                    4a:73:de:a6:2b:8f:24:3a:fd:c7:ea:5e:dd:1d:ee:
                    4e:f5:1e:df:45:6a:fc:7b:6d:f1:97:c2:40:eb:1e:
                    1a:b5:88:f0:ee:4e:f8:56:f5:77:24:09:6f:10:51:
                    34:d0:5d:38:b6:f3:d8:2d:64:93:23:5c:57:e8:cd:
                    f3:5e:bc:db:c0:c5:5d:a0:4f:83:a2:4a:93:fb:63:
                    c5:53:d5:e6:94:bf:8c:16:cd:e8:1b:88:61:91:2d:
                    25:49:8b:66:bb:a1:9b:e3:09:d0:4d:6b:bf:32:b2:
                    42:55:72:21:45:80:7a:e5:27:1d:42:df:c1:0d:ae:
                    11:2a:c9:c9:95:42:7d:27:1e:5d:85:a6:dc:2d:ce:
                    0c:14:16:8b:8b:e3:f5:28:86:39:e9:31:b9:59:53:
                    eb:70:fb:94:91:c3:74:d8:9b:dd:73:78:e4:78:26:
                    30:dd:5c:42:d7:95:c9:25:89:04:17:3d:e4:c7:a9:
                    8a:79:1f:c5:20:bb:1e:a6:ec:30:c3:40:04:70:9d:
                    7f:7c:00:d2:09:ec:74:0a:0d:eb:8b:08:be:97:5e:
                    57:ce:88:bd:e9:10:44:71:8f:e4:d7:61:eb:67:4a:
                    39:9b:56:0b:1a:2d:da:de:5d:b5:e3:71:27:27:f4:
                    1e:25:3e:b5:14:15:b4:c1:37:e8:ec:48:34:46:95:
                    b9:49:e5:5c:4b:1e:d0:84:f1:0b:3a:39:f7:fd:42:
                    6c:37:02:45:7f:b1:98:83:50:e5:4d:4e:86:fa:c8:
                    ec:11:8d:9e:05:0f:6b:35:6a:7e:66:4a:8b:79:45:
                    0a:e0:2f:bd:b1:f2:0e:7c:7e:77:62:a2:56:4d:ff:
                    90:7c:8f:6d:ff:86:c7:22:89:e2:b0:64:1c:e1:74:
                    5c:9d:2f:1c:b2:8f:d7:bc:72:70:79:db:5a:0c:79:
                    a8:8a:63:28:4c:7d:38:c8:a1:69:c4:43:4b:f4:20:
                    40:71:74:a2:7b:e7:52:a4:4d:48:88:d6:51:4c:92:
                    a7:f8:b2:e3:5c:dd:fb:3a:18:3a:4d:7c:a0:c7:a7:
                    17:2b:37:be:26:0b:58:ee:88:0a:40:b5:db:8c:28:
                    b4:ea:64:58:02:19:c0:ee:40:97:85:ad:e5:5e:45:
                    41:44:03:cf:3c:91:67:8a:80:d5:c3:bc:07:9b:9c:
                    ae:18:95:47:7a:5e:53:b7:d7:9d:4c:f0:90:60:c2:
                    89:eb:2f:f6:82:5e:e8:f3:79:10:11:e7:d4:16:6e:
                    d6:42:7d:f9:f6:9c:49:86:2a:db:10:5b:d7:e0:8c:
                    fc:dd:f1:fd:5d:97:16:21:bb:5c:1d:2f:8f:d1:c9:
                    2a:11:fb
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha256WithRSAEncryption
         dc:1e:3a:57:be:f5:e3:94:55:8d:3b:11:33:e4:34:aa:e4:75:
         f7:40:e9:98:5a:bb:66:9e:72:22:92:69:32:29:96:fe:60:a8:
         8b:65:36:5a:32:db:ca:ac:98:27:4d:61:5e:2e:d0:a6:14:cb:
         4f:fd:5d:1d:f4:4f:00:0a:2d:b9:4c:af:56:0a:7f:0a:08:9d:
         c6:42:74:01:9c:d6:bf:d2:a7:15:52:ad:cb:18:cd:66:a4:4c:
         9a:54:c1:da:76:8d:29:18:33:b7:02:26:8a:dd:b7:aa:ef:06:
         bc:75:02:4d:7b:9d:b5:aa:f8:11:18:1f:ba:74:ff:d7:d8:c2:
         6e:38:5f:4b:18:50:4d:13:9b:fe:da:52:14:54:8b:c8:c5:15:
         55:2e:33:e0:ed:4d:ba:18:fa:a3:d5:74:b2:77:be:74:4e:26:
         a5:2a:69:b0:cc:44:2d:88:5b:d1:d4:3d:81:bd:c5:34:b6:6c:
         98:3c:06:65:c1:b0:ec:42:b5:c7:85:b6:67:4e:87:b3:99:06:
         34:eb:af:73:63:46:03:f4:70:2a:98:02:e8:7f:ed:a7:ae:61:
         0e:f0:be:d3:c4:05:21:21:42:4f:f4:45:ed:f4:34:5c:03:d5:
         11:9a:15:52:f9:ed:49:eb:0b:30:1d:36:bb:88:82:71:3a:d7:
         97:28:30:89:06:97:67:f1:8d:34:8c:19:46:02:fd:71:2c:d5:
         53:8b:93:9f:04:d7:44:e0:a8:21:85:26:83:bc:71:05:ad:74:
         35:26:f3:9b:4a:22:af:7d:d8:ad:74:ef:6b:f3:3b:c4:b4:a4:
         bd:fa:ad:c9:8a:d5:fd:e6:87:bc:65:3b:4d:00:7f:e2:e1:1e:
         13:e5:98:2a:93:7b:bb:84:f2:42:8f:72:8f:57:ec:ef:3e:e8:
         ec:a7:ca:fe:83:58:a0:58:ac:a8:47:66:2a:89:d1:f4:4c:83:
         ad:28:23:68:4f:ff:8a:bd:a8:a6:4d:97:83:20:39:54:c3:66:
         1f:41:45:50:65:a6:c1:53:88:ac:0c:f4:70:c5:76:e5:45:7b:
         26:c9:0e:66:5f:f0:65:b1:0b:20:4a:a9:11:8d:b9:3d:1c:df:
         83:ab:25:e6:2a:9e:27:31:14:3e:dc:7e:0c:f0:9b:cc:d3:38:
         fb:93:91:d1:3a:02:d3:69:95:7e:cd:7c:14:24:8d:df:a5:28:
         21:22:c6:e2:10:b5:0e:ae:2b:20:14:a4:ed:2a:e4:a5:1b:f3:
         b7:a1:63:21:91:1a:ff:1e:4b:0c:b8:a9:92:2f:24:72:70:f4:
         2a:72:9c:94:76:8a:27:ef:10:52:8c:ab:e3:ed:e6:bf:b1:e7:
         51:cc:85:25:85:19:b4:bf
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

__Use CA’s private key and cert to sign the server’s CSR__

Create a server's extfile `server-extfile.cnf`, replace the "IP.1" of the server where you have your Telegraf is running. 

```s
cat > server-extfile.cnf <<EOF

authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
IP.1  = 10.121.249.133

EOF
```

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ cat > server-extfile.cnf <<EOF
> 
> authorityKeyIdentifier=keyid,issuer
> basicConstraints=CA:FALSE
> keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
> subjectAltName = @alt_names
> 
> [alt_names]
> IP.1  = 10.121.249.133
> 
> EOF
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

Run the following command to sign the server's CSR by Root CA's private key and certificate. 

```s
openssl x509 -req -in server.csr -days 3650 \
    -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
    -out server.crt -extfile server-extfile.cnf
```

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl x509 -req -in server.csr -days 3650 \
>     -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
>     -out server.crt -extfile server-extfile.cnf
Signature ok
subject=C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
Getting CA Private Key
(main) expert@expert-cws:~/cisco-mdt-tig/certs$
```

View the `server.crt` in human readable format 

`openssl x509 -in server.crt -noout -text`

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl x509 -in server.crt -noout -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            62:15:2f:bd:02:5c:8f:f2:a0:68:0d:51:e8:12:5c:ab:03:95:56:6a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com  emailAddress=admin@devnetbro.com
        Validity
            Not Before: Oct  5 00:32:04 2022 GMT
            Not After : Oct  2 00:32:04 2032 GMT
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:ef:d6:0e:5f:1c:29:37:29:72:39:6d:5a:21:3d:
                    4a:73:de:a6:2b:8f:24:3a:fd:c7:ea:5e:dd:1d:ee:
                    4e:f5:1e:df:45:6a:fc:7b:6d:f1:97:c2:40:eb:1e:
                    1a:b5:88:f0:ee:4e:f8:56:f5:77:24:09:6f:10:51:
                    34:d0:5d:38:b6:f3:d8:2d:64:93:23:5c:57:e8:cd:
                    f3:5e:bc:db:c0:c5:5d:a0:4f:83:a2:4a:93:fb:63:
                    c5:53:d5:e6:94:bf:8c:16:cd:e8:1b:88:61:91:2d:
                    25:49:8b:66:bb:a1:9b:e3:09:d0:4d:6b:bf:32:b2:
                    42:55:72:21:45:80:7a:e5:27:1d:42:df:c1:0d:ae:
                    11:2a:c9:c9:95:42:7d:27:1e:5d:85:a6:dc:2d:ce:
                    0c:14:16:8b:8b:e3:f5:28:86:39:e9:31:b9:59:53:
                    eb:70:fb:94:91:c3:74:d8:9b:dd:73:78:e4:78:26:
                    30:dd:5c:42:d7:95:c9:25:89:04:17:3d:e4:c7:a9:
                    8a:79:1f:c5:20:bb:1e:a6:ec:30:c3:40:04:70:9d:
                    7f:7c:00:d2:09:ec:74:0a:0d:eb:8b:08:be:97:5e:
                    57:ce:88:bd:e9:10:44:71:8f:e4:d7:61:eb:67:4a:
                    39:9b:56:0b:1a:2d:da:de:5d:b5:e3:71:27:27:f4:
                    1e:25:3e:b5:14:15:b4:c1:37:e8:ec:48:34:46:95:
                    b9:49:e5:5c:4b:1e:d0:84:f1:0b:3a:39:f7:fd:42:
                    6c:37:02:45:7f:b1:98:83:50:e5:4d:4e:86:fa:c8:
                    ec:11:8d:9e:05:0f:6b:35:6a:7e:66:4a:8b:79:45:
                    0a:e0:2f:bd:b1:f2:0e:7c:7e:77:62:a2:56:4d:ff:
                    90:7c:8f:6d:ff:86:c7:22:89:e2:b0:64:1c:e1:74:
                    5c:9d:2f:1c:b2:8f:d7:bc:72:70:79:db:5a:0c:79:
                    a8:8a:63:28:4c:7d:38:c8:a1:69:c4:43:4b:f4:20:
                    40:71:74:a2:7b:e7:52:a4:4d:48:88:d6:51:4c:92:
                    a7:f8:b2:e3:5c:dd:fb:3a:18:3a:4d:7c:a0:c7:a7:
                    17:2b:37:be:26:0b:58:ee:88:0a:40:b5:db:8c:28:
                    b4:ea:64:58:02:19:c0:ee:40:97:85:ad:e5:5e:45:
                    41:44:03:cf:3c:91:67:8a:80:d5:c3:bc:07:9b:9c:
                    ae:18:95:47:7a:5e:53:b7:d7:9d:4c:f0:90:60:c2:
                    89:eb:2f:f6:82:5e:e8:f3:79:10:11:e7:d4:16:6e:
                    d6:42:7d:f9:f6:9c:49:86:2a:db:10:5b:d7:e0:8c:
                    fc:dd:f1:fd:5d:97:16:21:bb:5c:1d:2f:8f:d1:c9:
                    2a:11:fb
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Authority Key Identifier: 
                keyid:DF:79:00:48:DA:E6:31:2A:1D:F3:2A:55:ED:13:6C:47:02:2A:87:18

            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Key Usage: 
                Digital Signature, Non Repudiation, Key Encipherment, Data Encipherment
            X509v3 Subject Alternative Name: 
                IP Address:10.121.249.133
    Signature Algorithm: sha256WithRSAEncryption
         6b:8d:48:62:60:a4:09:ff:83:20:be:25:cd:46:0c:b8:d8:67:
         cc:3e:5d:9c:c2:0f:8d:27:99:19:ce:53:6f:32:aa:8a:bc:f5:
         6a:5f:f7:2f:23:b3:03:8b:d7:19:85:f6:c1:b2:75:92:1e:83:
         ba:50:ab:d4:4b:61:36:24:76:25:0e:9b:83:f7:99:24:ca:8b:
         c0:91:24:9f:27:35:a5:04:7e:ed:37:79:3f:02:df:c2:57:ee:
         2f:6f:eb:19:75:7b:ea:bc:05:83:88:84:c2:29:ae:31:b2:7a:
         84:bd:09:f0:f9:e1:29:e2:e2:b7:f6:14:ac:5c:16:17:47:85:
         64:17:95:d1:c5:bf:44:16:0c:5f:0f:b9:5e:4d:25:07:16:9d:
         24:17:cf:ac:b4:e2:d3:aa:f6:e2:83:86:27:3c:5a:25:f6:65:
         f9:a9:dd:df:2b:e8:ad:8f:df:8d:4b:f5:bb:a0:8d:f5:be:9d:
         c2:c5:ac:ab:ab:8e:a1:8a:75:21:aa:d4:62:14:80:e2:11:3e:
         de:3c:7a:87:c9:28:d4:c3:10:5f:3e:80:15:54:37:55:28:bf:
         52:81:5b:9e:0d:21:40:e6:95:c1:66:78:03:61:be:84:f0:cf:
         31:9f:b7:b7:42:c2:63:cc:14:4c:19:a2:aa:cc:6c:3d:78:ea:
         30:75:26:ad:23:9a:55:35:83:ac:57:6b:8b:3d:b1:37:fe:81:
         f7:1c:e4:6e:95:5b:1f:06:96:71:2c:ec:af:42:c6:48:6e:c0:
         af:5d:c7:df:c3:7c:ae:d6:81:e5:00:39:4b:12:43:f6:6b:e2:
         ee:eb:90:76:a4:21:29:e2:5e:1e:44:11:c3:ca:d8:81:4f:ce:
         9c:b0:e5:28:27:b1:0d:44:88:5d:ff:00:ab:a0:a7:3f:a0:d8:
         56:5a:f4:84:f8:12:c1:9d:4a:55:4b:0d:83:fb:c5:55:6b:d9:
         36:bb:95:9b:81:38:47:ba:aa:f1:46:9b:cf:43:a4:e7:06:3f:
         ed:c9:1c:c6:a8:2d:09:38:83:9d:e6:ce:b2:02:3b:85:8b:6e:
         23:d5:f4:0e:a0:0c:ab:86:0a:ce:28:fc:35:cf:27:fb:31:f5:
         c4:43:49:2e:9c:3e:27:f5:4b:f6:c3:31:80:2a:e5:a7:d8:56:
         e3:07:b2:f7:ec:6b:61:84:ec:bd:b7:7c:75:a1:e7:cc:9f:bf:
         67:ae:87:54:6a:1d:a3:93:b2:80:52:ce:0f:27:de:55:17:8f:
         30:ed:d2:87:e4:99:f7:81:f2:5a:1b:b8:db:94:c8:a1:db:66:
         1f:b2:95:c6:04:76:90:08:90:6a:f5:a5:fa:aa:c4:8a:69:fe:
         c7:97:cd:2c:a4:b5:77:1d
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

There you go, you now have server's self-signed certificate generated. You can verify this `server.crt` with the root CA `ca-cert.pem` cert file"

```s
openssl verify -CAfile ca-cert.pem -verbose server.crt
```

__Output__

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ openssl verify -CAfile ca-cert.pem -verbose server.crt
server.crt: OK
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

Finally, you can check what certificates and key you have created in the directory. 

```bash
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ ls -l
total 32
-rw-rw-r-- 1 expert expert 2143 Oct  4 22:36 ca-cert.pem
-rw-rw-r-- 1 expert expert   41 Oct  5 00:32 ca-cert.srl
-rw------- 1 expert expert 3272 Oct  4 22:36 ca-key.pem
-rw-rw-r-- 1 expert expert 2118 Oct  4 23:17 server.crt
-rw-rw-r-- 1 expert expert 1740 Oct  4 22:52 server.csr
-rw-rw-r-- 1 expert expert  207 Oct  4 23:13 server-extfile.cnf
-rw------- 1 expert expert 3272 Oct  4 22:52 server.key
(main) expert@expert-cws:~/cisco-mdt-tig/certs$ 
```

The most interesting files are `ca-cert.pem`, `server.key` and `server.crt`.