import sys
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon
from networkx import draw, Graph, draw_networkx_nodes, spring_layout, draw_networkx_edges, \
    get_edge_attributes, draw_networkx_edge_labels
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from Py_files.prepare_data import prepare_graph, Dijkstra_algo
from Py_files.mainWindow import Ui_MainWindow


class Canvas(FigureCanvas):
    def __init__(self, dictio, path_vertices=None):
        """The class that plot the graph"""
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=190)  # add a subplot
        super().__init__(fig)
        g = Graph(dictio)  # graph constructor
        pos = spring_layout(g)
        for i in dictio.keys():
            for j in dictio[i]:
                g.add_edge(i, j, weight=dictio[i][j])
        draw(g, pos=pos, with_labels=True, node_color='b', edge_color='b')  # draw the graph with a certain color
        labels = get_edge_attributes(g, 'weight')
        draw_networkx_edge_labels(g, pos=pos, edge_labels=labels, font_color="black")
        if path_vertices:  # if path was provided
            # draw vertices with different color
            draw_networkx_nodes(g, pos=pos, nodelist=path_vertices, node_color='r')
            edges = []  # to store edges list
            for i in range(len(path_vertices) - 1):
                tup = (path_vertices[i], path_vertices[i + 1])  # tuple of vertices linked by edge
                edges.append(tup)  # append to edges list
            draw_networkx_edges(g, pos=pos, edgelist=edges, edge_color='r')  # draw edges
        self.ax.plot()  # show the plot in widget


class main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Dijkstra")  # Our window's title
        self.setWindowIcon(QIcon("icons/iconPro.png"))
        self.layout = QVBoxLayout(self.widget)  # creating a box layout
        self.toolbar()  # Creation of tool bar
        self.i = 0  # A counter to keep track of widget adding

    def closeEvent(self, event):
        if self.i > 0:  # If we had  a plot in the file
            ms = "Do you want to save  the plot  before quitting ?"
            answer = QMessageBox.question(self, "Exit before save  !", ms,
                                           QMessageBox.Yes, QMessageBox.No)

            if answer == QMessageBox.Yes:  # If we click on yes we save file and quit
                self.saveFile()
                event.accept()
            if answer == QMessageBox.No:  # If No was clicked we quit
                event.accept()
        else:  # else we quit directly
            event.accept()

    def update(self, char):
        # this method the widget with chart in every call
        if self.i == 0:
            # if we were ploting for the first time
            # we just embed the plot in our widget
            self.layout.addWidget(char)
            self.i += 1
            self.old = char  # this variable stores the current plot in widget
        else:
            # We remove the previous plot and add the new one
            self.layout.removeWidget(self.old)
            self.layout.addWidget(char)
            self.old = char

    def toolbar(self):
        # the method that creates a tool bar and its actions
        self.tool = self.addToolBar("toolBar")
        addData = QAction(QIcon("icons/q4.png"), "Add", self)  # data button
        addData.setShortcut('Ctrl+A')  # its shortcut
        addData.triggered.connect(self.browseFiles)  # What we are calling if it were triggered

        self.showpath = QAction(QIcon("icons/icon4.png"), "Show Shortest Path", self)
        #self.showpath.setIconText("Add Data File")
        self.showpath.setEnabled(0)
        self.showpath.setStatusTip("Show shortest path using Dijkstra algorithm")
        self.showpath.setShortcut("Ctrl+Q")
        self.showpath.triggered.connect(self.plotGraph)

        self.save = QAction(QIcon("icons/icon3.jpg"), "Save File", self)
        self.save.setEnabled(0)
        self.save.setStatusTip("Save figure to device")
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.saveFile)
        # Add created actions to tool bar
        self.tool.addAction(addData)
        self.tool.addAction(self.save)
        self.tool.addAction(self.showpath)

    def browseFiles(self):
        """The method that opens files to select data file"""
        self.filename, _ = QFileDialog.getOpenFileName(self, "Add Data File", "", "Excel Files (*.xlsx);")
        if self.filename:  # if a file was selected
            load = prepare_graph(self.filename)  # make data in it as a dictionary
            if load != -1:  # If file contains accurate data
                self.vertices = load[1]
                self.graph = load[0]
                # update Graph
                self.update(Canvas(self.graph))  # Plot it in widget
                if load[2]:
                    self.showpath.setEnabled(0)
                    ne = QMessageBox()
                    ne.setWindowTitle("Attention !")  # title
                    ne.setText("Provided Excel file contains negative weights!")  # Text in MessageBox
                    ne.setWindowIcon(QIcon("icons/icon5.png"))  # Icon
                    ne.setIcon(QMessageBox.Warning)
                    ne.setStandardButtons(QMessageBox.Ok)
                    ne.setDefaultButton(QMessageBox.Ok)
                    ne.setDetailedText("The graph you provided contains negative weights ,"
                                       "because Dijkstra algorithm can not operate on graphs"
                                       " with negative weights !")  # details text
                    ne.exec_()
                    self.save.setEnabled(1)
                else:
                    self.save.setEnabled(1)
                    self.showpath.setEnabled(1)


            else:  # If not show a MessageBox
                box = QMessageBox()  # its instance
                box.setWindowTitle("Attention !")  # title
                box.setText("Provided Excel file contains inaccurate data !")  # Text in MessageBox
                box.setWindowIcon(QIcon("icons/icon5.png"))  # Icon
                box.setIcon(QMessageBox.Warning)
                box.setStandardButtons(QMessageBox.Ok)
                box.setDefaultButton(QMessageBox.Ok)
                box.setDetailedText("Please remember that the excel file should contain"
                                    " a matrix like data , so it will be visualized within "
                                    " the main window!")  # details text
                x = box.exec_()

    def plotGraph(self):
        start_v = self.fromVertexLineEdit.text()  # We get the starting vertex
        end_v = self.toVertexLineEdit.text()  # We get the ending vertex
        self.label_1.setText("")
        self.label_2.setText("")
        if start_v in self.vertices:
            if end_v in self.vertices:
                # if both from  and to vertices are present
                # we show the shortest path using Dijkstra
                dist_path = Dijkstra_algo(self.graph, start_v, end_v)  # shortest path and distance
                self.shortest = dist_path[0]  # get shortest path
                self.update(Canvas(self.graph, self.shortest))  # update our graph
                min_cost = dist_path[1]
                if end_v == start_v:
                    min_cost = 0
                al = f"THE MINIMUM DISTANCE TO GO FROM  {start_v} TO {end_v} IS : {min_cost} ."
                if min_cost == float("inf"):
                    al = f"THERE IS NO PATH FROM {start_v} TO {end_v} ."

                self.label_3.setText(al)
                self.label_3.adjustSize()

        if start_v not in self.vertices:
            self.label_1.setText("Non-existent Vertex !")
            self.label_1.adjustSize()

        if end_v not in self.vertices:
            self.label_2.setText("Non-existent Vertex !")
            self.label_2.adjustSize()

    def saveFile(self):
        # To save our plot
        self.filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Format (*.png);")
        if self.filePath:  # if file location is present
            plt.savefig(self.filePath)  # Save in that location


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = main()
    gui.show()
    sys.exit(app.exec_())
