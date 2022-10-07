## gRPC dial-out with SSL/TLS on Cisco IOSXE 

### Create own CA (Certificate Authority) and self-signed certificate via Bash Script

We need to follow these steps to generate self-signed certifcate to secure the gRPC connection. you can refer to this [self-signed-cert-gen.md](self-signed-cert-gen.md) if you like to do it manually, however I have created a bash script [ssl_certs.sh](certs/ssl_certs.sh) which can run all these steps. 

- Generate CA’s private key and its self-signed certificate.
- Generate server's private key and certificate signing request (CSR).
- Use CA’s private key and cert to sign the server’s CSR to generate server's self-signed certificate.

Clone the repository in your Linux box, where you want to run the dockerized TIG stack and make sure you have docker-compose installed. 

`git clone https://github.com/muhammad-rafi/cisco-mdt-tig.git`

Go to the `cisco-mdt-tig` directory and run the docker-compose to pull and run the docker TIG stack.

__Output__

```bash
ubuntu@devnet-box:~$ cd cisco-mdt-tig/
ubuntu@devnet-box:~/cisco-mdt-tig$ 
ubuntu@devnet-box:~/cisco-mdt-tig$ docker compose up -d
[+] Running 3/3
 ⠿ Container influxdb  Started                                                                                                  0.3s
 ⠿ Container grafana   Started                                                                                                  1.2s
 ⠿ Container telegraf  Started                                                                                                  1.3s
ubuntu@devnet-box:~/cisco-mdt-tig$
```

```bash
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker compose ps -a
NAME                COMMAND                  SERVICE             STATUS              PORTS
grafana             "/run.sh"                grafana             running             0.0.0.0:3000->3000/tcp, :::3000->3000/tcp
influxdb            "/entrypoint.sh infl…"   influxdb            running             0.0.0.0:8086->8086/tcp, :::8086->8086/tcp
telegraf            "/entrypoint.sh tele…"   telegraf            running             0.0.0.0:57000->57000/tcp, :::57000->57000/tcp
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

I have created a bash script `ssl_certs.sh` under the `certs` directory, that can generate the required keys and certs. I am going to run this script where my TIG stack is running with docker compose. 

__Note:__ in the bash script, you need to enter correct IP address of the telegraf server. You may also change cert details in the `-subj` as per you need.

```s
[alt_names]
IP.1  = <telegraf-server-ip>
```

Now, go to the `certs` directory and run the script, currently it should not have any keys and certs. 

__Output__

```bash
ubuntu@devnet-box:~/cisco-mdt-tig$ cd certs/
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ bash ssl_certs.sh 
Generating a RSA private key
....................................................................++++
........................++++
writing new private key to 'ca-key.pem'
-----
printing the 'ca-cert.pem' in human readable format
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            66:ee:62:12:c0:46:3a:f0:20:3c:88:1e:df:f4:dc:65:23:b1:79:5e
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com emailAddress=admin@devnetbro.com
        Validity
            Not Before: Oct  5 02:52:47 2022 GMT
            Not After : Oct  2 02:52:47 2032 GMT
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:ad:db:30:05:83:c9:42:26:a0:5f:ee:ae:e2:68:
                    0b:52:8a:18:5c:74:4d:0d:2a:32:04:7d:bf:2a:76:
                    c6:8e:f8:f3:f9:2a:f4:84:54:1d:ad:d9:8a:ac:e8:
                    b2:58:26:d6:06:63:34:05:35:cf:ef:e1:9c:da:0f:
                    6d:59:77:79:73:c6:d3:21:89:4f:fd:ea:b4:09:b3:
                    e5:b6:c6:61:f7:b7:55:e9:9c:7b:b4:19:68:ee:12:
                    38:65:bd:49:81:b5:36:45:ea:a3:ee:f9:88:94:51:
                    13:8d:b1:70:51:8a:a9:21:4b:30:4d:8f:dd:f6:1e:
                    35:3a:ec:76:ed:78:15:15:df:47:f9:10:b9:97:d1:
                    d9:bc:db:99:bb:5a:d3:fa:4e:1a:27:f2:da:dd:5e:
                    1c:ac:5c:53:e4:d3:da:a5:f4:18:f9:2e:ba:4e:8b:
                    f4:76:44:0e:a2:3b:a4:71:ac:64:62:db:a2:31:ee:
                    59:e0:04:2e:a3:3e:8e:41:8b:d9:28:fe:5e:d5:c3:
                    7f:99:c3:a7:eb:ea:44:43:5d:8b:bb:3a:9b:87:f9:
                    73:54:6d:8a:a9:fd:5c:d2:cf:76:45:2d:56:5c:06:
                    c6:dc:41:53:50:7d:23:60:22:3c:15:61:75:04:b6:
                    a1:a7:e5:0f:37:e7:b9:1f:70:7a:f8:cf:2d:03:6a:
                    41:c9:9d:78:82:7b:41:50:41:b8:ab:f5:52:d4:c0:
                    ae:25:79:9e:0a:92:70:72:a1:fe:58:d9:ed:84:19:
                    66:b4:8a:f6:c0:b6:09:9b:cd:dc:99:79:58:30:55:
                    a5:24:8b:41:83:c6:ae:5f:84:90:20:da:38:ef:a4:
                    39:63:ad:2c:c2:6d:b5:0f:d3:6a:43:46:5e:4d:03:
                    01:8e:de:42:6f:d3:13:97:b0:d6:15:8d:0f:6d:77:
                    05:c9:55:82:51:83:cd:8a:5d:70:f2:91:4b:b8:a9:
                    07:16:6f:0c:89:d8:c6:28:e4:ea:ed:d7:c9:1b:33:
                    1b:48:e9:27:3e:7f:7c:29:95:37:53:61:8c:41:41:
                    80:d2:02:18:96:91:2d:83:e8:ff:8c:a5:47:65:c8:
                    50:09:3c:cd:ea:5c:af:ba:dc:9f:c8:d7:45:2f:74:
                    4b:87:d4:96:ff:15:79:3b:81:4d:1a:85:89:43:89:
                    f5:43:03:15:b8:7a:00:25:af:dd:3d:e9:72:29:c3:
                    fc:f5:6d:6f:5a:06:eb:21:b0:a5:7a:bd:f8:e6:67:
                    d8:10:43:b0:43:4e:e8:cf:dd:ba:ba:66:ba:86:d6:
                    6a:e3:98:78:5d:f4:f0:c1:e9:56:c0:18:cf:26:96:
                    51:67:e0:c2:38:5b:fb:48:4e:10:6f:0b:df:04:2c:
                    60:c1:2f
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                61:A0:EA:C6:F1:F2:D0:08:69:DF:67:A0:74:DA:69:40:83:20:77:58
            X509v3 Authority Key Identifier: 
                keyid:61:A0:EA:C6:F1:F2:D0:08:69:DF:67:A0:74:DA:69:40:83:20:77:58

            X509v3 Basic Constraints: critical
                CA:TRUE
    Signature Algorithm: sha256WithRSAEncryption
         a8:6b:60:54:2e:7b:d2:44:ff:68:bb:79:8f:c3:38:9b:c1:74:
         a5:52:6e:20:99:fc:d5:32:32:a5:f9:de:c2:e2:3f:f6:b6:fe:
         82:98:87:78:46:ec:12:84:d0:2e:bb:16:34:8f:25:d9:3c:f5:
         6b:17:2d:df:af:9c:b8:95:60:f7:2c:1c:99:f3:7e:3a:42:37:
         48:76:be:e7:64:fa:e9:d7:48:28:6a:2f:ac:ab:2b:40:f1:44:
         d2:98:7e:92:1f:26:2b:2a:83:96:50:0d:8b:55:25:6f:1a:1e:
         03:c5:65:73:bf:47:63:5c:b2:7f:29:c4:73:05:5c:f9:d3:45:
         55:8b:f7:ec:dc:cb:22:6d:71:74:04:47:08:81:0d:a5:6e:fb:
         92:f5:56:47:6a:93:6e:2f:4a:47:f1:b1:cc:d3:57:57:d0:50:
         cb:ed:60:73:7b:26:5e:38:c6:bc:d6:f6:07:56:2c:68:23:a1:
         f2:64:0e:7a:7f:4f:86:f7:5d:37:1a:b7:fd:57:fa:50:c8:61:
         54:22:8d:8d:5e:b4:c5:82:a1:8d:ec:3c:45:30:27:65:5c:2e:
         92:51:0b:2c:38:2c:bb:23:b3:be:60:e2:03:88:2c:c3:e6:59:
         2a:4a:be:15:42:4e:5f:71:8d:e1:26:e9:36:77:b8:ef:b0:89:
         c7:24:c6:45:7f:fb:3a:0e:2a:95:dd:ff:55:f5:92:4a:f6:ec:
         82:4c:6e:b5:b2:40:5a:8a:69:a3:7a:50:a7:6a:e6:52:d6:9d:
         3a:e8:70:44:89:92:bf:e6:a3:6f:4e:6e:9e:9f:86:e4:5c:ff:
         7f:98:60:d2:67:68:0d:d7:75:4f:ca:b6:e5:68:f7:f0:58:94:
         6d:ab:59:da:8c:88:3b:cb:0e:76:ba:5c:22:3b:22:73:80:43:
         89:d6:6b:7e:4e:23:22:a4:a5:33:12:e4:5c:81:f2:86:86:57:
         80:ff:e8:1f:a4:92:7b:54:0a:9e:d7:98:1f:c9:21:93:73:65:
         20:c2:a4:2b:69:e5:0d:31:57:1a:71:4f:b3:4a:6d:05:25:d4:
         d7:49:e6:eb:4a:8f:37:bb:1d:85:e6:9c:ad:a4:fa:8e:f3:bd:
         0c:00:0a:9c:c7:35:c7:42:9d:fd:53:c5:32:12:5a:5e:e1:68:
         e7:d5:28:68:fa:80:2a:df:23:6c:f2:40:64:2f:7c:c4:c4:e8:
         9b:15:74:eb:aa:37:a3:01:08:be:6c:74:66:5a:1d:45:5d:2f:
         e7:d5:9a:52:b1:69:bd:eb:0c:eb:62:17:c8:6f:0e:dd:e2:ae:
         1e:9e:9d:4d:0b:b9:7f:3a:69:97:19:f5:b9:5a:aa:8c:2a:fb:
         ab:de:e8:6b:aa:c8:50:55
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generating a RSA private key
.............................................................................................................................................................................................................++++
..............................++++
writing new private key to 'server.key'
-----
printing the 'server.csr' in human readable format
Certificate Request:
    Data:
        Version: 1 (0x0)
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:d1:a4:27:4a:f2:f5:7f:74:ce:25:5b:f3:e5:13:
                    d0:3b:51:d0:1d:db:1c:33:a7:d8:64:1f:91:e3:20:
                    05:3c:47:e6:da:3b:9f:98:84:5e:08:cd:51:75:97:
                    c0:fa:26:49:b9:62:ac:d1:6f:36:19:1e:2c:8d:77:
                    79:3f:14:2a:91:88:36:fd:18:99:d5:21:be:9b:e1:
                    29:98:62:a6:28:7d:5a:31:77:ed:ec:b5:68:68:4e:
                    4a:d8:ce:df:49:a4:a9:61:a7:d5:6c:08:43:d7:3f:
                    90:99:9e:d9:5b:00:63:40:0d:b3:d1:cf:55:2a:07:
                    84:7d:87:05:5d:f6:cd:9b:90:33:56:b0:df:be:89:
                    d0:30:c3:8f:85:9d:81:b7:55:c3:2c:34:e3:45:3c:
                    a9:6d:e1:e4:32:ad:eb:2a:e6:b9:e6:6e:aa:42:24:
                    ca:81:3c:5e:02:41:9b:23:43:e7:e5:4c:88:97:cd:
                    20:fd:63:a3:ca:b0:0c:89:17:0c:e5:97:ae:77:e3:
                    d6:2a:30:b4:af:37:23:22:89:1c:8f:5e:0e:fa:97:
                    d4:19:3a:81:9d:93:9c:75:ca:27:f2:50:dd:50:70:
                    79:67:cd:bb:c6:f3:ed:9b:e3:44:e4:55:67:57:95:
                    ea:0e:08:88:51:c4:66:41:08:51:8f:6b:4a:bb:a6:
                    98:14:4d:3c:d1:c6:47:56:33:b6:89:d7:cc:f8:30:
                    42:f8:a3:08:3d:f2:7a:28:d4:12:d4:0f:89:10:9e:
                    cf:ed:a5:71:d0:51:c0:dc:7b:42:c4:f5:b1:c0:32:
                    ef:bc:1f:d2:91:7a:e1:6d:72:62:06:16:df:4a:64:
                    6d:4e:23:ea:be:03:32:f2:0f:78:e5:1e:28:04:5b:
                    ce:b4:a5:2d:46:ed:60:32:07:fc:d4:78:44:54:1e:
                    70:70:e6:9c:8f:18:53:d9:74:e5:5f:ae:60:a1:5c:
                    c5:e1:1b:a9:e2:5c:de:13:ad:fc:e9:f2:c7:f8:99:
                    7b:17:af:02:35:ea:26:35:1b:6b:3d:2f:fa:9f:1f:
                    49:c4:dc:9b:39:50:d5:99:60:b3:be:e3:ee:a9:56:
                    0d:c1:7a:b7:df:ff:01:da:22:59:43:83:1b:57:23:
                    cd:06:9a:1b:d9:ee:c4:dc:54:7e:af:80:e9:a6:2f:
                    3a:4a:a1:a7:91:bf:49:79:74:34:c0:fb:cb:7f:1a:
                    c3:6b:fd:3c:e3:6e:69:e6:91:47:69:7e:b5:79:9d:
                    50:80:db:2a:e0:70:5f:01:e5:14:b1:a5:fb:27:04:
                    9a:a9:a8:5f:7e:6d:fe:8a:a0:1f:bf:94:e8:9a:84:
                    5d:33:41:da:09:dc:ce:83:fe:be:69:72:63:eb:ac:
                    e7:88:33
                Exponent: 65537 (0x10001)
        Attributes:
            a0:00
    Signature Algorithm: sha256WithRSAEncryption
         8c:e1:e4:1e:41:cc:f9:a0:cb:a6:48:60:22:b8:4a:d8:26:ab:
         b7:1d:eb:d7:d4:e0:18:d3:35:03:2b:8d:7e:b8:5e:64:6d:25:
         71:62:1a:7b:1b:1c:3c:c8:a1:f4:25:31:8a:5f:4f:c9:61:e8:
         46:ce:9a:9b:a8:38:5f:58:1b:53:15:a2:ca:a0:dc:e1:da:fb:
         c1:5a:d2:d6:88:23:23:f8:a5:90:ac:35:26:bd:4f:a4:0a:e9:
         36:8a:97:11:d3:14:c1:67:77:21:a8:2e:e8:4c:c6:26:70:80:
         1a:dc:b3:f8:de:68:fe:4b:0b:8e:f5:d3:cf:4f:4b:50:24:49:
         17:fe:d6:bb:bb:93:0f:5a:52:7d:46:c3:99:d3:22:1a:9f:90:
         14:9a:f3:4d:81:5f:c3:0a:34:e2:36:ac:60:ec:1f:34:4a:72:
         cf:5f:a7:6f:d6:54:47:4b:23:f2:30:91:75:0c:0d:48:d0:55:
         a6:cd:c2:6b:9c:50:f5:b6:68:6a:4a:ff:8d:3f:53:74:fb:1c:
         29:38:84:33:df:5e:1d:58:15:2a:4d:69:a0:6c:69:0f:54:f5:
         6f:68:08:53:c3:59:92:dc:c8:dd:25:d0:b7:0e:3d:56:22:6b:
         4a:70:63:61:0c:ed:c2:96:b1:d3:80:c8:53:5e:30:79:44:dd:
         ff:25:a8:02:ff:23:9f:56:b4:cf:f4:9e:30:a0:31:21:90:2d:
         37:31:73:66:c0:66:01:18:f3:14:25:c4:ae:c1:11:ba:ea:33:
         bd:36:7b:b3:44:9c:00:20:8d:7d:e2:cb:68:86:8e:5b:0b:d4:
         53:77:cd:0f:6d:89:35:b9:f4:53:69:5a:a6:c9:b5:25:69:30:
         50:e0:76:95:57:55:5a:77:ac:63:1b:97:b7:a1:0e:33:20:23:
         d0:2d:97:63:15:36:73:1c:1f:b7:54:63:bc:12:7f:ba:55:56:
         b3:58:e5:75:b1:88:db:ae:ff:65:74:af:28:ed:cc:bd:f8:52:
         36:02:55:c1:b2:49:70:04:f8:4c:18:92:6f:09:30:2d:a2:9d:
         2d:e7:be:3b:11:4d:2b:05:d8:1d:df:e8:7d:15:c2:20:8a:e4:
         6d:dd:42:d1:a2:8f:73:9d:e1:5a:78:15:38:b5:ac:62:75:f5:
         6b:f1:b0:60:9d:d5:9e:41:a1:56:36:0f:3e:88:d9:14:4e:99:
         34:49:3b:0b:e2:53:ee:08:41:0f:56:11:5e:b4:b2:06:08:a3:
         3f:82:d4:e7:04:8d:f4:40:fb:c1:09:14:c0:bf:15:e0:6e:2d:
         c2:c8:65:8a:17:f9:57:52:68:06:2f:5c:92:a3:0a:70:3c:f9:
         21:2e:ab:90:03:0d:bc:30
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creating server's extfile 'server-extfile.cnf'
Signature ok
subject=C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
Getting CA Private Key
printing the 'server.crt' in human readable format
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            39:c5:ee:35:89:ff:0c:7a:7f:b3:b6:99:1e:f2:d6:48:fc:47:63:16
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = devnetbro.com emailAddress=admin@devnetbro.com
        Validity
            Not Before: Oct  5 02:52:54 2022 GMT
            Not After : Oct  2 02:52:54 2032 GMT
        Subject: C = GB, ST = England, L = London, O = DevnetBro, OU = NetOps, CN = grpc emailAddress=admin@devnetbro.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (4096 bit)
                Modulus:
                    00:d1:a4:27:4a:f2:f5:7f:74:ce:25:5b:f3:e5:13:
                    d0:3b:51:d0:1d:db:1c:33:a7:d8:64:1f:91:e3:20:
                    05:3c:47:e6:da:3b:9f:98:84:5e:08:cd:51:75:97:
                    c0:fa:26:49:b9:62:ac:d1:6f:36:19:1e:2c:8d:77:
                    79:3f:14:2a:91:88:36:fd:18:99:d5:21:be:9b:e1:
                    29:98:62:a6:28:7d:5a:31:77:ed:ec:b5:68:68:4e:
                    4a:d8:ce:df:49:a4:a9:61:a7:d5:6c:08:43:d7:3f:
                    90:99:9e:d9:5b:00:63:40:0d:b3:d1:cf:55:2a:07:
                    84:7d:87:05:5d:f6:cd:9b:90:33:56:b0:df:be:89:
                    d0:30:c3:8f:85:9d:81:b7:55:c3:2c:34:e3:45:3c:
                    a9:6d:e1:e4:32:ad:eb:2a:e6:b9:e6:6e:aa:42:24:
                    ca:81:3c:5e:02:41:9b:23:43:e7:e5:4c:88:97:cd:
                    20:fd:63:a3:ca:b0:0c:89:17:0c:e5:97:ae:77:e3:
                    d6:2a:30:b4:af:37:23:22:89:1c:8f:5e:0e:fa:97:
                    d4:19:3a:81:9d:93:9c:75:ca:27:f2:50:dd:50:70:
                    79:67:cd:bb:c6:f3:ed:9b:e3:44:e4:55:67:57:95:
                    ea:0e:08:88:51:c4:66:41:08:51:8f:6b:4a:bb:a6:
                    98:14:4d:3c:d1:c6:47:56:33:b6:89:d7:cc:f8:30:
                    42:f8:a3:08:3d:f2:7a:28:d4:12:d4:0f:89:10:9e:
                    cf:ed:a5:71:d0:51:c0:dc:7b:42:c4:f5:b1:c0:32:
                    ef:bc:1f:d2:91:7a:e1:6d:72:62:06:16:df:4a:64:
                    6d:4e:23:ea:be:03:32:f2:0f:78:e5:1e:28:04:5b:
                    ce:b4:a5:2d:46:ed:60:32:07:fc:d4:78:44:54:1e:
                    70:70:e6:9c:8f:18:53:d9:74:e5:5f:ae:60:a1:5c:
                    c5:e1:1b:a9:e2:5c:de:13:ad:fc:e9:f2:c7:f8:99:
                    7b:17:af:02:35:ea:26:35:1b:6b:3d:2f:fa:9f:1f:
                    49:c4:dc:9b:39:50:d5:99:60:b3:be:e3:ee:a9:56:
                    0d:c1:7a:b7:df:ff:01:da:22:59:43:83:1b:57:23:
                    cd:06:9a:1b:d9:ee:c4:dc:54:7e:af:80:e9:a6:2f:
                    3a:4a:a1:a7:91:bf:49:79:74:34:c0:fb:cb:7f:1a:
                    c3:6b:fd:3c:e3:6e:69:e6:91:47:69:7e:b5:79:9d:
                    50:80:db:2a:e0:70:5f:01:e5:14:b1:a5:fb:27:04:
                    9a:a9:a8:5f:7e:6d:fe:8a:a0:1f:bf:94:e8:9a:84:
                    5d:33:41:da:09:dc:ce:83:fe:be:69:72:63:eb:ac:
                    e7:88:33
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Authority Key Identifier: 
                keyid:61:A0:EA:C6:F1:F2:D0:08:69:DF:67:A0:74:DA:69:40:83:20:77:58

            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Key Usage: 
                Digital Signature, Non Repudiation, Key Encipherment, Data Encipherment
            X509v3 Subject Alternative Name: 
                IP Address:10.121.249.133
    Signature Algorithm: sha256WithRSAEncryption
         7b:08:d2:c9:e9:5f:03:7b:5b:6e:8b:35:5e:79:e9:6d:15:13:
         6a:0e:25:b7:5c:29:73:bd:bb:9b:41:de:8d:83:93:b3:4c:64:
         ff:5b:82:20:6c:a5:71:42:db:c9:50:8c:1d:8f:b7:9e:f3:fc:
         2d:e5:f6:3e:cc:7b:14:f1:05:9b:1c:9d:a2:82:6f:05:91:80:
         2c:52:5b:33:26:d1:6e:67:c1:1b:b8:3e:d1:6e:1d:64:c6:a9:
         5b:98:5f:a5:8b:ad:3f:a3:bf:a7:60:c8:e1:7d:e4:ab:82:78:
         2e:c9:c7:66:6f:ec:42:aa:43:9e:e8:ff:ba:25:79:96:7d:86:
         5e:25:b9:d4:be:7c:bc:3d:3e:18:a6:45:bd:93:ab:ca:48:54:
         38:8a:2b:a2:58:7a:da:8e:3e:66:93:f9:a1:84:dc:d8:b5:e4:
         93:87:34:2b:3c:9e:73:9b:b8:34:57:0b:c6:14:d6:e8:34:bd:
         13:c9:23:de:e7:0f:7b:a8:6e:78:d0:f2:4e:18:16:fc:c8:a4:
         1f:70:06:6d:47:67:1c:76:4c:0a:18:f2:0f:49:2e:ce:f5:1e:
         1d:78:16:26:d5:8a:a8:a8:23:a2:2b:46:ef:d0:d0:80:2f:87:
         25:b4:e6:1e:3c:a8:80:b6:23:3f:fb:53:e4:5e:79:8d:a9:d7:
         af:06:f5:df:ac:2b:c0:f1:09:ad:d6:11:b1:9e:4e:4a:5f:40:
         de:52:01:46:66:80:13:45:ba:a0:aa:c4:e6:38:3a:b7:5e:90:
         e4:61:65:e1:57:f7:fa:b1:5c:07:d6:6f:09:8e:62:9e:e5:a5:
         af:b4:4d:4d:f3:20:ae:24:80:c2:06:12:e9:55:b0:d6:1d:25:
         5a:80:c4:db:98:2b:eb:71:98:11:0f:7c:57:a7:b1:5f:a6:98:
         0b:53:0b:15:d6:4e:86:19:03:41:db:75:bd:c9:6b:fa:db:a1:
         aa:f7:4f:a5:fa:67:6c:11:a4:19:cf:9b:02:8c:66:36:51:5a:
         8e:30:6c:ef:70:63:f4:0c:5f:0c:ac:0b:30:17:e3:18:1f:82:
         0d:20:73:e1:ad:d8:89:1b:e6:83:29:b7:d6:6e:3c:a6:e1:bb:
         04:a8:e3:61:ed:9c:2a:c6:10:91:78:ae:77:1d:34:d1:19:57:
         d8:fc:34:4e:21:dd:44:b6:55:26:a6:1b:99:6f:98:ff:04:17:
         0f:05:a6:4a:3b:ed:a9:0c:22:53:33:96:c8:95:48:27:3b:c5:
         8f:34:fa:1f:ef:27:e2:34:32:ab:81:52:82:da:f5:56:3c:3e:
         58:09:bd:9d:46:7f:34:f3:22:21:9b:68:bc:1f:ce:36:8f:4d:
         5e:19:4b:da:c4:0a:24:68
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Verifying 'server.crt' with the root CA
server.crt: OK
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

You can see these new certs and keys are created in this directory

```bash
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ ls -l
total 32
-rw-r----- 1 ubuntu ubuntu 2139 Oct  5 02:52 ca-cert.pem
-rw-r----- 1 ubuntu ubuntu   41 Oct  5 02:52 ca-cert.srl
-rw------- 1 ubuntu ubuntu 3272 Oct  5 02:52 ca-key.pem
-rw-r----- 1 ubuntu ubuntu  207 Oct  5 02:52 server-extfile.cnf
-rw-r----- 1 ubuntu ubuntu 2118 Oct  5 02:52 server.crt
-rw-r----- 1 ubuntu ubuntu 1740 Oct  5 02:52 server.csr
-rw------- 1 ubuntu ubuntu 3272 Oct  5 02:52 server.key
-rw-r----- 1 ubuntu ubuntu 2345 Oct  5 02:52 ssl_certs.sh
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

The most interesting files are `ca-cert.pem`, `server.key` and `server.crt`.

### Copy Server's Key and Self-Signed Certificate to Telegraf

Next step is to copy these `server.key` and `server.crt` to the telegraf container.

Run following commands to copy the server's key and cert file 
```s
docker cp server.key telegraf:/etc/telegraf/server.key
docker cp server.crt telegraf:/etc/telegraf/server.crt
```

Please note, you may require `sudo` to run this `docker cp` command depending upon how you install docker in your system.

__Output__

```bash
ubuntu@devnet-box:~$ cd cisco-mdt-tig/certs/
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker cp server.key telegraf:/etc/telegraf/server.key
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker cp server.crt telegraf:/etc/telegraf/server.crt
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

Once you copied the server's key and cert, then restart the TIG stack via docker compose. 

```bash
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker compose stop
[+] Running 3/3
 ⠿ Container telegraf  Stopped                                                                                                  0.3s
 ⠿ Container grafana   Stopped                                                                                                  0.3s
 ⠿ Container influxdb  Stopped                                                                                                  0.3s
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker compose ps -a
NAME                COMMAND                  SERVICE             STATUS              PORTS
grafana             "/run.sh"                grafana             exited (0)          
influxdb            "/entrypoint.sh infl…"   influxdb            exited (0)          
telegraf            "/entrypoint.sh tele…"   telegraf            exited (0)          
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker compose start
[+] Running 3/3
 ⠿ Container influxdb  Started                                                                                                  0.3s
 ⠿ Container grafana   Started                                                                                                  0.4s
 ⠿ Container telegraf  Started                                                                                                  0.5s
ubuntu@devnet-box:~/cisco-mdt-tig/certs$
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker compose ps -a
NAME                COMMAND                  SERVICE             STATUS              PORTS
grafana             "/run.sh"                grafana             running             0.0.0.0:3000->3000/tcp, :::3000->3000/tcp
influxdb            "/entrypoint.sh infl…"   influxdb            running             0.0.0.0:8086->8086/tcp, :::8086->8086/tcp
telegraf            "/entrypoint.sh tele…"   telegraf            running             0.0.0.0:57000->57000/tcp, :::57000->57000/tcp
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

Verify the files have been copied over. 

```bash
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker exec -it telegraf /bin/bash
root@76b1861886f9:/# ls -l /etc/telegraf/
total 332
-rw-r----- 1 1000 1000   2118 Oct  5 02:52 server.crt
-rw------- 1 1000 1000   3272 Oct  5 02:52 server.key
-rw-r----- 0 1000 1000    796 Oct  5 02:40 telegraf.conf
-rw-r--r-- 1 root root 321550 Jun 17  2021 telegraf.conf.sample
drwxr-xr-x 2 root root   4096 Jun 17  2021 telegraf.d
root@76b1861886f9:/# 
```

Sure enough, files have been copied, next step to edit the telegraf.conf if you do not currently have TLS options enabled. 

### Edit telegraf.conf to enable TLS (optional)

I am running a TIG (Telegraf, InfluxDB and Grafana) in docker, so let's login to the telegraf docker and edit the `telegraf.conf` file. 

```bash
ubuntu@devnet-box:~/cisco-mdt-tig$ docker ps -a
CONTAINER ID   IMAGE                                 COMMAND                  CREATED         STATUS                    PORTS                                                                         NAMES
76b1861886f9   telegraf:1.19.0                       "/entrypoint.sh tele…"   6 minutes ago   Up 6 minutes              8092/udp, 8125/udp, 8094/tcp, 0.0.0.0:57000->57000/tcp, :::57000->57000/tcp   telegraf
d27a6d11b125   grafana/grafana:8.1.0-ubuntu          "/run.sh"                6 minutes ago   Up 6 minutes              0.0.0.0:3000->3000/tcp, :::3000->3000/tcp                                     grafana
ad115e48736f   influxdb:1.8                          "/entrypoint.sh infl…"   6 minutes ago   Up 6 minutes              0.0.0.0:8086->8086/tcp, :::8086->8086/tcp                                     influxdb
212f0018185e   gcr.io/k8s-minikube/kicbase:v0.0.27   "/usr/local/bin/entr…"   2 weeks ago     Exited (130) 9 days ago                                                                                 minikube
ubuntu@devnet-box:~/cisco-mdt-tig$ 
ubuntu@devnet-box:~/cisco-mdt-tig$ docker exec -it telegraf /bin/bash
root@76b1861886f9:/# 
```

Edit the file as below; enable or add these two lines 

```s
  tls_cert = "/etc/telegraf/server.crt"
  tls_key = "/etc/telegraf/server.key"
```

```bash
root@76b1861886f9:/# cat /etc/telegraf/telegraf.conf
# Global Agent Configuration
[agent]
  hostname = "ubuntu-server"
  flush_interval = "15s"
  interval = "15s"

# gRPC Dial-Out Telemetry Listener
[[inputs.cisco_telemetry_mdt]]
  transport = "grpc"
  service_address = ":57000"

  # Optional TLS Config
  # tls_server_name = "myhost.example.org"
  # tls_ca = "/etc/telegraf/ca-cert.pem"
  tls_cert = "/etc/telegraf/server.crt"
  tls_key = "/etc/telegraf/server.key"

  # Use TLS but skip chain & host verification
  # insecure_skip_verify = false

# Output Plugin InfluxDB for gRPC dial-out mdt 
[[outputs.influxdb]]
  database = "cisco_mdt"
  # urls = [ "http://127.0.0.1:8086" ]
  urls = [ "http://influxdb:8086" ]
  username = "admin"
  password = "telegraf"

# Telegraf log file 
[[outputs.file]]
  files = ["/var/log/telegraf/telegraf.log"] 
root@76b1861886f9:/# 
```

### Create a Trustpoint and Enroll the `ca-cert.pem` on IOSXE device 

We will be enrolling the CA cert manually via terminal (cut-and-paste) method as describe in the [Public Key Infrastructure Configuration Guide, Cisco IOS XE 17](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_pki/configuration/xe-17/sec-pki-xe-17-book/sec-cert-enroll-pki.html)
, though you also have different other method available but this is easiest one, you just need to copy the contents of the `ca-cert.pem` and paste it on the IOSXE device. 

Let's copy the contents of the `ca-cert.pem`. make sure you copy include the header and footer of the cert too. 

```bash
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ cat ca-cert.pem 
-----BEGIN CERTIFICATE-----
MIIF/zCCA+egAwIBAgIUZu5iEsBGOvAgPIge3/TcZSOxeV4wDQYJKoZIhvcNAQEL
BQAwgY4xCzAJBgNVBAYTAkdCMRAwDgYDVQQIDAdFbmdsYW5kMQ8wDQYDVQQHDAZM
b25kb24xEjAQBgNVBAoMCURldm5ldEJybzEPMA0GA1UECwwGTmV0T3BzMTcwNQYD
VQQDDC5kZXZuZXRicm8uY29tIGVtYWlsQWRkcmVzcz1hZG1pbkBkZXZuZXRicm8u
Y29tMB4XDTIyMTAwNTAyNTI0N1oXDTMyMTAwMjAyNTI0N1owgY4xCzAJBgNVBAYT
AkdCMRAwDgYDVQQIDAdFbmdsYW5kMQ8wDQYDVQQHDAZMb25kb24xEjAQBgNVBAoM
CURldm5ldEJybzEPMA0GA1UECwwGTmV0T3BzMTcwNQYDVQQDDC5kZXZuZXRicm8u
Y29tIGVtYWlsQWRkcmVzcz1hZG1pbkBkZXZuZXRicm8uY29tMIICIjANBgkqhkiG
9w0BAQEFAAOCAg8AMIICCgKCAgEArdswBYPJQiagX+6u4mgLUooYXHRNDSoyBH2/
KnbGjvjz+Sr0hFQdrdmKrOiyWCbWBmM0BTXP7+Gc2g9tWXd5c8bTIYlP/eq0CbPl
tsZh97dV6Zx7tBlo7hI4Zb1JgbU2Reqj7vmIlFETjbFwUYqpIUswTY/d9h41Oux2
7XgVFd9H+RC5l9HZvNuZu1rT+k4aJ/La3V4crFxT5NPapfQY+S66Tov0dkQOojuk
caxkYtuiMe5Z4AQuoz6OQYvZKP5e1cN/mcOn6+pEQ12Luzqbh/lzVG2Kqf1c0s92
RS1WXAbG3EFTUH0jYCI8FWF1BLahp+UPN+e5H3B6+M8tA2pByZ14gntBUEG4q/VS
1MCuJXmeCpJwcqH+WNnthBlmtIr2wLYJm83cmXlYMFWlJItBg8auX4SQINo476Q5
Y60swm21D9NqQ0ZeTQMBjt5Cb9MTl7DWFY0PbXcFyVWCUYPNil1w8pFLuKkHFm8M
idjGKOTq7dfJGzMbSOknPn98KZU3U2GMQUGA0gIYlpEtg+j/jKVHZchQCTzN6lyv
utyfyNdFL3RLh9SW/xV5O4FNGoWJQ4n1QwMVuHoAJa/dPelyKcP89W1vWgbrIbCl
er345mfYEEOwQ07oz926uma6htZq45h4XfTwwelWwBjPJpZRZ+DCOFv7SE4Qbwvf
BCxgwS8CAwEAAaNTMFEwHQYDVR0OBBYEFGGg6sbx8tAIad9noHTaaUCDIHdYMB8G
A1UdIwQYMBaAFGGg6sbx8tAIad9noHTaaUCDIHdYMA8GA1UdEwEB/wQFMAMBAf8w
DQYJKoZIhvcNAQELBQADggIBAKhrYFQue9JE/2i7eY/DOJvBdKVSbiCZ/NUyMqX5
3sLiP/a2/oKYh3hG7BKE0C67FjSPJdk89WsXLd+vnLiVYPcsHJnzfjpCN0h2vudk
+unXSChqL6yrK0DxRNKYfpIfJisqg5ZQDYtVJW8aHgPFZXO/R2Ncsn8pxHMFXPnT
RVWL9+zcyyJtcXQERwiBDaVu+5L1Vkdqk24vSkfxsczTV1fQUMvtYHN7Jl44xrzW
9gdWLGgjofJkDnp/T4b3XTcat/1X+lDIYVQijY1etMWCoY3sPEUwJ2VcLpJRCyw4
LLsjs75g4gOILMPmWSpKvhVCTl9xjeEm6TZ3uO+wicckxkV/+zoOKpXd/1X1kkr2
7IJMbrWyQFqKaaN6UKdq5lLWnTrocESJkr/mo29Obp6fhuRc/3+YYNJnaA3XdU/K
tuVo9/BYlG2rWdqMiDvLDna6XCI7InOAQ4nWa35OIyKkpTMS5FyB8oaGV4D/6B+k
kntUCp7XmB/JIZNzZSDCpCtp5Q0xVxpxT7NKbQUl1NdJ5utKjze7HYXmnK2k+o7z
vQwACpzHNcdCnf1TxTISWl7haOfVKGj6gCrfI2zyQGQvfMTE6JsVdOuqN6MBCL5s
dGZaHUVdL+fVmlKxab3rDOtiF8hvDt3irh6enU0LuX86aZcZ9blaqowq+6ve6Guq
yFBV
-----END CERTIFICATE-----
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ 
```

Now login to the IOSXE device and configure a trustpoint and enroll the certificate by pasting the above `ca-cert.pem` contents.

```shell
conf t
 crypto pki trustpoint my-tp
  enrollment terminal
  chain-validation stop
  revocation-check none
  exit
 crypto pki authenticate my-tp
	<< paste contents of ca-cert.pem >>

```

__Output__

```shell
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ ssh admin@10.100.5.207 
The authenticity of host '10.100.5.207 (10.100.5.207)' can't be established.
RSA key fingerprint is SHA256:2R/W7K3jkfveWdGEpIFCQsQsbL5nxKtKVeucdfRhLXs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.100.5.207' (RSA) to the list of known hosts.
Password: 



cml-dist-rtr02#
cml-dist-rtr02#
cml-dist-rtr02#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
cml-dist-rtr02(config)# crypto pki trustpoint my-tp
cml-dist-rtr02(ca-trustpoint)#  enrollment terminal
cml-dist-rtr02(ca-trustpoint)#  chain-validation stop
cml-dist-rtr02(ca-trustpoint)#  revocation-check none
cml-dist-rtr02(ca-trustpoint)#  exit
cml-dist-rtr02(config)# crypto pki authenticate my-tp

Enter the base 64 encoded CA certificate.
End with a blank line or the word "quit" on a line by itself

-----BEGIN CERTIFICATE-----
MIIF/zCCA+egAwIBAgIUZu5iEsBGOvAgPIge3/TcZSOxeV4wDQYJKoZIhvcNAQEL
BQAwgY4xCzAJBgNVBAYTAkdCMRAwDgYDVQQIDAdFbmdsYW5kMQ8wDQYDVQQHDAZM
b25kb24xEjAQBgNVBAoMCURldm5ldEJybzEPMA0GA1UECwwGTmV0T3BzMTcwNQYD
VQQDDC5kZXZuZXRicm8uY29tIGVtYWlsQWRkcmVzcz1hZG1pbkBkZXZuZXRicm8u
Y29tMB4XDTIyMTAwNTAyNTI0N1oXDTMyMTAwMjAyNTI0N1owgY4xCzAJBgNVBAYT
AkdCMRAwDgYDVQQIDAdFbmdsYW5kMQ8wDQYDVQQHDAZMb25kb24xEjAQBgNVBAoM
CURldm5ldEJybzEPMA0GA1UECwwGTmV0T3BzMTcwNQYDVQQDDC5kZXZuZXRicm8u
Y29tIGVtYWlsQWRkcmVzcz1hZG1pbkBkZXZuZXRicm8uY29tMIICIjANBgkqhkiG
9w0BAQEFAAOCAg8AMIICCgKCAgEArdswBYPJQiagX+6u4mgLUooYXHRNDSoyBH2/
KnbGjvjz+Sr0hFQdrdmKrOiyWCbWBmM0BTXP7+Gc2g9tWXd5c8bTIYlP/eq0CbPl
tsZh97dV6Zx7tBlo7hI4Zb1JgbU2Reqj7vmIlFETjbFwUYqpIUswTY/d9h41Oux2
7XgVFd9H+RC5l9HZvNuZu1rT+k4aJ/La3V4crFxT5NPapfQY+S66Tov0dkQOojuk
caxkYtuiMe5Z4AQuoz6OQYvZKP5e1cN/mcOn6+pEQ12Luzqbh/lzVG2Kqf1c0s92
RS1WXAbG3EFTUH0jYCI8FWF1BLahp+UPN+e5H3B6+M8tA2pByZ14gntBUEG4q/VS
1MCuJXmeCpJwcqH+WNnthBlmtIr2wLYJm83cmXlYMFWlJItBg8auX4SQINo476Q5
Y60swm21D9NqQ0ZeTQMBjt5Cb9MTl7DWFY0PbXcFyVWCUYPNil1w8pFLuKkHFm8M
idjGKOTq7dfJGzMbSOknPn98KZU3U2GMQUGA0gIYlpEtg+j/jKVHZchQCTzN6lyv
utyfyNdFL3RLh9SW/xV5O4FNGoWJQ4n1QwMVuHoAJa/dPelyKcP89W1vWgbrIbCl
er345mfYEEOwQ07oz926uma6htZq45h4XfTwwelWwBjPJpZRZ+DCOFv7SE4Qbwvf
BCxgwS8CAwEAAaNTMFEwHQYDVR0OBBYEFGGg6sbx8tAIad9noHTaaUCDIHdYMB8G
A1UdIwQYMBaAFGGg6sbx8tAIad9noHTaaUCDIHdYMA8GA1UdEwEB/wQFMAMBAf8w
DQYJKoZIhvcNAQELBQADggIBAKhrYFQue9JE/2i7eY/DOJvBdKVSbiCZ/NUyMqX5
3sLiP/a2/oKYh3hG7BKE0C67FjSPJdk89WsXLd+vnLiVYPcsHJnzfjpCN0h2vudk
+unXSChqL6yrK0DxRNKYfpIfJisqg5ZQDYtVJW8aHgPFZXO/R2Ncsn8pxHMFXPnT
RVWL9+zcyyJtcXQERwiBDaVu+5L1Vkdqk24vSkfxsczTV1fQUMvtYHN7Jl44xrzW
9gdWLGgjofJkDnp/T4b3XTcat/1X+lDIYVQijY1etMWCoY3sPEUwJ2VcLpJRCyw4
LLsjs75g4gOILMPmWSpKvhVCTl9xjeEm6TZ3uO+wicckxkV/+zoOKpXd/1X1kkr2
7IJMbrWyQFqKaaN6UKdq5lLWnTrocESJkr/mo29Obp6fhuRc/3+YYNJnaA3XdU/K
tuVo9/BYlG2rWdqMiDvLDna6XCI7InOAQ4nWa35OIyKkpTMS5FyB8oaGV4D/6B+k
kntUCp7XmB/JIZNzZSDCpCtp5Q0xVxpxT7NKbQUl1NdJ5utKjze7HYXmnK2k+o7z
vQwACpzHNcdCnf1TxTISWl7haOfVKGj6gCrfI2zyQGQvfMTE6JsVdOuqN6MBCL5s
dGZaHUVdL+fVmlKxab3rDOtiF8hvDt3irh6enU0LuX86aZcZ9blaqowq+6ve6Guq
yFBV
-----END CERTIFICATE-----

Certificate has the following attributes:
       Fingerprint MD5: A39B7683 F6B047A2 5DDB3B4D 17928288 
      Fingerprint SHA1: 94CDBCDF 0DA14FA0 065EA440 F4D8BA92 6437B89B 

% Do you accept this certificate? [yes/no]: yes
Trustpoint CA certificate accepted.
% Certificate successfully imported

cml-dist-rtr02(config)#
```

Now we have created the trustpoint and enrolled the certificate, next step is to configure the gRPC subscription with TLS on the IOSXE device. 

### Configure gRPC subscription with TLS on the IOSXE device

```shell
conf t
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
 source-address 10.100.5.207
 stream yang-push
 update-policy periodic 1000
 no receiver ip address 10.121.249.133 57000 protocol grpc-tcp
 receiver ip address 10.121.249.133 57000 protocol grpc-tls profile my-tp
 end
!
```

__Output__

```shell
cml-dist-rtr02(config)#telemetry ietf subscription 101
cml-dist-rtr02(config-mdt-subs)# encoding encode-kvgpb
cml-dist-rtr02(config-mdt-subs)# filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
cml-dist-rtr02(config-mdt-subs)# source-address 10.100.5.207
cml-dist-rtr02(config-mdt-subs)# stream yang-push
cml-dist-rtr02(config-mdt-subs)# update-policy periodic 1000
cml-dist-rtr02(config-mdt-subs)# no receiver ip address 10.121.249.133 57000 protocol grpc-tcp
cml-dist-rtr02(config-mdt-subs)# receiver ip address 10.121.249.133 57000 protocol grpc-tls profile my-tp
cml-dist-rtr02(config-mdt-subs)# end
cml-dist-rtr02#!
```

Let's verify the subscription, if there is any error. 

`show telemetry ietf subscription 101 receiver`

__Output__

```shell
cml-dist-rtr02#show telemetry ietf subscription 101 receiver
Telemetry subscription receivers detail:

  Subscription ID: 101
  Address: 10.121.249.133
  Port: 57000
  Protocol: grpc-tls
  Profile: my-tp
  Connection: 295
  State: Connected
  Explanation: 


cml-dist-rtr02#
```

As you can see `State: Connected` in the above output, that means IOSXE device is successfully connected with the telegraf receiver and streaming the telemetry periodically. 

`Protocol: grpc-tls` you can see the secure gRPC is being used. 

Let's run couple of more commands to see the details of this stream. 

```shell
cml-dist-rtr02#show telemetry ietf subscription 101       
  Telemetry subscription brief

  ID               Type        State       Filter type      
  --------------------------------------------------------
  101              Configured  Valid       xpath            

cml-dist-rtr02#
cml-dist-rtr02#show telemetry ietf subscription 101 detail 
Telemetry subscription detail:

  Subscription ID: 101
  Type: Configured
  State: Valid
  Stream: yang-push
  Filter:
    Filter type: xpath
    XPath: /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
  Update policy:
    Update Trigger: periodic
    Period: 1000
  Encoding: encode-kvgpb
  Source VRF: 
  Source Address: 10.100.5.207
  Notes: 

  Receivers:
    Address                                    Port     Protocol         Protocol Profile      
    -----------------------------------------------------------------------------------------
    10.121.249.133                             57000    grpc-tls         my-tp                 


cml-dist-rtr02#
```

### Verify secure gRPC subscription via Telegraf

As we have seen above that gRPC with TLS connected and streaming the data which is being received by Telegraf. We can also confirm this on the Telegraf.

Login to the Telegraf container and check the logs 

```shell
docker exec -it telegraf /bin/bash
tail -f /var/log/telegraf/telegraf.log 
```

__Output__

```shell
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker exec -it telegraf /bin/bash
root@d7b9a0b9a476:/# tail -f /var/log/telegraf/telegraf.log 
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970340762000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970350766000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970360765000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970370762000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=1i 1664970380766000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970390764000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970400765000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970410762000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970420765000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970430767000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=1i 1664970440763000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970450762000000
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,host=ubuntu-server,path=Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization,source=cml-dist-rtr02,subscription=101 five_seconds=0i 1664970460762000000
^C
root@d7b9a0b9a476:/# 
```

Great! we are seeing the telemetry data is being received by Telegraf. 

### Verify secure gRPC subscription via Influxdb

Let's verify it via Influxdb if it is being written in the Influxdb as well. 

```shell
docker exec -it influxdb /bin/bash
influx
show users
show databases
use cisco_mdt
show measurements
SELECT COUNT("five_seconds") FROM "Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization"
```

__Output__

```shell
ubuntu@devnet-box:~/cisco-mdt-tig/certs$ docker exec -it influxdb /bin/bash
root@3bbec2e42c5e:/# influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
> show users
user admin
---- -----
> show databases
name: databases
name
----
cisco_mdt
_internal
> use cisco_mdt
Using database cisco_mdt
> show measurements
name: measurements
name
----
Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization
> SELECT COUNT("five_seconds") FROM "Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization"
name: Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization
time count
---- -----
0    191
> 
```

In the future, I will be covering to present this data in to nice graphical form via Grafana, as I am currently having a port issues accessing the Grafana. 

Hope you enjoy this post. 

## References: 

_https://github.com/jeremycohoe/cisco-ios-xe-mdt/blob/master/c9300-grpc-tls-lab.md_

_https://dev.to/techschoolguru/how-to-secure-grpc-connection-with-ssl-tls-in-go-4ph_

