%define section free
%define debug_package %{nil}
%define gcj_support 1

Name:           cpptasks
Version:        1.0
Release:        %mkrel 0.b4.4.2
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
