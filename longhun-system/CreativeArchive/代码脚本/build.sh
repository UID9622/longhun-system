export NODE_TLS_REJECT_UNAUTHORIZED=0
export NODE_EXTRA_CA_CERTS=/etc/pki/tls/certs/ca-bundle.crt
npm i
npm run package
