# .bashrc

# User specific aliases and functions

function wget() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/wget "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function rm() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/rm "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function spawn() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/spawn "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function scp() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/scp "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function mount() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/mount "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function ssh() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/ssh "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function rsync() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/rsync "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function curl() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/curl "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function git() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/git "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}


function yum() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/yum "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function yumdownloader() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    /usr/bin/yumdownloader "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function mvn() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${CID_MAVEN_HOME}/bin/mvn "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function npm() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${NODEJS_HOME}/bin/npm "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function go() {
    echo "$GOPROXY" >> ${CID_CACHE_DIR}/GO_PROXY_LIST
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${GOROOT}/bin/go "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function gradle() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${GRADLE_HOME}/bin/gradle "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function pip() {
    parameter="$@"
    echo "pip $parameter"
    if [[ $parameter =~ "install " || $parameter =~ "download " || $parameter =~ "wheel " ]];then

      if [[ $parameter =~ "uninstall " ]]
      then
        parameter=$parameter
      else
        if [[ x"$CID_PIP_SETTING" == x"cbu-pip-settings" ]];then
          parameter="$parameter -i https://pypi.cloudartifact.dgg.dragon.tools.huawei.com/artifactory/api/pypi/cbu-pypi-public/simple --trusted-host pypi.cloudartifact.dgg.dragon.tools.huawei.com"
        elif [[ x"$CID_PIP_SETTING" == x"huawei-pip-settings" ]];then
          parameter="$parameter -i https://cmc.centralrepo.rnd.huawei.com/artifactory/pypi-central-repo/simple/ --extra-index-url=https://pypi.cloudartifact.dgg.dragon.tools.huawei.com/artifactory/pypi-cbu-common-pypi/simple/ --extra-index-url=https://cmc.centralrepo.rnd.huawei.com/artifactory/product_pypi/simple/ --trusted-host pypi.cloudartifact.dgg.dragon.tools.huawei.com --trusted-host cmc.centralrepo.rnd.huawei.com"
        fi
      fi

    fi
    echo "$parameter" >> ${CID_CACHE_DIR}/PIP_INSTALL_LIST
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${CID_PYTHON_HOME}/bin/pip_bak $parameter
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function pip3() {
    parameter="$@"
    echo "pip3 $parameter"
    if [[ $parameter =~ "install " || $parameter =~ "download " || $parameter =~ "wheel " ]];then

      if [[ $parameter =~ "uninstall " ]]
      then
        parameter=$parameter
      else
        if [[ x"$CID_PIP_SETTING" == x"cbu-pip-settings" ]];then
          parameter="$parameter -i https://pypi.cloudartifact.dgg.dragon.tools.huawei.com/artifactory/api/pypi/cbu-pypi-public/simple --trusted-host pypi.cloudartifact.dgg.dragon.tools.huawei.com"
        elif [[ x"$CID_PIP_SETTING" == x"huawei-pip-settings" ]];then
          parameter="$parameter -i https://cmc.centralrepo.rnd.huawei.com/artifactory/pypi-central-repo/simple/ --extra-index-url=https://pypi.cloudartifact.dgg.dragon.tools.huawei.com/artifactory/pypi-cbu-common-pypi/simple/ --extra-index-url=https://cmc.centralrepo.rnd.huawei.com/artifactory/product_pypi/simple/ --trusted-host pypi.cloudartifact.dgg.dragon.tools.huawei.com --trusted-host cmc.centralrepo.rnd.huawei.com"
        fi
      fi

    fi
    echo "$parameter" >> ${CID_CACHE_DIR}/PIP_INSTALL_LIST
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${CID_PYTHON_HOME}/bin/pip3_bak $parameter
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function bm() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${CID_BM_HOME}/bin/bm "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

function ant() {
    exec 99>> ${CID_CACHE_DIR}/debug.log
    export BASH_XTRACEFD="99"
    set -x
    ${CID_ANT_HOME}/bin/ant -Divy.cache.dir=${IVY_CACHE_DIR} "$@"
    SHELL_STATUS=$?
    set +x
    return $SHELL_STATUS
}

export CID_CACHE_DIR=${PWD}_cache
export -f wget
export -f git
export -f yum
export -f yumdownloader
export -f mvn
export -f npm
export -f gradle
export -f pip
export -f pip3
export -f rm
export -f spawn
export -f scp
export -f mount
export -f ssh
export -f rsync
export -f go
export -f curl
export -f bm
export -f ant

