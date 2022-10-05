
# Generate CA’s private key and its self-signed certificate
openssl req -x509 -newkey rsa:4096 -days 3650 -nodes \
        -keyout ca-key.pem -out ca-cert.pem \
        -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=devnetbro.com emailAddress=admin@devnetbro.com"

echo "printing the 'ca-cert.pem' in human readable format"
openssl x509 -in ca-cert.pem -noout -text

printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

# Sleep for 2 seconds
sleep 2

# Generate server's private key and certificate signing request (CSR)
openssl req -newkey rsa:4096 -nodes \
        -keyout server.key -out server.csr \
        -subj "/C=GB/ST=England/L=London/O=DevnetBro/OU=NetOps/CN=grpc emailAddress=admin@devnetbro.com"

echo "printing the 'server.csr' in human readable format"
openssl req -in server.csr -noout -text

printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

# Sleep for 2 seconds
sleep 2

echo "Creating server's extfile 'server-extfile.cnf'"
cat > server-extfile.cnf <<EOF

authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
IP.1  = 10.121.249.133

EOF

# Sleep for 2 seconds
sleep 2

# Use CA’s private key and cert to sign the server’s CSR
openssl x509 -req -in server.csr -days 3650 \
    -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
    -out server.crt -extfile server-extfile.cnf

echo "printing the 'server.crt' in human readable format"
openssl x509 -in server.crt -noout -text

printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
printf '%s\n' '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

# Sleep for 2 seconds
sleep 2

echo "Verifying 'server.crt' with the root CA"
openssl verify -CAfile ca-cert.pem -verbose server.crt
