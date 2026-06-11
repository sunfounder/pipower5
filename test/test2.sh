#!/bin/bash
# pipower5 test suite
SYSFS=/sys/class/pipower5/pipower5; PS=/sys/class/power_supply/pipower5
G="[32m"; R="[31m"; N="[0m"; B="[1m"; Y="[33m"
PASS=0; FAIL=0; SKIP=0
INT=0; [ "${1:-}" = "--full" ] && INT=1
_p() { echo -e "  $G PASS$N $1"; PASS=$((PASS+1)); }
_f() { echo -e "  $R FAIL$N $1 - $2"; FAIL=$((FAIL+1)); }
_s() { echo -e "  $Y SKIP$N $1 - $2"; SKIP=$((SKIP+1)); }
_sec() { echo ""; echo -e "$B[$1]$N $2"; }