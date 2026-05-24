#!/usr/bin/env bash
# ~/.zshrc 最后一行加:  source "$HOME/longhun-system/lh-env.sh"
export LONGHUN_ROOT="${LONGHUN_ROOT:-$HOME/longhun-system}"
export PATH="${LONGHUN_ROOT}/bin:${PATH}"
alias lh-dna="bash ${LONGHUN_ROOT}/lh-dna"
alias lh-notion="bash ${LONGHUN_ROOT}/bin/Notion算力.sh"
