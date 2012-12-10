%define section free
%define debug_package %{nil}
%define gcj_support 1

Name:           cpptasks
Version:        1.0
Release:        %mkrel 0.b4.4.4
Epoch:          0
Summary:        Compile and link task
License:        Apache License
URL:            http://ant-contrib.sourceforge.net/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        http://easynews.dl.sourceforge.net/ant-contrib/cpptasks-1.0b4.tar.bz2
Source1:	cpptasks-antlib.xml
Requires:	xerces-j2
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  xerces-j2
Requires:  	ant >= 0:1.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
%endif

%description
This task can compile various source languages 
and produce executables, shared libraries 
(aka DLL's) and static libraries. Compiler 
adaptors are currently available for several 
C/C++ compilers, FORTRAN, MIDL and Windows 
Resource files. 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        manual
Summary:        Docs for %{name}
Group:          Development/Java

%description    manual
%{summary}.

%prep
%setup -q -n %{name}-%{version}b4
find . -name "*.jar" -exec rm {} \;


%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath xerces-j2)
%{__mkdir_p} build/classes/net/sf/antcontrib/cpptasks
install -m 644 %{SOURCE1} build/classes/net/sf/antcontrib/cpptasks/antlib.xml
%ant jars javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -Dpm 644 build/lib/%{name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#cp -p LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#cp -p NOTICE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

for i in LICENSE NOTICE `find $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} -type f`; do
  %{__perl} -pi -e 's/\r$//g' $i
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE NOTICE
%{_javadir}/*.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

# -----------------------------------------------------------------------------


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.0-0.b4.4.4mdv2011.0
+ Revision: 617435
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 0:1.0-0.b4.4.3mdv2010.0
+ Revision: 425149
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.0-0.b4.4.2mdv2009.0
+ Revision: 136345
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-0.b4.4.2mdv2008.1
+ Revision: 120855
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-0.b4.4.1mdv2008.0
+ Revision: 87301
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Aug 28 2007 David Walluck <walluck@mandriva.org> 0:1.0-0.b4.4.0mdv2008.0
+ Revision: 72510
- rebuild
- Import cpptasks



* Wed Aug 09 2006 David Walluck <walluck@mandriva.org> 0:1.0-0.b4.4mdv2007.0
- (Build)Requires: xerces-j2

* Mon Jul 24 2006 David Walluck <walluck@mandriva.org> 0:1.0-0.b4.3mdv2007.0
- rebuild

* Wed Jun 14 2006 David Walluck <walluck@mandriva.org> 0:1.0-0.b4.2mdv2007.0
- fix duplicated LICENSE and NOTICE files

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.0-0.b4.1mdv2007.0

* Fri Oct 28 2005 David Walluck <walluck@mandriva.org> 0:1.0-0.b3.2.0.2mdk
- add antlib.xml

* Fri Oct 28 2005 David Walluck <walluck@mandriva.org> 0:1.0-0.b3.2.0.1mdk
- release

* Mon Sep 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b3.2jpp
- Upgrade to Ant 1.6.X
- Build with ant-1.6.2
- Upgraded to 1.0.b3 and relaxed requirements on Thu Jul 15 2004 
  by Ralph Apel <r.apel at r-apel.de> as 0:1.0-0.b3.1jpp

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.4jpp
- Build with ant-1.6.2
- Relax versioned BuildReq
- Drop junit runtime requirement

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.3jpp
- Also runtime dep to Ant 1.6.X

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.0-0.b2.2jpp
- Upgrade to Ant 1.6.X

* Wed Mar 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b2.1jpp
- First JPackage release
