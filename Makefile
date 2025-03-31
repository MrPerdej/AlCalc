PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
APPDIR=$(PREFIX)/share/applications
ICONDIR=$(PREFIX)/share/icons/hicolor/scalable/apps

install:
	install -Dm755 alcalc.py $(BINDIR)/alcalc
	install -Dm644 AlCalc.desktop $(APPDIR)/AlCalc.desktop
	install -Dm644 /usr/share/icons/hicolor/scalable/apps/accessories-calculator.svg $(ICONDIR)/accessories-calculator.svg

uninstall:
	rm -f $(BINDIR)/alcalc
	rm -f $(APPDIR)/AlCalc.desktop
	rm -f $(ICONDIR)/accessories-calculator.svg

.PHONY: install uninstall
