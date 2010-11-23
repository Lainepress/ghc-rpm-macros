#!/bin/sh
# find rpm provides and requires for Haskell GHC libraries

# To use add the following lines to spec file:
#   %define _use_internal_dependency_generator 0
#   %define __find_requires /usr/lib/rpm/ghc-deps.sh --requires %{buildroot}%{ghcpkgbasedir}
#   %define __find_provides /usr/lib/rpm/ghc-deps.sh --provides %{buildroot}%{ghcpkgbasedir}

[ $# -ne 2 ] && echo "Usage: `basename $0` [--provides|--requires] %{buildroot}" && exit 1

MODE=$1
PKGBASEDIR=$2
PKGCONFDIR=$PKGBASEDIR/package.conf.d

files=$(cat)

#set -x

if [ -d "$PKGCONFDIR" ]; then
 for i in $files; do
  LIB_FILE=$(echo $i | grep /libHS | grep -v /libHSrts)
  if [ -n "$LIB_FILE" ]; then
    case $LIB_FILE in
      *.so) META=ghc ;;
      *_p.a) META=ghc-prof SELF=ghc-devel ;;
      *.a) META=ghc-devel SELF=ghc ;;
    esac
    if [ -n "$META" ]; then
      case $MODE in
	--provides) FIELD=id ;;
	--requires) FIELD=depends ;;
	*) echo "`basename $0`: Need --provides or --requires" ; exit 1
      esac
      PKGVER=$(echo $LIB_FILE | sed -e "s%$PKGBASEDIR/*\([^/]\+\)/libHS.*%\1%")
      HASHS=$(ghc-pkg -f $PKGCONFDIR field $PKGVER $FIELD | sed -e "s/^$FIELD: \+//")
      for i in $HASHS; do
	echo $i | sed -e "s/\(.*\)-\(.*\)/$META(\1) = \2/"
      done
      if [ "$MODE" = "--requires" -a -n "$SELF" ]; then
	HASHS=$(ghc-pkg -f $PKGCONFDIR field $PKGVER id | sed -e "s/^id: \+//")
	for i in $HASHS; do
	  echo $i | sed -e "s/\(.*\)-\(.*\)/$SELF(\1) = \2/"
	done
      fi
    fi
  fi
 done
fi

echo $files | tr [:blank:] '\n' | /usr/lib/rpm/rpmdeps $MODE
