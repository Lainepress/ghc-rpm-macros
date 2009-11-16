Name:		ghc-rpm-macros
Version:	0.2.5
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

