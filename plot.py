import pyqtgraph as pg

class graph():
    def __init__(self,pens = [{"color":(255,0,0),"name":"NaN"}] , moving=False , n_data=50, x_name="" , y_name="" , title=""):
        #When showing a moving graph n_data decides the no. of elements shown
        self.moving = moving
        self.n_data = n_data

        # Creating Graph Widget
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground((0,0,0))

        # Making plots
        self.plots=[]
        for pen in pens :
            self.plots.append({
                "x" : [],
                "y" : [],
                "pen" : pg.mkPen(color=pen["color"],width=2),
                "name" : pen["name"]
            })

        # Add Title
        self.graphWidget.setTitle(title, color="w", size="5pt")

        # Add Axis Labels
        styles = {"color": "#FFFFFF", "font-size": "15px"}
        self.graphWidget.setLabel("left", y_name, **styles)
        self.graphWidget.setLabel("bottom", x_name, **styles)

    def update(self,x,y):
        for i,plot in enumerate(self.plots) :
            if y[i]:
                plot["y"].append(y[i])
                plot["x"].append(x)
            if len(plot["x"]) == 1 :
                self.graphWidget.addLegend()
                plot["data_line"] = self.graphWidget.plot(plot["x"],plot["y"], pen=plot["pen"],name=plot["name"])
            if self.moving and len(plot["x"]) > self.n_data:
                plot["y"] = plot["y"][1:]  # Remove the first
                plot["x"] = plot["x"][1:]  # Remove the first

            plot["data_line"].setData(plot["x"], plot["y"])  # Update the data.
