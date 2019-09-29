%define url_ver %(echo %{version} | cut -d. -f1,2)

%define	rname network-manager-applet
%define	api 1.0

%define	major_gtk 0
%define libname_gtk %mklibname nm-gtk %{major_gtk}
%define girname_gtk %mklibname nmgtk-gir %{api}
%define devname_gtk %mklibname nm-gtk -d

%define	major_nma 0
%define libname_nma %mklibname nma %{major_nma}
%define girname_nma %mklibname nma-gir %{api}
%define devname_nma %mklibname nma -d

%bcond_with selinux

Name:		networkmanager-applet
Summary:	Network connection manager applet for GNOME
Version:	1.8.22
Release:	1
Group:		System/Configuration/Networking
License:	GPLv2+
Url:		https://www.gnome.org/projects/NetworkManager/
Source0:	https://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/%{url_ver}/%{rname}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	libiw-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(gcr-3)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libnm) >= %{url_ver}
BuildRequires:	pkgconfig(libnotify)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(mm-glib) >= 1.0.0
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.92
BuildRequires:  pkgconfig(mobile-broadband-provider-info)
%if %{with selinux}
BuildRequires:	pkgconfig(libselinux)
%endif
BuildRequires:	meson ninja

Requires:	networkmanager >= 1.0.6

%description
Network-manager-applet is a system tray applet which lets you easily
connect to different networks. It is created for GNOME's notification area
but it also works for other desktop environments which provide a system
tray like KDE or XFCE. It displays the available networks and allows to
easily switch between them. For encrypted networks it will prompt the user
for the key/passphrase and it can optionally store them in the
gnome-keyring.

%files -f nm-applet.lang
%doc ChangeLog CONTRIBUTING
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_bindir}/nm-connection-editor
%{_bindir}/nm-applet
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/metainfo/nm-connection-editor.appdata.xml
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
#%dir %{_datadir}/nm-applet/
#%{_datadir}/nm-applet/*.png
#%{_datadir}/nm-applet/*.ui
%{_datadir}/applications/nm-applet.desktop
#%{_datadir}/libnm-gtk/wifi.ui
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/nm-applet.1*
%{_mandir}/man1/nm-connection-editor.1*

#----------------------------------------------------------------------

%package -n %{libname_nma}
Group:		System/Libraries
Summary:	%{summary}
Requires:	mobile-broadband-provider-info
Obsoletes:	%{libname_gtk} < %{EVRD}

%description -n %{libname_nma}
Library from %{name}-nma.

%files -n %{libname_nma}
%{_libdir}/libnma.so.%{major_nma}*

#----------------------------------------------------------------------

%package -n %{girname_nma}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Obsoletes:	%{girname_gtk} < %{EVRD}

%description -n %{girname_nma}
GObject Introspection interface description for %{name}.

%files -n %{girname_nma}
%{_libdir}/girepository-1.0/NMA-%{api}.typelib

#----------------------------------------------------------------------

%package -n %{devname_nma}
Group:		Development/C
Summary:	Development libraries and header files from %{name}
Requires:	%{libname_nma} = %{EVRD}
Requires:	%{girname_nma} = %{EVRD}
Obsoletes:	%{devname_gtk} < %{EVRD}

%description -n %{devname_nma}
%{name}-nma development headers and libraries.

%files -n %{devname_nma}
%doc %{_datadir}/gtk-doc/html/libnma/
%{_includedir}/libnma/*
%{_libdir}/libnma.so
%{_libdir}/pkgconfig/libnma.pc
%{_datadir}/gir-1.0/NMA-%{api}.gir

#----------------------------------------------------------------------

%prep
%autosetup -p1 -n %{rname}-%{version}
%meson \
%if %{without selinux}
	-Dselinux=false \
%endif

%build
%ninja_build -C build

%install
%ninja_install -C build

# locales
%find_lang nm-applet

