import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

BACKGROUND_COLOR = '#262f46'
PLOT_COLOR = '#5ed4bf'
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 650
API_KEY = 'Q3fkhJXjvNAhZ0F43UvxPbasinz74Dve'

window = ctk.CTk()
window.title('')
window.configure(fg_color=BACKGROUND_COLOR)
window.resizable(False, False)
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

try:
    HWND = windll.user32.GetParent(window.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(int(BACKGROUND_COLOR[5:7] + BACKGROUND_COLOR[3:5] + BACKGROUND_COLOR[1:3], 16))), sizeof(c_int))
except:
    pass

class StockSettings(ctk.CTkFrame):
    def __init__(self, parent):
        super(StockSettings, self).__init__(master=parent, fg_color='#1e2439')
        self.stock_entry = ctk.CTkEntry(self, fg_color=BACKGROUND_COLOR, border_color='white')
        self.week_label = ctk.CTkLabel(self, text='Week', text_color='white')
        self.month_label = ctk.CTkLabel(self, text='Month', text_color='white')
        self.half_year_label = ctk.CTkLabel(self, text='6 Months', text_color='white')
        self.one_year_label = ctk.CTkLabel(self, text='1 Year', text_color='white')
        self.max_label = ctk.CTkLabel(self, text='Max', text_color=PLOT_COLOR)

        self.week_label.place(x=WINDOW_WIDTH-300, y=14)
        self.month_label.place(x=WINDOW_WIDTH-240, y=14)
        self.half_year_label.place(x=WINDOW_WIDTH-180, y=14)
        self.one_year_label.place(x=WINDOW_WIDTH-110, y=14)
        self.max_label.place(x=WINDOW_WIDTH-50, y=14)
        self.stock_entry.place(x=10, y=14)

        # Bind click events to the change_color function
        self.week_label.bind("<Button-1>", lambda event, label=self.week_label: self.change_color(label))
        self.month_label.bind("<Button-1>", lambda event, label=self.month_label: self.change_color(label))
        self.half_year_label.bind("<Button-1>", lambda event, label=self.half_year_label: self.change_color(label))
        self.one_year_label.bind("<Button-1>", lambda event, label=self.one_year_label: self.change_color(label))
        self.max_label.bind("<Button-1>", lambda event, label=self.max_label: self.change_color(label))

        self.stock_entry.bind('<Return>', self.process_data)

        self.place(relx=0, rely=0.92, relwidth=1)

    def display_graph(self, time_period):
        company_name = self.stock_entry.get()

        msft = yf.Ticker(company_name)

        # get all stock info
        if time_period == '5d':
            hist = msft.history(period="5d").reset_index()
        elif time_period == 'max':
            hist = msft.history(period="max").reset_index()
        elif time_period == '1mo':
            hist = msft.history(period="1mo").reset_index()
        elif time_period == '6mo':
            hist = msft.history(period="6mo").reset_index()
        elif time_period == '1y':
            hist = msft.history(period="1y").reset_index()
        hist['Date'] = pd.to_datetime(hist['Date'])
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')

        try:
            self.canvas.get_tk_widget().pack_forget()

        except:
            pass

        fig = Figure(figsize=(18, 7),
                     dpi=100, facecolor=BACKGROUND_COLOR)
        plot1 = fig.add_subplot(111)
        # plot1.xaxis.set_major_formatter(AutoDateFormatter(AutoDateLocator()))
        plot1.plot(hist['Date'], hist['High'], color=PLOT_COLOR)
        plot1.set_facecolor(BACKGROUND_COLOR)
        plot1.tick_params(axis='y', colors=PLOT_COLOR)
        plot1.tick_params(axis='x', colors='white')
        plot1.tick_params(axis='x', rotation=45)  # Adjust rotation as needed
        plot1.xaxis.set_major_locator(plt.MaxNLocator(10))
        self.canvas = FigureCanvasTkAgg(fig,
                                        master=window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def process_data(self, event):
        if self.week_label.cget('text_color') == PLOT_COLOR:
            self.display_graph('5d')
        elif self.month_label.cget('text_color') == PLOT_COLOR:
            self.display_graph('1mo')
        elif self.half_year_label.cget('text_color') == PLOT_COLOR:
            self.display_graph('6mo')
        elif self.one_year_label.cget('text_color') == PLOT_COLOR:
            self.display_graph('1y')
        elif self.max_label.cget('text_color') == PLOT_COLOR:
            self.display_graph('max')

    def change_color(self, clicked_label):
        # Reset the color of all labels to white
        for label in [self.week_label, self.month_label, self.half_year_label, self.one_year_label, self.max_label]:
            label.configure(text_color='white')
        if clicked_label.cget('text') == 'Max':
            self.display_graph('max')
        elif clicked_label.cget('text') == '1 Year':
            self.display_graph('1y')
        elif clicked_label.cget('text') == '6 Months':
            self.display_graph('6mo')
        elif clicked_label.cget('text') == 'Month':
            self.display_graph('1mo')
        elif clicked_label.cget('text') == 'Week':
            self.display_graph('5d')

        # Change the color of the clicked label to green
        clicked_label.configure(text_color=PLOT_COLOR)

stock_settings = StockSettings(window)

window.mainloop()
