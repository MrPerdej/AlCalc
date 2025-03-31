PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
APPDIR=$(PREFIX)/share/applications
ICONDIR=$(PREFIX)/share/icons/hicolor/scalable/apps
BUILDDIR=build
DISTDIR=dist

build:
	pyinstaller --onefile --windowed --name alcalc alcalc.py

install: build
	install -Dm755 $(DISTDIR)/alcalc $(BINDIR)/alcalc
	install -Dm644 AlCalc.desktop $(APPDIR)/AlCalc.desktop
	install -Dm644 /usr/share/icons/hicolor/scalable/apps/accessories-calculator.svg $(ICONDIR)/accessories-calculator.svg

uninstall:
	rm -f $(BINDIR)/alcalc
	rm -f $(APPDIR)/AlCalc.desktop
	rm -f $(ICONDIR)/accessories-calculator.svg

clean:
	rm -rf $(BUILDDIR) $(DISTDIR)

.PHONY: install uninstall build clean
