%define	rname	network-manager-applet
%define	major	0
%define libname %mklibname nm-gtk %{major}
%define develname %mklibname nm-gtk -d

Name:		networkmanager-applet
Summary:	Network connection manager applet for GNOME
Version:	0.9.4.1
Release:	1
Group:		System/Configuration/Networking
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.9/%{rname}-%{version}.tar.xz
Patch0:		network-manager-applet-0.7.999-dont-start-in-kde.patch
Patch1:		network-manager-applet-0.9.4.1-format_not_a_string_literal.patch
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libiw-devel
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gnome-bluetooth-1.0)
BuildRequires:	pkgconfig(libnm-glib) >= 0.8.6.0
BuildRequires:	pkgconfig(libnm-glib-vpn) >= 0.8.6.0
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.92
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
Group:      System/Libraries
Summary:    %{summary}

%description -n %{libname}
Library from %{name}-gtk

%package -n %{develname}
Group:      Development/C
Summary:    Development libraries and header files from %{name}
Requires:   %{libname} = %{EVRD}

%description -n %{develname}
%{name}-gtk development headers and libraries.

%prep
%setup -qn %{rname}-%{version}
%apply_patches

%build
autoreconf -fi
%configure2_5x \
	--disable-static \
	--enable-more-warnings=no \
	--with-bluetooth

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print
%find_lang nm-applet

%files -f nm-applet.lang
%doc ChangeLog CONTRIBUTING
%{_bindir}/nm-connection-editor
%{_bindir}/nm-applet
%{_datadir}/applications/nm-connection-editor.desktop
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/*.png
%{_datadir}/nm-applet/*.ui
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/libnm-gtk/wifi.ui
%{_iconsdir}/hicolor/*/apps/*
%{_libdir}/gnome-bluetooth/plugins/libnma.so
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
#{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%{_sysconfdir}/gconf/schemas/nm-applet.schemas

%files -n %{libname}
%{_libdir}/libnm-gtk.so.%{major}*

%files -n %{develname}
%{_includedir}/libnm-gtk/*
%{_libdir}/libnm-gtk.so
%{_libdir}/pkgconfig/libnm-gtk.pc
