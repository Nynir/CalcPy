import tkinter as tk
from tkinter import ttk
from functools import partial

DEBUG = True

global darkTheme
darkTheme = True

class calculator(ttk.Frame):
	def __init__(self, parent):
		ttk.Frame.__init__(self)

		global allowed
		allowed = { "=", "+", "-", "/", "%", "*" } #Doesnt support ^

		global justEntered
		self.justEntered = tk.BooleanVar()
		self.justEntered.set(False)

		#Columns
		for index in [0,1,2,3]:
			self.columnconfigure(index=index, weight=1)
			self.rowconfigure(index=index+1, weight=1)

		self.result = tk.StringVar(value="")

		#Create
		self.setup_things()

	def verifyInput(self,key):
		if DEBUG: print("DEBUG: verifying key")

		if key.isdigit() or key in allowed:
			if DEBUG: print("DEBUG: allowed key=%s" % key)
			calculator.button_pressed(self,key)
		else:
			if DEBUG: print("DEBUG: not allowed character=%s" % key)

	def setup_things(self):
		self.label = ttk.Label(self, anchor="e", textvariable=self.result, font=("-size", 15), padding=5)
		self.label.grid(row=0, column=0, columnspan=4, sticky="ew")

		for index, key in enumerate("147C2580369=+-*/"):
			ttk.Button(self, text=key, style="Accent.TButton" if key == "=" else "TButton", command=partial(self.button_pressed, key),).grid(row=index % 4 + 1, column=index // 4, sticky="nsew", padx=2, pady=2)

	def copyPasteHandler(self,typeOf):
		if DEBUG: print("DEBUG: doing " + str(typeOf))
		if typeOf == "copy":
			self.clipboard_clear()
			text = self.result.get()
			self.clipboard_append(text)
		elif typeOf == "paste":
			clip = self.selection_get(selection='CLIPBOARD')
			if DEBUG: print("DEBUG: clipboard: " + str(clip))
			try:
				n = int(clip)
				self.result.set(self.result.get() + str(n))
			except:
				if DEBUG: print("ERROR: invalid input")

	def button_pressed(self,key):
		if key == "C":
			self.result.set("")
		elif key == "=":
			if self.result.get() == "":
				pass
			else:
				self.result.set(round(eval(self.result.get())))
				self.justEntered.set(True)
		elif key == "BackSpace":
			if DEBUG: print("button backspace")
			x = self.result.get()
			y = x[0:len(x)-1]
			self.result.set(y)
		else:
			if self.justEntered.get() == True and key not in allowed:
				self.result.set("")
				self.justEntered.set(False)
				self.result.set(self.result.get() + key)
			else:
				self.result.set(self.result.get() + key)
				self.justEntered.set(False)

if __name__ == "__main__":
	root = tk.Tk()
	root.title("CalcPy")
	root.geometry("300x300")
	root.attributes("-topmost", True)

	root.tk.call("source", "sun-valley.tcl")
	root.tk.call("set_theme", "dark")

	def change_theme():
		global darkTheme
		if DEBUG: print("DEBUG: Change theme")
		if darkTheme == True:
			root.tk.call("set_theme", "light")
			darkTheme = False
		else:
			root.tk.call("set_theme", "dark")
			darkTheme = True

	def key_pressed(event):
		if DEBUG: print("KEY: " + event.keysym)
		key = event.char
		calculator.verifyInput(app,key)

	root.bind("<Key>",key_pressed)

	def hitEnter(event):
		if DEBUG: print("DEBUG: pressed enter")
		calculator.button_pressed(app,"=") #Triggers the already existing equals function

	def hitBackspace(event):
		if DEBUG: print("DEBUG: pressed backspace")
		calculator.button_pressed(app,"BackSpace")

	def hitDelete(event):
		if DEBUG: print("DEBUG: pressed delete")
		calculator.button_pressed(app,"C") #Triggers the already existing clear function

	def copyResults(event):
		print("copying")
		calculator.copyPasteHandler(app,"copy")

	def pasteResults(event):
		print("pasting")
		calculator.copyPasteHandler(app,"paste")

	root.bind('<Return>', hitEnter)
	root.bind('<BackSpace>', hitBackspace)
	root.bind('<Delete>', hitDelete)
	root.bind('<Control-c>', copyResults)
	root.bind('<Control-v>', pasteResults)

	def changeType():
		#Could be used in the future to change calculator types (scientific, conversion, etc)
		if DEBUG: print("Change type")

	##########Menu##########
	menubar = tk.Menu(root)
	
	view = tk.Menu(menubar, tearoff=False)
	menubar.add_cascade(label="View", menu=view)
	view.add("command", label="Theme", command=change_theme)

	#Not working, input issues
	#edit = tk.Menu(menubar, tearoff=False)
	#menubar.add_cascade(label="Edit", menu=edit)
	#edit.add("command", label="Copy", command=copyResults)
	#edit.add("command", label="Paste", command=pasteResults(event))
	''' Needs a lot more work for this to be done
	edit.add("command", label="Standard", command=changeType)
	edit.add("command", label="Scientific", command=changeType)
	edit.add("command", label="Graphing", command=changeType)
	edit.add("command", label="Conversion", command=changeType)
	'''

	menubar.add_cascade(label="Quit", menu=quit, command=root.destroy)

	root.config(menu=menubar)
	##########End menu##########

	app = calculator(root)
	app.pack(fill="both", expand=True)

	root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
	y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
	root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

	root.mainloop()