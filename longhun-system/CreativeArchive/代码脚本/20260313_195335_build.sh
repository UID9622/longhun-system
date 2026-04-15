export NODE_TLS_REJECT_UNAUTHORIZED=0
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

newCloudBuildInfo() {
	# set version
	if [ "$serviceVersion" ]; then
		package_version=$serviceVersion
	else
		package_version=$(node -p "require('./package.json').version")
	fi
	datetime=$(date +%Y%m%d%H%M%S)
	buildVersion=$package_version.$datetime
	echo buildVersion: $buildVersion
	echo "buildVersion=$buildVersion" >buildInfo.properties
}

getArtget() {
	curl -sS https://cmc-nkg-artifactory.cmc.tools.huawei.com/artifactory/cmc-software-release/CloudArtifact/ArtGet/1.3.7.2/linux/artget > /tmp/artget
	chmod 755 /tmp/artget
	export PATH="/tmp:$PATH"
}

getHeader() {
	# prepare for Installing
	ELECTRON_HEADERS_VERSION="16.16.0"
	HEADERS_PATH="$HOME/.cache/node-gyp/${ELECTRON_HEADERS_VERSION}"
	mkdir -p "$HEADERS_PATH"
	artget pull -ap "$HEADERS_PATH" -g "hw-cloudide/vscode-huawei" \
		-a "tools/electron-headers" -v "v${ELECTRON_HEADERS_VERSION}/node-v${ELECTRON_HEADERS_VERSION}-headers.tar.gz" \
		-at artifactsds -repo-username cloudide -repo-password "${artgetpw}"
	tar zxf "$HEADERS_PATH/node-v${ELECTRON_HEADERS_VERSION}-headers.tar.gz" -C "$HEADERS_PATH" node_headers/include --strip-components 1
	echo 9 >"$HEADERS_PATH/installVersion"
	# Install node headers
	npm install -g node-gyp@5.1.0
	node-gyp install --dist-url "http://mirrors.tools.huawei.com/nodejs" $(node -v)
}

newCloudBuildInfo
getArtget
getHeader

npm config set strict-ssl false
npm install
npx vsce package