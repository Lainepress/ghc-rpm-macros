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

case $MODE in
    --provides) FIELD=id ;;
    --requires) FIELD=depends ;;
    *) echo "`basename $0`: Need --provides or --requires" ; exit 1
esac

GHCVERSION=$(ghc --numeric-version)

files=$(cat)

#set -x

for i in $files; do
 LIB_FILE=$(echo $i | grep /libHS | egrep -v "$PKGBASEDIR/libHS")
 if [ -n "$LIB_FILE" ]; then
  if [ -d "$PKGCONFDIR" ]; then
    META=""
    SELF=""
    case $LIB_FILE in
      *.so) META=ghc ;;
      *_p.a) META=ghc-prof SELF=ghc-devel ;;
      *.a) META=ghc-devel SELF=ghc ;;
    esac
    if [ -n "$META" ]; then
      PKGVER=$(echo $LIB_FILE | sed -e "s%$PKGBASEDIR/\([^/]\+\)/libHS.*%\1%")
      HASHS=$(ghc-pkg -f $PKGCONFDIR field $PKGVER $FIELD | sed -e "s/^$FIELD: \+//")
      for i in $HASHS; do
	  case $i in
	      *-*) echo $i | sed -e "s/\(.*\)-\(.*\)/$META(\1) = \2/" ;;
	      *) ;;
	  esac
      done
      if [ "$MODE" = "--requires" -a -n "$SELF" ]; then
	HASHS=$(ghc-pkg -f $PKGCONFDIR field $PKGVER id | sed -e "s/^id: \+//")
	for i in $HASHS; do
	  echo $i | sed -e "s/\(.*\)-\(.*\)/$SELF(\1) = \2/"
	done
      fi
    fi
  fi
 elif [ "$MODE" = "--requires" ]; then
   if file $i | grep -q 'executable, .* dynamically linked'; then
     BIN_DEPS=$(ldd $i | grep libHS | grep -v libHSrts | sed -e "s%^\\tlibHS\(.*\)-ghc${GHCVERSION}.so =.*%\1%")
     for p in ${BIN_DEPS}; do
	 HASH=$(ghc-pkg --global field $p id | sed -e "s/^id: \+//")
	 echo $HASH | sed -e "s/\(.*\)-\(.*\)/ghc(\1) = \2/"
     done
   fi
 fi
done

echo $files | tr [:blank:] '\n' | /usr/lib/rpm/rpmdeps $MODE
