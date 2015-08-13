%{?_javapackages_macros:%_javapackages_macros}
Name:		cpptasks
Version:	1.0b5
Release:	15
Summary:	Compile and link task for ant
Group:		Development/Java
License:	ASL 2.0
URL:		http://ant-contrib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ant-contrib/cpptasks-1.0b5.tar.gz

BuildRequires:	ant 
BuildRequires:	maven-local

BuildArch:	noarch

%description
This ant task can compile various source languages and produce
executables, shared libraries (aka DLL's) and static libraries. Compiler
adaptors are currently available for several C/C++ compilers, FORTRAN,
MIDL and Windows Resource files.

%package        javadoc
Summary:	Javadoc for %{name}

%description	javadoc
Javadoc documentation for %{summary}.

%prep
%setup -q

find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

sed -i 's/\r//' NOTICE 

# Use default compiler configuration
%pom_remove_plugin :maven-compiler-plugin

# Let xmvn generate javadocs
%pom_remove_plugin :maven-javadoc-plugin

# Fix dependency on ant
%pom_remove_dep ant:ant
%pom_remove_dep ant:ant-nodeps
%pom_remove_dep ant:ant-trax
%pom_add_dep org.apache.ant:ant

%mvn_file :%{name} ant/%{name}

%build
%mvn_build

%install
%mvn_install

# Place a file into ant's config dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/
echo "ant/%{name}" > $RPM_BUILD_ROOT/%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%doc LICENSE NOTICE
%{_sysconfdir}/ant.d/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Jun 17 2015 Mat Booth <mat.booth@redhat.com> - 1.0b5-15
- Fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 12 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0b5-12
- Use default compiler config and fix bad deps on ant.

* Sun Aug 11 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0b5-11
- Build with maven 3, update for newer guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-5
- Req needs whitespace

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-4
- tag bump

* Thu Sep 03 2009 D Haley <mycae@yahoo.com> - 1.0b5-3
- Remove excess BR
- Fix subpackage dep
- Fix doc installation 

* Fri Aug 28 2009 D Haley <mycae@yahoo.com> - 1.0b5-2
- Fix doc installation 
- Move to _javadir/ant/ rather than _javadir/
- Fix requires + buildrequires for both main and javadoc packages
- Add README.fedora source in lieu of  maven build 

* Sat Mar 14 2009 D Haley <mycae@yahoo.com> - 1.0b5-1
- Update to b5
- cpptasks now uses difficult mvn-doxia xdoc, so remove manual subpackage
- Add distribution jar check
- EOL conversion on NOTICE
- Change summary & format description
- Fix BuildRoot 
- Change licence to ASL 2.0 from Apache Software Licence 2.0
- Documentation to "Documentation" Group

