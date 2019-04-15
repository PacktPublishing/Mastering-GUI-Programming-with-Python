import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtChart as qtch

from collections import deque
import psutil


class DiskUsageChartView(qtch.QChartView):

    chart_title = 'Disk Usage by Partition'

    def __init__(self):
        super().__init__()
        # Create chart
        chart = qtch.QChart(title=self.chart_title)
        self.setChart(chart)

        # Create series
        series = qtch.QBarSeries()
        chart.addSeries(series)

        # add bar sets
        bar_set = qtch.QBarSet('Percent Used')
        series.append(bar_set)

        # Get the data
        partitions = []
        for part in psutil.disk_partitions():
            if 'rw' in part.opts.split(','):
                partitions.append(part.device)
                usage = psutil.disk_usage(part.mountpoint).percent
                bar_set.append(usage)

        # Create Axis
        x_axis = qtch.QBarCategoryAxis()
        x_axis.append(partitions)
        chart.setAxisX(x_axis)
        series.attachAxis(x_axis)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 100)
        chart.setAxisY(y_axis)
        series.attachAxis(y_axis)

        # Add labels
        series.setLabelsVisible(True)


class CPUUsageView(qtch.QChartView):

    num_data_points = 500
    chart_title = "CPU Utilization"

    def __init__(self):
        super().__init__()

        # create chart
        chart = qtch.QChart(title=self.chart_title)
        self.setChart(chart)

        # series
        self.series = qtch.QSplineSeries(name="Percentage")
        chart.addSeries(self.series)

        # Create data container
        self.data = deque(
            [0] * self.num_data_points, maxlen=self.num_data_points)
        self.series.append([
            qtc.QPoint(x, y)
            for x, y in enumerate(self.data)
        ])

        # CPU Axes
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, self.num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 100)
        chart.setAxisX(x_axis, self.series)
        chart.setAxisY(y_axis, self.series)

        # Appearance tweaks
        self.setRenderHint(qtg.QPainter.Antialiasing)

        # configure timer
        self.timer = qtc.QTimer(
            interval=200, timeout=self.refresh_stats)
        self.timer.start()

    def refresh_stats(self):
        usage = psutil.cpu_percent()
        self.data.append(usage)
        new_data = [
            qtc.QPoint(x, y)
            for x, y in enumerate(self.data)]
        self.series.replace(new_data)

    def keyPressEvent(self, event):
        keymap = {
            qtc.Qt.Key_Up: lambda: self.chart().scroll(0, -10),
            qtc.Qt.Key_Down: lambda: self.chart().scroll(0, 10),
            qtc.Qt.Key_Right: lambda: self.chart().scroll(-10, 0),
            qtc.Qt.Key_Left: lambda: self.chart().scroll(10, 0),
            qtc.Qt.Key_Greater: self.chart().zoomIn,
            qtc.Qt.Key_Less: self.chart().zoomOut,
        }
        callback = keymap.get(event.key())
        if callback:
            callback()


class MemoryChartView(qtch.QChartView):

    chart_title = "Memory Usage"
    num_data_points = 50

    def __init__(self):
        super().__init__()

        ################
        # Create Chart #
        ################

        # Create qchart object
        chart = qtch.QChart(title=self.chart_title)
        self.setChart(chart)

        # Setup series
        series = qtch.QStackedBarSeries()
        chart.addSeries(series)
        self.phys_set = qtch.QBarSet("Physical")
        self.swap_set = qtch.QBarSet("Swap")
        series.append(self.phys_set)
        series.append(self.swap_set)

        # Setup Data
        self.data = deque(
            [(0, 0)] * self.num_data_points,
            maxlen=self.num_data_points)
        for phys, swap in self.data:
            self.phys_set.append(phys)
            self.swap_set.append(swap)

        # Setup Axes
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, self.num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 100)
        chart.setAxisX(x_axis, series)
        chart.setAxisY(y_axis, series)

        # Start refresh timer
        self.timer = qtc.QTimer(
            interval=1000, timeout=self.refresh_stats)
        self.timer.start()

        ###################
        # Style the chart #
        ###################
        chart.setAnimationOptions(qtch.QChart.AllAnimations)

        chart.setAnimationEasingCurve(
            qtc.QEasingCurve(qtc.QEasingCurve.OutBounce))
        chart.setAnimationDuration(1000)

        # Add shadow around the chart area
        chart.setDropShadowEnabled(True)

        # Set the theme
        chart.setTheme(qtch.QChart.ChartThemeBrownSand)

        # Configure a background brush
        gradient = qtg.QLinearGradient(
            chart.plotArea().topLeft(), chart.plotArea().bottomRight())
        gradient.setColorAt(0, qtg.QColor("#333"))
        gradient.setColorAt(1, qtg.QColor("#660"))
        chart.setBackgroundBrush(qtg.QBrush(gradient))

        # Background Pen draws a border around the chart
        chart.setBackgroundPen(qtg.QPen(qtg.QColor('black'), 5))

        # Set title font and brush
        chart.setTitleBrush(
            qtg.QBrush(qtc.Qt.white))
        chart.setTitleFont(qtg.QFont('Impact', 32, qtg.QFont.Bold))

        # Set axes fonts and brushes
        axis_font = qtg.QFont('Mono', 16)
        axis_brush = qtg.QBrush(qtg.QColor('#EEF'))
        y_axis.setLabelsFont(axis_font)
        y_axis.setLabelsBrush(axis_brush)

        # Grid lines
        grid_pen = qtg.QPen(qtg.QColor('silver'))
        grid_pen.setDashPattern([1, 1, 0, 1])
        x_axis.setGridLinePen(grid_pen)
        y_axis.setGridLinePen(grid_pen)
        y_axis.setTickCount(11)

        #Shades
        y_axis.setShadesVisible(True)
        y_axis.setShadesColor(qtg.QColor('#884'))

        # Styling the legend
        legend = chart.legend()

        # Background
        legend.setBackgroundVisible(True)
        legend.setBrush(
            qtg.QBrush(qtg.QColor('white')))

        # Font
        legend.setFont(qtg.QFont('Courier', 14))
        legend.setLabelColor(qtc.Qt.darkRed)

        # Markers
        legend.setMarkerShape(qtch.QLegend.MarkerShapeCircle)


    def refresh_stats(self):
        phys = psutil.virtual_memory()
        swap = psutil.swap_memory()
        total_mem = phys.total + swap.total
        phys_pct = (phys.used / total_mem) * 100
        swap_pct = (swap.used / total_mem) * 100

        self.data.append(
            (phys_pct, swap_pct))
        for x, (phys, swap) in enumerate(self.data):
            self.phys_set.replace(x, phys)
            self.swap_set.replace(x, swap)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        tabs = qtw.QTabWidget()
        self.setCentralWidget(tabs)

        #########################################
        # Partition Usage as a static bar chart #
        #########################################

        disk_usage_view = DiskUsageChartView()
        tabs.addTab(disk_usage_view, "Disk Usage")

        #############################
        # CPU usage as a line chart #
        #############################

        cpu_view = CPUUsageView()
        tabs.addTab(cpu_view, "CPU Usage")

        #####################################
        # CPU Time Percent as a stacked bar #
        #####################################
        cpu_time_view = MemoryChartView()
        tabs.addTab(cpu_time_view, "Memory Usage")

        # End main UI code
        self.show()



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
