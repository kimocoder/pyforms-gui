#!/usr/bifn/python
# -*- coding: utf-8 -*-

from confapp import conf

from AnyQt                              import _api
from AnyQt.QtWidgets                    import QWidget, QVBoxLayout
from pyforms_gui.controls.control_base  import ControlBase
from pyforms_gui.basewidget             import BaseWidget


class ControlEmptyWidget(ControlBase, QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self)
        layout = QVBoxLayout()

        if _api.USED_API == _api.QT_API_PYQT5:
            layout.setContentsMargins(0,0,0,0)
        elif _api.USED_API == _api.QT_API_PYQT4:
            layout.setMargin(0)


        self.form.setLayout(layout)

        ControlBase.__init__(self, *args, **kwargs)
        self.value = kwargs.get('default', None)


    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self):
        return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        self.__clear_layout()

        if value is None or value == '':  return

        if isinstance(self._value, list):
            for w in self._value:
                if w != None and w != "": self.form.layout().removeWidget(w.form)

        if isinstance(value, list):
            for w in value:
                self.form.layout().addWidget(w.form)
                
                # The init_form should be called only for the BaseWidget
                if isinstance(w, BaseWidget) and not w._formLoaded:
                    w.init_form()
                if not hasattr(w, 'about_to_be_shown'):
                    w.about_to_be_shown = True
                    w.show()
                    del w.about_to_be_shown
        else:
            self.form.layout().addWidget(value.form)

            # The init_form should be called only for the BaseWidget
            if isinstance(value, BaseWidget) and not value._formLoaded:
                value.init_form()

            if not hasattr(value, 'about_to_be_shown'):
                value.about_to_be_shown = True
                value.show()
                del value.about_to_be_shown
        
        
    @property
    def form(self):
        return self

    def save_form(self, data, path=None):
        if self.value is not None and self.value != '':
            data['value'] = {}
            self.value.save_form(data['value'], path)
        return data

    def load_form(self, data, path=None):
        if 'value' in data and self.value is not None and self.value != '':
            self.value.load_form(data['value'], path)

    def __clear_layout(self):
        if self.form.layout() is not None:
            old_layout = self.form.layout()
            for i in reversed(range(old_layout.count())):
                old_layout.itemAt(i).widget().setParent(None)

    def show(self):
        """
        Show the control
        """
        QWidget.show(self)

    def hide(self):
        """
        Hide the control
        """
        QWidget.hide(self)
