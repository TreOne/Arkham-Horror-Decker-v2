import os
import codecs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from classes import constants, ui_util
from classes.logger import log
from classes.app import get_app
import datetime


class About(QDialog):
    """Окно 'О программе'"""

    ui_path = os.path.join('about')

    def __init__(self):
        QDialog.__init__(self)

        ui_util.load_ui(self, self.ui_path)
        ui_util.init_ui(self)

        create_text = 'Create &amp; Edit Amazing Videos and Movies'
        description_text = 'OpenShot Video Editor 2.x is the next generation of the award-winning <br/>OpenShot video editing platform.'
        learnmore_text = 'Learn more'
        copyright_text = 'Copyright &copy; %(begin_year)s-%(current_year)s' % {'begin_year': '2008', 'current_year': str(datetime.datetime.today().year) }
        about_html = '<html><head/><body><hr/><p align="center"><span style=" font-size:10pt; font-weight:600;">%s</span></p><p align="center"><span style=" font-size:10pt;">%s </span><a href="https://www.openshot.org/%s?r=about-us"><span style=" font-size:10pt; text-decoration: none; color:#55aaff;">%s</span></a><span style=" font-size:10pt;">.</span></p></body></html>' % (create_text, description_text, "constants.website_language()", learnmore_text)
        company_html = '<html><head/><body style="font-size:11pt; font-weight:400; font-style:normal;">\n<hr />\n<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600;">%s </span><a href="http://www.openshotstudios.com?r=about-us"><span style=" font-size:10pt; font-weight:600; text-decoration: none; color:#55aaff;">OpenShot Studios, LLC<br /></span></a></p></body></html>' % (copyright_text)

        # Set description and company labels
        self.lblAboutDescription.setText(about_html)
        self.lblAboutCompany.setText(company_html)

        # set events handlers
        self.btnlicense.clicked.connect(self.load_license)

        # Init some variables
        self.txtversion.setText("Версия: %s" % constants.VERSION)
        self.txtversion.setAlignment(Qt.AlignCenter)

    def load_license(self):
        """ Load License of the project """
        log.info('License screen has been opened')
        windo = License()
        windo.exec_()


class License(QDialog):
    """ License Dialog """

    ui_path = os.path.join('license')

    def __init__(self):
        # Create dialog class
        QDialog.__init__(self)

        # Load UI from designer
        ui_util.load_ui(self, self.ui_path)

        # Init Ui
        ui_util.init_ui(self)

        # Init license
        with open(os.path.join(constants.RESOURCES_PATH, 'license.txt'), 'r') as my_license:
            text = my_license.read()
            self.textBrowser.append(text)

        # Scroll to top
        cursor = self.textBrowser.textCursor()
        cursor.setPosition(0)
        self.textBrowser.setTextCursor(cursor)
