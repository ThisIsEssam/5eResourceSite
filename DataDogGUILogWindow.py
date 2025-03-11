#!/usr/bin/env python
import datetime
import json
import os
import pprint
import sys

import pytz
import requests
import tzlocal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *


class DataDogGUIFailSaveWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUIFailSaveWindow, self).__init__(parent)
        self.resize(200, 200)
        self.setWindowTitle("Save Failed")
        layout = QVBoxLayout()
        self.label = QLabel("An Error occurred when trying to export records")
        layout.addWidget(self.label)
        self.setLayout(layout)


class DataDogGUISuccessSaveWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUISuccessSaveWindow, self).__init__(parent)
        self.resize(200, 200)
        self.setWindowTitle("Successfully Saved!")
        layout = QVBoxLayout()
        self.label = QLabel("Successfully saved to /Users/USERNAME/Documents/DataDogLogs.txt")
        layout.addWidget(self.label)
        self.setLayout(layout)


class DataDogGUILogWindow(QWidget):
    def __init__(self, parent=None):
        super(DataDogGUILogWindow, self).__init__(parent)
        self.saveWindowSuccess = None
        self.saveWindowFail = None
        self.resize(700, 700)
        self.setFixedSize(700, 700)
        self.setWindowTitle("DataDogs Log Tool")

        # Font
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        # User Id Label
        userIdLabel = QLabel(self)
        userIdLabel.setText("User ID")
        userIdLabel.setFont(font)
        userIdLabel.move(10, 30)

        # From Date Label
        fromDateLabel = QLabel(self)
        fromDateLabel.setText("From")
        fromDateLabel.setFont(font)
        fromDateLabel.move(10, 60)

        # From Date Picker
        self.fromDatePicker = QDateTimeEdit(self, calendarPopup=True, displayFormat="yyyy-MM-dd HH:mm")
        self.fromDatePicker.setFixedWidth(230)
        self.fromDatePicker.setDateTime(datetime.datetime.now() - datetime.timedelta(hours=1))
        self.fromDatePicker.move(70, 50)

        # To Date label
        toDateLabel = QLabel(self)
        toDateLabel.setText("To")
        toDateLabel.setFont(font)
        toDateLabel.move(10, 90)

        # To Date Picker
        self.toDatePicker = QDateTimeEdit(self, calendarPopup=True, displayFormat="yyyy-MM-dd HH:mm")
        self.toDatePicker.setFixedWidth(230)
        self.toDatePicker.setDateTime(datetime.datetime.now())
        self.toDatePicker.move(70, 80)

        # Service Label
        serviceLabel = QLabel(self)
        serviceLabel.setText("Service")
        serviceLabel.setFont(font)
        serviceLabel.move(10, 120)

        # Service Combo
        self.serviceListChosen = []
        self.serviceCombo = QListWidget(self)
        self.serviceCombo.setFixedWidth(220)
        self.serviceCombo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.serviceCombo.resize(200, 70)
        self.serviceCombo.itemSelectionChanged.connect(
            lambda: get_services(self.serviceListChosen, self.serviceCombo.currentItem().text()))
        self.serviceCombo.addItem("mobile")
        self.serviceCombo.addItem("api")
        self.serviceCombo.addItem("identity")
        self.serviceCombo.addItem("identity-provider")
        self.serviceCombo.addItem("co.cardata.mileage")
        self.serviceCombo.addItem("driver-resource-api")
        self.serviceCombo.addItem("reporting-api")
        self.serviceCombo.addItem("mileage-resource-api")
        self.serviceCombo.addItem("rules-engine-api")
        self.serviceCombo.addItem("consumer")
        self.serviceCombo.addItem("cloud")
        self.serviceCombo.addItem("company-resource-api")
        self.serviceCombo.addItem("user-resource-api")
        self.serviceCombo.addItem("master-task")
        self.serviceCombo.addItem("rpt")
        self.serviceCombo.addItem("mail-service-api")
        self.serviceCombo.addItem("banking-resource-api")
        self.serviceCombo.addItem("vehicle-resource-api")
        self.serviceCombo.addItem("metabase")
        self.serviceCombo.addItem("kbb-resource-api")
        self.serviceCombo.move(75, 120)

        # Max Records Label
        maxRecordsLabel = QLabel(self)
        maxRecordsLabel.setText("Max Records")
        maxRecordsLabel.setFont(font)
        maxRecordsLabel.move(350, 60)

        # Max Records Entry
        self.maxRecordsEntry = QLineEdit(self)
        self.maxRecordsEntry.setFixedWidth(220)
        self.maxRecordsEntry.setPlaceholderText("Enter max number of records here..")
        self.maxRecordsEntry.setText("10")
        self.maxRecordsEntry.move(435, 55)

        # Status Label
        self.statusLabel = QLabel(self)
        self.statusLabel.setText("Log Status")
        self.statusLabel.setFont(font)
        self.statusLabel.move(350, 90)

        # Status Combo
        self.statusChosen = []
        self.statusCombo = QListWidget(self)
        self.statusCombo.setFixedWidth(220)
        self.statusCombo.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.statusCombo.resize(100, 70)
        self.statusCombo.itemSelectionChanged.connect(
            lambda: get_status(self.statusChosen, self.statusCombo.currentItem().text()))
        self.statusCombo.addItem("info")
        self.statusCombo.addItem("warn")
        self.statusCombo.addItem("error")
        self.statusCombo.addItem("debug")
        self.statusCombo.move(435, 90)

        # Query Checkbox
        self.queryCheck = QCheckBox(self)
        self.queryCheck.setText("Query")
        self.queryCheck.move(8, 210)
        self.queryCheck.stateChanged.connect(self.state_changed)

        # Disable Query Box

        # Query Multi-line
        self.queryEntry = QTextEdit(self)
        self.queryEntry.setFixedWidth(580)
        self.queryEntry.setFixedHeight(50)
        self.queryEntry.setDisabled(True)
        self.queryEntry.move(75, 210)

        # Environment Label
        envLabel = QLabel(self)
        envLabel.setText("Environment")
        envLabel.setFont(font)
        envLabel.move(350, 30)

        # Environment Combo Box
        self.envCombo = QComboBox(self)
        self.envCombo.setFixedWidth(232)
        self.envCombo.addItem("staging")
        self.envCombo.addItem("production")
        self.envCombo.addItem("dev")
        self.envCombo.move(430, 20)

        # Results Label
        self.resultsLabel = QLabel(self)
        self.resultsLabel.setText("Results")
        self.resultsLabel.setFont(font)
        self.resultsLabel.move(10, 270)

        # Results Table
        self.resultTable = QTableWidget(self)
        self.resultTable.move(75, 270)
        self.resultTable.resize(580, 350)
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.resultTable.itemSelectionChanged.connect(lambda: disable_export(self))
        # Submit Button
        submitButton = QPushButton(self)
        submitButton.setText("Submit Query")
        submitButton.clicked.connect(self.submit_query)
        submitButton.move(420, 655)

        self.exportButton = QPushButton(self)
        self.exportButton.setText("Export to Txt")
        self.exportButton.setDisabled(True)
        self.exportButton.clicked.connect(lambda: self.export_to_txt())
        self.exportButton.move(547, 655)

        # Next Button
        self.nextButton = QPushButton(self)
        self.nextButton.setText("Next")
        self.nextButton.move(595, 620)
        self.nextButton.clicked.connect(lambda: self.submit_query())

        # User ID Entry
        self.userIdEntry = QLineEdit(self)
        self.userIdEntry.setFixedWidth(220)
        self.userIdEntry.setPlaceholderText("Enter User ID here...")
        self.userIdEntry.move(75, 25)
        self.userIdEntry.setFocus()

        # Lat Long Label
        # self.latLongLabel = QLabel(self)
        # self.latLongLabel.setFont(font)
        # self.latLongLabel.setText("Lat/Long Table")
        # self.latLongLabel.move(10, 550)

        # Lat Long ComboBox
        # self.latLongCombo = QComboBox(self)
        # self.latLongCombo.addItem("Lat/Long in JSON")
        # self.latLongCombo.addItem("Comma Separated Or-Bar")
        # self.latLongCombo.move(100, 540)

        # Lat Long  Table
        # self.latLongTable = QTableWidget(self)
        # self.latLongTable.resize(740, 200)
        # self.latLongTable.move(10, 575)

    def state_changed(self):
        if not self.queryCheck.isChecked():
            self.queryEntry.setDisabled(True)
            self.userIdEntry.setDisabled(False)
            self.envCombo.setDisabled(False)
            self.serviceCombo.setDisabled(False)
            self.maxRecordsEntry.setDisabled(False)
            self.toDatePicker.setDisabled(False)
            self.fromDatePicker.setDisabled(False)
            self.statusCombo.setDisabled(False)
        else:
            self.queryEntry.setDisabled(False)
            self.userIdEntry.setDisabled(True)
            self.envCombo.setDisabled(True)
            self.serviceCombo.setDisabled(True)
            self.maxRecordsEntry.setDisabled(True)
            self.toDatePicker.setDisabled(True)
            self.fromDatePicker.setDisabled(True)
            self.statusCombo.setDisabled(True)

    def submit_query(self):
        # Get Values from UI

        userIdText = self.userIdEntry.text()
        fromDateTime = self.fromDatePicker.text()
        toDateTime = self.toDatePicker.text()
        maxRecords = self.maxRecordsEntry.text()
        environment = self.envCombo.currentText()

        toDateAndTime = toDateTime.split(" ")
        fromDateAndTime = fromDateTime.split(" ")

        # Access Datadog Logs
        # data dogs information set function call

        api_key1 = os.getenv('API_KEY_1')
        api_key2 = os.getenv('API_KEY_2')
        url = "https://api.us3.datadoghq.com/api/v2/logs/events/search"
        url_method = "POST"
        headers = {'Content-Type': 'application/json',
                   'DD-API-KEY': api_key1,
                   'DD-APPLICATION-KEY': api_key2}
        queryText = self.queryEntry.toPlainText()
        if self.queryCheck.isChecked():
            if queryText == "":
                payload = '{"page":{"limit":' + maxRecords + '},' \
                                                             '"filter": {"from": "' + fromDateAndTime[0] + 'T' + \
                          fromDateAndTime[1] + ':00' + get_timezone_offset() + '", "to": "' + toDateAndTime[0] + 'T' + \
                          toDateAndTime[
                              1] + ':00' + get_timezone_offset() + '", ' \
                                                                   '"query": " (@request.parameters.user_id:' + userIdText + ' || @usr.id:' + userIdText + ' || @request.parameters._user_id:' + userIdText + ' || @context.identity.user_id:' + userIdText + ') ' + status_determine(
                    self.statusChosen) + ' ' + check_box_determine(
                    self.serviceListChosen, environment) + '"}}'
            else:
                payload = queryText
        else:
            if userIdText == "":
                payload = '{"page":{"limit":' + maxRecords + '},' \
                                                             '"filter": {"from": "' + fromDateAndTime[0] + 'T' + \
                          fromDateAndTime[1] + ':00' + get_timezone_offset() + '", "to": "' + toDateAndTime[0] + 'T' + \
                          toDateAndTime[
                              1] + ':00' + get_timezone_offset() + '", ' \
                                                                   '"query": " ' + status_determine(
                    self.statusChosen) + ' ' + check_box_determine(
                    self.serviceListChosen, environment) + '"}}'
            else:
                payload = '{"page":{"limit":' + maxRecords + '},' \
                                                             '"filter": {"from": "' + fromDateAndTime[0] + 'T' + \
                          fromDateAndTime[1] + ':00' + get_timezone_offset() + '", "to": "' + toDateAndTime[0] + 'T' + \
                          toDateAndTime[
                              1] + ':00' + get_timezone_offset() + '", ' \
                                                                   '"query": " (@request.parameters.user_id:' + userIdText + ' || @usr.id:' + userIdText + ' || @request.parameters._user_id:' + userIdText + ' || @context.identity.user_id:' + userIdText + ') ' + status_determine(
                    self.statusChosen) + ' ' + check_box_determine(
                    self.serviceListChosen, environment) + '"}}'
        # '"query": " (@request.path:api/v3/trip ) -status:(info OR warn OR error) -service:(api-staging or mileage-resource-api OR rules-engine-api OR cloud OR driver-resource-api)"}}'
        response = requests.request(url_method, url, headers=headers, data=payload)
        try:
            response_json = response.json()
            populate_table(self, response_json)
        except Exception:
            if response.status_code == 429:
                error = QErrorMessage()
                error.showMessage("Error! Too many requests. Slow down")
            else:
                error = QErrorMessage()
                error.showMessage("Error! Something went wrong.")

        # Populate Query Text box
        if self.queryCheck.isChecked():
            self.queryEntry.setText(payload)
        else:
            self.queryEntry.setText(payload)

    def export_to_txt(self):
        results_list = []
        pp = pprint.PrettyPrinter(indent=4)
        counter = 0
        for i in self.resultTable.selectionModel().selectedRows():
            counter += 1
            query = self.resultTable.model().data(self.resultTable.model().index(i.row(), 1))
            query = json.loads(query)
            coordinates = self.resultTable.model().data(self.resultTable.model().index(i.row(), 2))
            data = "Export Record: " + str(counter) + '\n'
            data += "Log Date: " + self.resultTable.model().data(self.resultTable.model().index(i.row(), 0)) + "\n"
            data += "Query: \n" + pp.pformat(query) + "\n \n"
            if coordinates != "N/A":
                or_bar = coordinates.find("|")
                coordinates_one = coordinates[0:or_bar]
                data += "Lat-Long Datapoints: \n" + coordinates + "\n \n"
                data += "Google Maps Link: \nhttps://www.google.com/maps/dir/" + coordinates.replace("|",
                                                                                                     "/") + "/@" + coordinates_one + ",16z/data=!3m1!4b1!4m2!4m1!3e0?entry=ttu\n"
            data += "" \
                    "---------------------------------------------------------------------------------------------------------------------- \n"
            results_list.append(data)

        try:
            with open(file=os.path.expanduser('~/Documents/DataDogLog.txt'), mode='w') as f:
                f.writelines(results_list)
            if self.saveWindowSuccess is None:
                self.saveWindowSuccess = DataDogGUISuccessSaveWindow()
                self.saveWindowSuccess.setFixedHeight(75)
                self.saveWindowSuccess.show()
            else:
                self.saveWindowSuccess.close()
                self.saveWindowSuccess = None
        except:
            if self.saveWindowFail is None:
                self.saveWindowFail = DataDogGUIFailSaveWindow()
                self.saveWindowFail.setFixedHeight(75)
                self.saveWindowFail.show()
            else:
                self.saveWindowFail.close()
                self.saveWindowFail = None


def populate_table(self, response_json):
    columns = ["Timestamp", "Record", "Lat/Long"]
    recordList = []
    self.resultTable.setColumnCount(len(columns))
    self.resultTable.setHorizontalHeaderLabels(columns)
    header = self.resultTable.horizontalHeader()
    for record in response_json['data']:
        my_record = record['attributes']
        my_record.pop('tags')
        attributes = my_record['attributes']
        service = my_record['service']
        if service == 'mobile':
            request = attributes['request']
            if request['path'] == 'api/v3/trip':
                lat_long = get_lat_long_GPS(record)
            else:
                lat_long = "N/A"
        else:
            lat_long = "N/A"
        my_timestamp = str(my_record['timestamp'])
        year = my_timestamp[0:10]
        time = my_timestamp[11:19]
        my_timestamp = year + " " + time
        my_record = json.dumps(my_record)
        # pretty_print_data = pp.pformat(my_record)
        my_data = [my_record, my_timestamp, lat_long]
        recordList.append(my_data)
    self.resultTable.setRowCount(len(recordList))
    for i, (record, timestamp, lat_long) in enumerate(recordList):
        item_record = QTableWidgetItem(record)
        item_timestamp = QTableWidgetItem(timestamp)
        item_lat_long = QTableWidgetItem(lat_long)
        self.resultTable.setItem(i, 0, item_timestamp)
        self.resultTable.setItem(i, 1, item_record)
        self.resultTable.setItem(i, 2, item_lat_long)
    header.setSectionResizeMode(0, QHeaderView.ResizeMode(3))
    header.setSectionResizeMode(1, QHeaderView.ResizeMode(3))
    header.setSectionResizeMode(2, QHeaderView.ResizeMode(3))

    # recordList = [[]]
    #
    # for record in response_json['data']:
    #     my_record = record['attributes']
    #     my_record = str(my_record.pop('tags'))
    #     timestamp = str(record['timestamp'])
    #     record_timestamp = []
    #     record_timestamp.append(timestamp)
    #     record_timestamp.append(my_record)
    #     recordList.append(record_timestamp)
    #     self.results_list.append(my_record)
    #
    #
    # self.resultTable.setRowCount(len(recordList))
    # self.resultTable.setColumnCount(4)
    # header = self.resultTable.horizontalHeader()
    # header.setSectionResizeMode(0, QHeaderView.ResizeMode(3))
    # for i, record in enumerate(recordList):
    #     recordEntry = QTableWidgetItem(record)
    #     self.resultTable.setItem(i, 0, recordEntry)

    # if self.latLongCombo.currentText() == "Lat/Long in JSON":
    #     self.latLongTable.setRowCount(len(get_lat_long_default(response_json['data'])))
    #     self.latLongTable.setColumnCount(1)
    #     latlongHeader = self.latLongTable.horizontalHeader()
    #     latlongHeader.setSectionResizeMode(0, QHeaderView.ResizeMode(3))
    #     for i, x in enumerate(get_lat_long_default(response_json['data'])):
    #         latLong = QTableWidgetItem(x)
    #         self.latLongTable.setItem(i, 0, latLong)
    # if self.latLongCombo.currentText() == "Comma Separated Or-Bar":
    #     self.latLongTable.setRowCount(len(get_lat_long_GPS(response_json['data'])))
    #     self.latLongTable.setColumnCount(1)
    #     latlongHeader = self.latLongTable.horizontalHeader()
    #     latlongHeader.setSectionResizeMode(0, QHeaderView.ResizeMode(3))
    #     for i, x in enumerate(get_lat_long_GPS(response_json['data'])):
    #         latLong = QTableWidgetItem(x)
    #         self.latLongTable.setItem(i, 0, latLong)


def disable_export(self):
    if len(self.resultTable.selectionModel().selectedRows()) >= 1:
        self.exportButton.setDisabled(False)
    else:
        self.exportButton.setDisabled(True)


def get_services(serviceList, serviceItem):
    if serviceItem in serviceList:
        serviceList.remove(serviceItem)
    else:
        serviceList.append(serviceItem)


def get_status(statusList, statusItem):
    if statusItem in statusList:
        statusList.remove(statusItem)
    else:
        statusList.append(statusItem)


def get_lat_long_default(record):
    b = record.get("attributes")
    c = b.get("attributes")
    d = c.get("request")
    e = d.get("parameters")
    start_time = "start_time: " + str(e.get("start_time"))
    origin = "origin: " + str(e.get("origin"))
    end_time = "end_time: " + str(e.get("end_time"))
    destination = "destination: " + str(e.get("destination"))
    locations = "locations: " + str(e.get("locations"))
    latLong = start_time + ", " + origin + ", " + end_time + ", " + destination + ", " + locations
    return latLong


def get_lat_long_GPS(record):
    latLongString = ""
    b = record.get("attributes")
    c = b.get("attributes")
    d = c.get("request")
    e = d.get("parameters")
    locations = e.get("locations")
    for i in locations:
        # lat = str(i.get("latitude"))
        # long = str(i.get("longitude"))
        lat = str(round(i["latitude"], 5))
        long = str(round(i["longitude"], 5))
        latlong = lat + "," + long + "|"
        latLongString += latlong
    latLongString = latLongString[:len(latLongString) - 1]
    return latLongString


def get_timezone_offset():
    local_tz = tzlocal.get_localzone()
    local_time = datetime.datetime.now(pytz.timezone(str(local_tz))).strftime('%z')
    local_time = local_time[:3] + ":" + local_time[3:]
    return local_time


def status_determine(statusList):
    # status:(info OR warn OR error OR debug)
    list = []
    for i in statusList:
        if i == "info":
            list.append(i)
        if i == "warn":
            list.append(i)
        if i == "error":
            list.append(i)
        if i == "debug":
            list.append(i)
    statusListChosen = ' OR '.join(map(str, list))
    if not statusList:
        return ""
    else:
        return 'status:(' + statusListChosen + ')'


def check_box_determine(serviceList, environment):
    list = []
    for i in serviceList:
        if i == 'mobile':
            if environment == 'production':
                list.append('mobile')
            if environment == 'staging':
                list.append('mobile-staging')
            if environment == 'dev':
                list.append('mobile-dev')
        if i == 'api':
            if environment == 'production':
                list.append('api')
            if environment == 'staging':
                list.append('api-staging')
            if environment == 'dev':
                list.append('api-dev')
        if i == 'identity':
            if environment == 'production':
                list.append('identity-api')
            if environment == 'staging':
                list.append('identity-api-staging')
            if environment == 'dev':
                list.append('identity-api-dev')
        if i == 'identity-provider':
            if environment == 'production':
                list.append('identity-provider-api')
            if environment == 'staging':
                list.append('identity-provider-api-staging')
            if environment == 'dev':
                list.append('identity-provider-api-dev')
        if i == 'co.cardata.mileage':
            if environment == 'production':
                list.append('co.cardata.mileage')
            if environment == 'staging':
                list.append('co.cardata.mileage-staging')
            if environment == 'dev':
                list.append('co.cardata.mileage-dev')
        if i == 'driver-resource-api':
            if environment == 'production':
                list.append('driver-resource-api')
            if environment == 'staging':
                list.append('driver-resource-api-staging')
            if environment == 'dev':
                list.append('driver-resource-api-dev')
        if i == 'reporting-api':
            if environment == 'production':
                list.append('reporting-api')
            if environment == 'staging':
                list.append('reporting-api-staging')
            if environment == 'dev':
                list.append('reporting-api-dev')
        if i == 'mileage-resource-api':
            if environment == 'production':
                list.append('mileage-resource-api')
            if environment == 'staging':
                list.append('mileage-resource-api-staging')
            if environment == 'dev':
                list.append('mileage-resource-api-dev')
        if i == 'consumer':
            if environment == 'production':
                list.append('consumer')
            if environment == 'staging':
                list.append('consumer-staging')
            if environment == 'dev':
                list.append('consumer-dev')
        if i == 'cloud':
            if environment == 'production':
                list.append('cloud')
            if environment == 'staging':
                list.append('cloud-staging')
            if environment == 'dev':
                list.append('cloud-dev')
        if i == 'company-resource-api':
            if environment == 'production':
                list.append('company-resource-api')
            if environment == 'staging':
                list.append('company-resource-api-staging')
            if environment == 'dev':
                list.append('company-resource-api-dev')
        if i == 'user-resource-api':
            if environment == 'production':
                list.append('user-resource-api')
            if environment == 'staging':
                list.append('user-resource-api-staging')
            if environment == 'dev':
                list.append('user-resource-api-dev')
        if i == 'master-task':
            if environment == 'production':
                list.append('master-task')
            if environment == 'staging':
                list.append('master-task-staging')
            if environment == 'dev':
                list.append('master-task-dev')
        if i == 'rpt':
            if environment == 'production':
                list.append('rpt')
            if environment == 'staging':
                list.append('rpt-staging')
            if environment == 'dev':
                list.append('rpt-dev')
        if i == 'mail-service-api':
            if environment == 'production':
                list.append('mail-service-api')
            if environment == 'staging':
                list.append('mail-service-api-staging')
            if environment == 'dev':
                list.append('mail-service-api-dev')
        if i == 'banking-resource-api':
            if environment == 'production':
                list.append('banking-resource-api')
            if environment == 'staging':
                list.append('banking-resource-api-staging')
            if environment == 'dev':
                list.append('banking-resource-api-dev')
        if i == 'vehicle-resource-api':
            if environment == 'production':
                list.append('vehicle-resource-api')
            if environment == 'staging':
                list.append('vehicle-resource-api-staging')
            if environment == 'dev':
                list.append('vehicle-resource-api-dev')
        if i == 'metabase':
            if environment == 'production':
                list.append('metabase')
            if environment == 'staging':
                list.append('metabase-staging')
            if environment == 'dev':
                list.append('metabase-dev')
        if i == 'kbb-resource-api':
            if environment == 'production':
                list.append('kbb-resource-api')
            if environment == 'staging':
                list.append('kbb-resource-api-staging')
            if environment == 'dev':
                list.append('kbb-resource-api-dev')

    serviceListChosen = ' OR '.join(map(str, list))
    if not serviceList:
        return ""
    else:
        return 'service:(' + serviceListChosen + ')'


def main():
    app = QApplication(sys.argv)
    ex = DataDogGUILogWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
