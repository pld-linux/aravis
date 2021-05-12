#
# Conditional build:
%bcond_without	gui		# Viewer application
%bcond_without	gstreamer	# GStreamer plugin

Summary:	Aravis digital video camera acquisition library
Summary(pl.UTF-8):	Aravis - biblioteka do pobierania obrazu z kamer cyfrowych
Name:		aravis
Version:	0.8.10
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/aravis/0.8/%{name}-%{version}.tar.xz
# Source0-md5:	c40ab0035b5b79ef3e98e04abed94b75
URL:		https://wiki.gnome.org/Projects/Aravis
BuildRequires:	appstream-glib
BuildRequires:	audit-libs-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.10.0
%if %{with gstreamer} || %{with gui}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
%{?with_gui:BuildRequires:	gtk+3-devel >= 3.14.0}
BuildRequires:	gtk-doc >= 1.14
%{?with_gui:BuildRequires:	libnotify-devel}
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.14
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.44
Requires:	gtk+3 >= 3.14.0
Obsoletes:	gstreamer0.10-aravis < 0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aravis is a GLib/GObject based library for video acquisition using
Genicam cameras. It currently only implements an Ethernet camera
protocol used for industrial cameras.

%description -l pl.UTF-8
Aravis to oparta na GLib/GObject biblioteka do pobierania obrazu przy
użyciu kamer Genicam. Obecnie ma zaimplementowany tylko protokół kamer
ethernetowych używany przez kamery przemysłowe.

%package viewer
Summary:	Simple viewer of video stream acquired using Aravis
Summary(pl.UTF-8):	Prosta przeglądarka strumienia obrazu pobranego przy użyciu biblioteki Aravis
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme

%description viewer
Aravis Viewer is a simple viewer used to display video streams from
GENICAM-based Ethernet industrial cameras.

%description viewer -l pl.UTF-8
Aravis Viewer to prosta przeglądarka do wyświetlania strumieni obrazu
pobranych z ethernetowych kamer przemysłowych opartych na GENICAM.

%package devel
Summary:	Header files for Aravis library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Aravis
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	libxml2-devel >= 2.0
Requires:	zlib-devel

%description devel
Header files for Aravis library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Aravis.

%package static
Summary:	Static Aravis library
Summary(pl.UTF-8):	Statyczna biblioteka Aravis
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Aravis library.

%description static -l pl.UTF-8
Statyczna biblioteka Aravis.

%package apidocs
Summary:	API documentation for Aravis library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Aravis
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
API documentation for Aravis library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Aravis.

%package -n gstreamer-aravis
Summary:	GStreamer plugin for Aravis digital video camera acquisition library
Summary(pl.UTF-8):	Wtyczka GStreamera do biblioteki pobierania obrazu z kamer cyfrowych Aravis
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer >= 1.0
Requires:	gstreamer-plugins-base >= 1.0

%description -n gstreamer-aravis
GStreamer plugin for Aravis digital video camera acquisition
library.

%description -n gstreamer-aravis -l pl.UTF-8
Wtyczka GStreamera do biblioteki pobierania obrazu z kamer cyfrowych
Aravis.

%prep
%setup -q

%build
%meson build \
	%{!?with_gstreamer:-Dgst-plugin=disabled} \
	%{!?with_gui:-Dviewer=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name}-0.8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	viewer
%update_icon_cache hicolor

%postun	viewer
%update_icon_cache hicolor

%files -f %{name}-0.8.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS.md README.md
%attr(755,root,root) %{_bindir}/arv-camera-test-0.8
%attr(755,root,root) %{_bindir}/arv-fake-gv-camera-0.8
%attr(755,root,root) %{_bindir}/arv-tool-0.8
%attr(755,root,root) %{_libdir}/libaravis-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaravis-0.8.so.0
%{_libdir}/girepository-1.0/Aravis-0.8.typelib
%{_mandir}/man1/arv-tool-0.8.1*

%if %{with gui}
%files viewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/arv-viewer-0.8
%{_datadir}/metainfo/arv-viewer-0.8.appdata.xml
%{_desktopdir}/arv-viewer-0.8.desktop
%{_iconsdir}/hicolor/*x*/apps/aravis-0.8.png
%{_mandir}/man1/arv-viewer-0.8.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaravis-0.8.so
%{_includedir}/aravis-0.8
%{_datadir}/gir-1.0/Aravis-0.8.gir
%{_pkgconfigdir}/aravis-0.8.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaravis-0.8.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/aravis-0.8

%if %{with gstreamer}
%files -n gstreamer-aravis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstaravis.0.8.so
%endif
