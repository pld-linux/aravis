#
# Conditional build:
%bcond_without	gui		# Viewer application
%bcond_without	gstreamer	# alias to disable both GStreamer plugins
%bcond_without	gstreamer1	# GStreamer 1 plugin
%bcond_without	gstreamer0_10	# GStreamer 0.10 plugin
#
%if %{without gstreamer}
%undefine	with_gstreamer1
%undefine	with_gstreamer0_10
%endif
Summary:	Aravis digital video camera acquisition library
Summary(pl.UTF-8):	Aravis - biblioteka do pobierania obrazu z kamer cyfrowych
Name:		aravis
Version:	0.3.8
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/aravis/0.3/%{name}-%{version}.tar.xz
# Source0-md5:	a09325d614fa4ffa9d7227489fb89a25
URL:		https://wiki.gnome.org/Projects/Aravis
BuildRequires:	appstream-glib-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	gobject-introspection-devel >= 0.10.0
%if %{with gstreamer1} || %{with gui}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
%if %{with gstreamer0_10}
BuildRequires:	gstreamer0.10-devel >= 0.10
BuildRequires:	gstreamer0.10-plugins-base-devel >= 0.10
%endif
%{?with_gui:BuildRequires:	gtk+3-devel >= 3.14.0}
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.31.2
%{?with_gui:BuildRequires:	libnotify-devel}
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig >= 1:0.14
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.14.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aravis is a GLib/GObject based library for video acquisition using
Genicam cameras. It currently only implements an Ethernet camera
protocol used for industrial cameras.

%description -l pl.UTF-8
Aravis to oparta na GLib/GObject biblioteka do pobierania obrazu przy
użyciu kamer Genicam. Obecnie ma zaimplementowany tylko protokół
kamer ethernetowych używany przez kamery przemysłowe.

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
Requires:	glib2-devel >= 4.0
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

%description apidocs
API documentation for Aravis library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Aravis.

%package -n gstreamer0.10-aravis
Summary:	GStreamer 0.10 plugin for Aravis digital video camera acquisition library
Summary(pl.UTF-8):	Wtyczka GStreamera 0.10 do biblioteki pobierania obrazu z kamer cyfrowych Aravis
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer0.10 >= 0.10
Requires:	gstreamer0.10-plugins-base >= 0.10

%description -n gstreamer0.10-aravis
GStreamer 0.10 plugin for Aravis digital video camera acquisition
library.

%description -n gstreamer0.10-aravis -l pl.UTF-8
Wtyczka GStreamera 0.10 do biblioteki pobierania obrazu z kamer
cyfrowych Aravis.

%package -n gstreamer-aravis
Summary:	GStreamer 1 plugin for Aravis digital video camera acquisition library
Summary(pl.UTF-8):	Wtyczka GStreamera 1 do biblioteki pobierania obrazu z kamer cyfrowych Aravis
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer >= 1.0
Requires:	gstreamer-plugins-base >= 1.0

%description -n gstreamer-aravis
GStreamer 1 plugin for Aravis digital video camera acquisition
library.

%description -n gstreamer-aravis -l pl.UTF-8
Wtyczka GStreamera 1 do biblioteki pobierania obrazu z kamer cyfrowych
Aravis.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_gstreamer1:--disable-gst-plugin} \
	%{!?with_gstreamer0_10:--disable-gst-0.10-plugin} \
	%{!?with_gui:--disable-viewer} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-*/libgstaravis-0.4.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaravis-0.4.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc

%find_lang %{name}-0.4

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	viewer
%update_icon_cache hicolor

%postun	viewer
%update_icon_cache hicolor

%files -f %{name}-0.4.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/arv-fake-gv-camera-0.4
%attr(755,root,root) %{_bindir}/arv-tool-0.4
%attr(755,root,root) %{_libdir}/libaravis-0.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaravis-0.4.so.0
%{_libdir}/girepository-1.0/Aravis-0.4.typelib

%if %{with gui}
%files viewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/arv-viewer
%{_datadir}/aravis-0.4
%{_datadir}/appdata/arv-viewer.appdata.xml
%{_desktopdir}/arv-viewer.desktop
%{_iconsdir}/hicolor/*/apps/aravis.png
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaravis-0.4.so
%{_includedir}/aravis-0.4
%{_datadir}/gir-1.0/Aravis-0.4.gir
%{_pkgconfigdir}/aravis-0.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaravis-0.4.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/aravis-0.4

%if %{with gstreamer0_10}
%files -n gstreamer0.10-aravis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-0.10/libgstaravis-0.4.so
%endif

%if %{with gstreamer1}
%files -n gstreamer-aravis
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstaravis-0.4.so
%endif
