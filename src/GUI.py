import slint

components = slint.load_file('slint-gui/app-window.slint', style='cosmic')
main_window = components.MainWindow()
main_window.run()
