%if 0%{?rhel}%{?el7}
# see https://fedorahosted.org/fpc/ticket/395
%global _monodir %{_prefix}/lib/mono
%global _monogacdir %{_monodir}/gac
%endif

%global debug_package %{nil}
%global _docdir_fmt %{name}

%define oname GtkSharp

Summary:        GTK+ 3 and GNOME 3 bindings for Mono
Name:           gtk-sharp3
Version:        3.22.2
Release:        1
License:        LGPLv2
Url:            https://github.com/GLibSharp/GtkSharp
Source0:        https://github.com/GLibSharp/GtkSharp/archive/refs/tags/%{version}/%{oname}-%{version}.tar.gz
Patch0:         gtk-sharp3-2.99.3-gui-thread-check.patch
Patch1:         gtk-sharp3-2.99.3-gtkrange.patch
Patch2:         gtk-sharp3-3.22.2-nolibdir.patch
Patch3:         gtk-sharp3-3.22.2-add-cairo-sharp-dll-config.patch
BuildRequires:  meson
BuildRequires:  monodoc
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  pkgconfig(mono) 
BuildRequires:  pkgconfig(gtk+-3.0) 
BuildRequires:  pkgconfig(libglade-2.0) 
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  perl-generators


%description
This package provides a library that allows you to build
fully native graphical GNOME applications using Mono. Gtk#
is a binding to version 3 of GTK+, the cross platform user interface
toolkit used in GNOME. It includes bindings for Gtk, Atk,
Pango, Gdk.

%package gapi
Summary:        Tools for creation and maintenance managed bindings for Mono and .NET

%description gapi
This package provides developer tools for the creation and
maintenance of managed bindings to native libraries which utilize
glib and GObject. Some examples of libraries currently bound using
the GAPI tools and found in Gtk# include Gtk, Atk, Pango, Gdk.

%package devel
Summary:        Files needed for developing with gtk-sharp3
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package provides the necessary development libraries and headers
for writing gtk-sharp3 applications.

%package doc
Summary:        Gtk# 3 documentation
Requires:       monodoc
BuildArch:      noarch

%description doc
This package provides the Gtk# 3 documentation for monodoc.

%prep
%autosetup -n %{oname}-%{version} -p1

#fix missing gdk_api_includes references
sed -i "s/gdk_api_includes/gio_api_includes/" Source/gdk/generated/meson.build
sed -i "s/gdk_api_includes/gio_api_includes/" Source/gio/generated/meson.build
sed -i "s/gdk_api_includes/gio_api_includes/" Source/gtk/generated/meson.build
sed -i "s/gdk_api_includes/gio_api_includes/" Source/sample/valtest/generated/meson.build

%build
%meson -Dinstall=true
%meson_build

%install
%meson_install

%files
%doc README.md
%license LICENSE
%{_prefix}/lib/gac/
%{_prefix}/lib/GtkSharp-3.0
%{_prefix}/lib/atk-sharp
%{_prefix}/lib/cairo-sharp
%{_prefix}/lib/gdk-sharp
%{_prefix}/lib/gtk-sharp
%{_prefix}/lib/gio-sharp
%{_prefix}/lib/glib-sharp
%{_prefix}/lib/pango-sharp

%files gapi
%{_bindir}/gapi3-codegen
%{_bindir}/gapi3-fixup
%{_bindir}/gapi3-parser
%dir %{_prefix}/lib/gapi-3.0
%{_prefix}/lib/gapi-3.0/gapi_codegen.exe
%{_prefix}/lib/gapi-3.0/gapi-fixup.exe
%{_prefix}/lib/gapi-3.0/gapi-parser.exe
%{_prefix}/lib/gapi-3.0/gapi_pp.pl
%{_prefix}/lib/gapi-3.0/gapi2xml.pl
%{_datadir}/gapi-3.0
%{_libdir}/pkgconfig/gapi-3.0.pc

%files devel
%{_libdir}/pkgconfig/*-sharp-3.0.pc

%files doc
#{_prefix}/lib/monodoc/sources/*
