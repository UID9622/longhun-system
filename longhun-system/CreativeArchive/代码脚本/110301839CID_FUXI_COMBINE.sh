source strace_script_https.sh
export NODE_TLS_REJECT_UNAUTHORIZED=0 ||exit 1
export NODE_EXTRA_CA_CERTS=/etc/pki/tls/certs/ca-bundle.crt ||exit 1
npm i ||exit 1
npm run package ||exit 1
