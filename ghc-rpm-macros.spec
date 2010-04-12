Name:		ghc-rpm-macros
Version:	0.5.6
Release:	1%{?dist}
Summary:	Macros for building packages for GHC

Group:		Development/Libraries
License:	GPLv3
URL:		https://fedoraproject.org/wiki/Haskell_SIG

# This is a Fedora maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0:	ghc-rpm-macros.ghc
Source1:	COPYING
Source2:	AUTHORS
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

%description
A set of macros for building GHC packages following the Haskell Guidelines
of the Haskell SIG. This package probably shouldn't be installed on its own
as GHC is needed in order to make use of these macros.

%prep
%setup -c -T
cp %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/rpm
cp -p %{SOURCE0} ${RPM_BUILD_ROOT}/%{_sysconfdir}/rpm/macros.ghc


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS
%config(noreplace) %{_sysconfdir}/rpm/macros.ghc


%changelog
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

