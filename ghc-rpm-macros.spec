%global debug_package %{nil}

%global macros_file %{_sysconfdir}/rpm/macros.ghc

Name:           ghc-rpm-macros
Version:        0.13.5
Release:        1%{?dist}
Summary:        Macros for building packages for GHC

Group:          Development/Libraries
License:        GPLv3
URL:            https://fedoraproject.org/wiki/Haskell_SIG

# This is a Fedora maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0:        ghc-rpm-macros.ghc
Source1:        COPYING
Source2:        AUTHORS
Source3:        ghc-deps.sh

%description
A set of macros for building GHC packages following the Haskell Guidelines
of the Fedora Haskell SIG.  ghc needs to be installed in order to make use of
these macros.


%prep
%setup -c -T
cp %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} ${RPM_BUILD_ROOT}/%{macros_file}

install -p -D -m 0755 %{SOURCE3} %{buildroot}/%{_prefix}/lib/rpm/ghc-deps.sh

# this is why this package is now arch-dependent:
# turn off shared libs and dynamic linking on secondary archs
%ifnarch %{ix86} x86_64
cat >> %{buildroot}/%{macros_file} <<EOF

# shared libraries are only supported on primary intel archs
%%ghc_without_dynamic 1
%%ghc_without_shared 1
EOF
%endif


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%config(noreplace) %{macros_file}
%{_prefix}/lib/rpm/ghc-deps.sh


%changelog
* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.5-1
- ghc_bootstrap is now a macro which sets ghc_bootstrapping,
  ghc_without_shared, without_prof, without_haddock, without_hscolour,
  without_manual, without_testsuite
- tweaks to ghc_check_bootstrap

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.4-1
- add ghc_check_bootstrap

* Thu Jun  2 2011 Jens Petersen <petersen@redhat.com> - 0.13.3-1
- rename macros.ghc-pkg back to macros.ghc
- move the devel summary prefix back to a suffix

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.2-1
- macros need to live in /etc/rpm
- use macro_file for macros.ghc filepath

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.1-1
- move macros.ghc to /usr/lib/rpm to avoid conflict with redhat-rpm-config

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 0.13-1
- merge prof subpackages into devel to simplify packaging

* Mon May  9 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- include ghc_pkg_c_deps even when -c option used

* Sat May  7 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- drop ghc_pkg_deps from ghc_package_devel and ghc_package_prof since
  ghc-deps.sh generates better inter-package dependencies already
- condition --htmldir on pkg_name

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 0.11.14-1
- provides ghc-*-doc still needed for current lib templates

* Mon Mar 28 2011 Jens Petersen <petersen@redhat.com> - 0.11.13-1
- ghc-deps.sh: check PKGBASEDIR exists to avoid warning for bin package
- abort cabal_configure if ghc is not self-bootstrapped
- make ghc_reindex_haddock a safe no-op
- no longer provide ghc-*-doc
- no longer run ghc_reindex_haddock in ghc-*-devel scripts

* Thu Mar 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.12-1
- add ghc_pkg_obsoletes to binlib base lib package too

* Wed Mar  9 2011 Jens Petersen <petersen@redhat.com> - 0.11.11-1
- add docdir when subpackaging packages too

* Sun Feb 13 2011 Jens Petersen <petersen@redhat.com> - 0.11.10-1
- this package is now arch-dependent
- rename without_shared to ghc_without_shared and without_dynamic
  to ghc_without_dynamic so that they can be globally defined for
  secondary archs without shared libs
- use %%undefined macro
- disable debug_package in ghc_bin_build and ghc_lib_build
- set ghc_without_shared and ghc_without_dynamic on secondary
  (ie non main intel) archs
- disable debuginfo for self

* Fri Feb 11 2011 Jens Petersen <petersen@redhat.com> - 0.11.9-1
- revert "set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build" change, since happening for all archs

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.8-1
- only link Setup dynamically if without_shared and without_dynamic not set
- set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build
- add cabal_configure_options to pass extra options to cabal_configure

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.7-1
- fix ghc-deps.sh for without_shared libraries

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Jens Petersen <petersen@redhat.com> - 0.11.6-1
- simplify adding shared subpackage license file
- own ghc-deps.sh not /usr/lib/rpm

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 0.11.5-1
- add rpm hash requires for dynamic executables in ghc-deps.sh
- compile Setup in cabal macro
- use _rpmconfigdir

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 0.11.4-1
- drop deprecated ghcdocdir and ghcpkgdir
- new ghclibdocdir
- replace some missed RPM_BUILD_ROOT's
- bring back ghc requires in ghc_devel_requires
- improve prof summary and description
- add without_prof and without_haddock option macros

* Fri Jan 21 2011 Jens Petersen <petersen@redhat.com> - 0.11.3-1
- compile Setup to help speed up builds

* Thu Jan 20 2011 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- put docdir (license) also into shared lib subpackage
- add ghc_binlib_package option to exclude package from ghc_packages_list
- condition lib base package additional description for srpm

* Mon Jan  3 2011 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- use buildroot instead of RPM_BUILD_ROOT
- rename ghcpkgbasedir to ghclibdir
- split "[name-version]" args into "[name] [version]" args
- move remaining name and version macro options (-n and -v) to args
- drop deprecated -o options

* Thu Dec 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- add support for subpackaging ghc's libraries:
- deprecate ghcpkgdir and ghcdocdir from now on
- ghc_gen_filelists optional arg is now name-version
- ghc_lib_build, ghc_lib_install, cabal_pkg_conf now take optional
  name-version arg

* Mon Dec 20 2010 Jens Petersen <petersen@redhat.com> - 0.10.3-1
- revert disabling debug_package, since with redhat-rpm-config installed
  the behaviour depended on the position of ghc_lib_package in the spec file
  (reported by narasim)

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com>
- drop with_devhelp since --html-help option gone from haddock-2.8.0

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- ignore ghc's builtin pseudo-libs

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.1-1
- bring back the explicit n-v-r internal package requires for devel and prof packages

* Mon Nov 22 2010 Jens Petersen <petersen@redhat.com> - 0.10.0-1
- turn on pkg hash metadata (for ghc-7 builds)
- ghc-deps.sh now requires an extra buildroot/ghcpkgbasedir arg
- automatic internal package deps from prof to devel to base
- rename ghc_requires to ghc_devel_requires
- drop ghc_doc_requires
- ghc_reindex_haddock is deprecated and now a no-op

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- fix without_shared build so it actually works

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.0-1
- add rpm provides and requires script ghc-deps.sh for package hash metadata
- turn on hash provides and disable debuginfo by default
- make shared and hscolour default
- use without_shared and without_hscolour to disable them
- add ghc_pkg_obsoletes for obsoleting old packages
- use ghcpkgbasedir
- always obsolete -doc packages, but keep -o for now for backward compatibility

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.1-1
- fix ghc_strip_dynlinked when no dynlinked files
- devel should provide doc also when not obsoleting

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-1
- merge -doc into -devel and provide -o obsoletes doc subpackage option

* Mon Jun 28 2010 Jens Petersen <petersen@redhat.com> - 0.7.1-1
- support hscolour'ing of src from haddock
- really remove redundant summary and description option flags

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.7.0-1
- new ghc_bin_build, ghc_bin_install, ghc_lib_build, ghc_lib_install

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.2-1
- a couple more fallback summary tweaks

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.1-1
- drop the summary -s and description -d package options since rpm does not
  seem to allow white\ space in macro option args anyway

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.6.0-1
- make ghc_strip_dynlinked conditional on no debug_package

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- replace ghc_strip_shared with ghc_strip_dynlinked

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.8-1
- add ghc_strip_shared to strip shared libraries

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- add comments over macros
- drop unused cabal_makefile

* Mon Apr 12 2010 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- drop unused ghc_pkg_ver macro
- add ghc_pkg_recache macro

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.5.5-1
- drop optional 2nd version arg from ghcdocdir, ghcpkgdir, and
  ghc_gen_filelists: multiversion subpackages are not supported
- add ghcpkgbasedir
- bring back some shared conditions which were dropped temporarily
- test for ghcpkgdir and ghcdocdir in ghc_gen_filelists
- allow optional pkgname arg for cabal_pkg_conf
- can now package gtk2hs

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- use -v in ghc_requires and ghc_prof_requires for version

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- drop "Library for" from base lib summary

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.2-1
- use -n in ghc_requires and ghc_prof_requires for when no pkg_name

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.1-1
- add ghcdocbasedir
- revert ghcdocdir to match upstream ghc
- ghcdocdir and ghcpkgdir now take optional name version args
- update ghc_gen_filelists to new optional name version args
- handle docdir in ghc_gen_filelists
- ghc_reindex_haddock uses ghcdocbasedir
- summary and description options to ghc_binlib_package, ghc_package_devel,
  ghc_package_doc, and ghc_package_prof

* Sun Jan 10 2010 Jens Petersen <petersen@redhat.com> - 0.5.0-1
- pkg_name must be set now for binlib packages too
- new ghc_lib_package and ghc_binlib_package macros make packaging too easy
- ghc_package_devel, ghc_package_doc, and ghc_package_prof helper macros
- ghc_gen_filelists now defaults to ghc-%%{pkg_name}
- add dynamic bcond to cabal_configure instead of cabal_configure_dynamic

* Thu Dec 24 2009 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- add cabal_configure_dynamic
- add ghc_requires, ghc_doc_requires, ghc_prof_requires

* Tue Dec 15 2009 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- use ghc_version_override to override ghc_version
- fix pkg .conf filelist match

* Sat Dec 12 2009 Jens Petersen <petersen@redhat.com> - 0.3.0-1
- major updates for ghc-6.12, package.conf.d, and shared libraries
- add shared support to cabal_configure, ghc_gen_filelists
- version ghcdocdir
- replace ghc_gen_scripts, ghc_install_scripts, ghc_register_pkg, ghc_unregister_pkg
  with cabal_pkg_conf
- allow (ghc to) override ghc_version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.5-1
- make ghc_pkg_ver only return pkg version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.4-1
- change GHCRequires to ghc_pkg_ver

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.3-1
- use the latest installed pkg version for %%GHCRequires

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.2-1
- add %%GHCRequires for automatically versioned library deps

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-2
- no, revert versioned ghcdocdir again!

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-1
- version ghcdocdir to allow multiple doc versions like ghcpkgdir

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Jens Petersen <petersen@redhat.com> - 0.2-1
- drop version from ghcdocdir since it breaks haddock indexing

* Wed May 13 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-7
- specifies the macros file as a %%conf

* Sat May  9 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-6
- removes archs and replaces with noarch
- bumps to avoid conflicts with jens

* Fri May  8 2009 Jens Petersen <petersen@redhat.com> - 0.1-5
- make it arch specific to fedora ghc archs
- setup a build dir so it can build from the current working dir

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-4
- renamed license file
- removed some extraneous comments needed only at review time

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-3
- updated license to GPLv3
- added AUTHORS file

* Tue May  5 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-2
- moved copying license from %%build to %%prep

* Mon May  4 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-1
- creation of package

