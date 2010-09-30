#!/bin/sh
# find rpm provides and requires for Haskell GHC libraries

#set -x

# To use add the following lines to spec file:
#   %define _use_internal_dependency_generator 0
#   %define __find_requires /usr/lib/rpm/ghc-deps.sh --requires
#   %define __find_provides /usr/lib/rpm/ghc-deps.sh --provides

[ $# -ne 1 ] && echo "Usage: `basename $0` [--provides|--requires]" && exit 1

MODE=$1

case $MODE in
    --provides) FIELD=id ;;
    --requires) FIELD=depends
esac

files=$(cat)

PKGCONF=$(echo $files | tr [:blank:] '\n' | grep package.conf.d)

if [ -n "$PKGCONF" ]; then
  CONFDIR=$(dirname $PKGCONF)
  PKGS=$(ghc-pkg -f $CONFDIR describe '*' | awk '/^name: / {print $2}')
  for pkg in $PKGS; do
    HASHS=$(ghc-pkg -f $CONFDIR field $pkg $FIELD | sed -e "s/^$FIELD: \+//")
    for i in $HASHS; do
      echo "ghc($i)"
    done
  done
fi

echo $files | tr [:blank:] '\n' | /usr/lib/rpm/rpmdeps $MODE
