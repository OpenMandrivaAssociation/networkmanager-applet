%define url_ver %(echo %{version} | cut -d. -f1,2)

%define	rname	network-manager-applet
%define	api	1.0
%define	major	0
%define libname %mklibname nm-gtk %{major}
%define girname %mklibname nmgtk-gir %{api}
%define devname %mklibname nm-gtk -d

Name:		networkmanager-applet
Summary:	Network connection manager applet for GNOME
Version:	0.9.8.2
Release:	7
Group:		System/Configuration/Networking
License:	GPLv2+
Url:		http://www.gnome.org/projects/NetworkManager/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/%{url_ver}/%{rname}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libiw-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libnm-glib) >= 0.8.6.0
BuildRequires:	pkgconfig(libnm-glib-vpn) >= 0.8.6.0
BuildRequires:	pkgconfig(libnm-util)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.92
BuildRequires:  pkgconfig(libsecret-1)
Requires:	networkmanager

%description
Network-manager-applet is a system tray applet which lets you easily
connect to different networks. It is created for GNOME's notification area
but it also works for other desktop environments which provide a system
tray like KDE or XFCE. It displays the available networks and allows to
easily switch between them. For encrypted networks it will prompt the user
for the key/passphrase and it can optionally store them in the
gnome-keyring.

%package -n %{libname}
Group:		System/Libraries
Summary:	%{summary}

%description -n %{libname}
Library from %{name}-gtk.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	Development libraries and header files from %{name}
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}

%description -n %{devname}
%{name}-gtk development headers and libraries.

%prep
%setup -qn %{rname}-%{version}
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--enable-more-warnings=no \
	--with-bluetooth

%make

%install
%makeinstall_std
%find_lang nm-applet

%files -f nm-applet.lang
%doc ChangeLog CONTRIBUTING
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_bindir}/nm-connection-editor
%{_bindir}/nm-applet
%{_libdir}/gnome-bluetooth/plugins/libnma.so
%{_libexecdir}/nm-applet-migration-tool
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/*.png
%{_datadir}/nm-applet/*.ui
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/libnm-gtk/wifi.ui
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/nm-applet.1*
%{_mandir}/man1/nm-connection-editor.1*

%files -n %{libname}
%{_libdir}/libnm-gtk.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/NMGtk-%{api}.typelib

%files -n %{devname}
%{_includedir}/libnm-gtk/*
%{_libdir}/libnm-gtk.so
%{_libdir}/pkgconfig/libnm-gtk.pc
%{_datadir}/gir-1.0/NMGtk-%{api}.gir
