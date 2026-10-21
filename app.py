"""Offline desktop interface; conversion logic lives in excel_to_prism.py."""
import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
from excel_to_prism import convert_excel_to_prism

TITLE = 'Excel to Prism Studio'
HELP = '''1. Browse for an Excel workbook (.xlsx, .xlsm or .xls).
2. Choose all worksheets or one named worksheet.
3. Choose Column or XY and an output .pzfx filename.
4. Convert, then open the result in your licensed GraphPad Prism.

First row: column titles. Other rows: numbers or blank cells.
Column: each column contains observations for one group.
XY: first column contains X; remaining columns contain Y datasets.
Each worksheet becomes a separate Prism data table.

This converter creates data tables only. It does not generate graphs,
analyses, grouped tables or replicate subcolumns. Empty/header-only
worksheets are skipped. Invalid cells report their Excel address.
Save/recalculate formulas in Excel first; only cached values are read.
Existing output files are never overwritten. Choose a new filename.

Prism 10 can open legacy PZFX in compatibility mode. Verify table names,
values, blanks and table type in Prism before relying on the conversion.
GraphPad Prism is separately licensed and is not bundled.
Conversion runs offline; your workbook is not uploaded.
'''
PALETTES = {
    'Light': ('#f6f3f5', '#ffffff', '#231c26', '#a41646', '#ffffff'),
    'OLED Dark': ('#000000', '#171217', '#f5eff5', '#c83262', '#ffffff'),
    'Colored Mode': ('#142235', '#22374b', '#fff4e3', '#a41646', '#ffffff'),
}

class App:
    def __init__(self, root):
        self.root = root
        root.title(TITLE)
        root.geometry('880x620')
        root.minsize(680, 500)
        self.busy = False
        self.events = queue.Queue()
        self.result = None
        self.source = tk.StringVar()
        self.output = tk.StringVar()
        self.sheet = tk.StringVar(value='All worksheets')
        self.kind = tk.StringVar(value='Column')
        self.theme = tk.StringVar(value='Light')
        self.status = tk.StringVar(value='Select a workbook to begin.')
        self.style = ttk.Style(root)
        self.style.theme_use('clam')
        outer = ttk.Frame(root, padding=20)
        outer.pack(fill='both', expand=True)
        top = ttk.Frame(outer)
        top.pack(fill='x')
        ttk.Label(top, text=TITLE, style='Title.TLabel').pack(side='left')
        ttk.Button(top, text='Supporting Tools', command=self.help).pack(side='right', padx=(8,0))
        themes = ttk.Combobox(top, textvariable=self.theme, values=list(PALETTES), state='readonly', width=14)
        themes.pack(side='right')
        themes.bind('<<ComboboxSelected>>', lambda e: self.apply_theme())
        ttk.Label(outer, text='Excel worksheets → Prism data tables · Offline', padding=(0,8,0,16)).pack(anchor='w')
        form = ttk.Frame(outer)
        form.pack(fill='x')
        form.columnconfigure(1, weight=1)
        ttk.Label(form, text='Excel workbook').grid(row=0,column=0,sticky='w',padx=(0,12),pady=6)
        self.source_entry = ttk.Entry(form, textvariable=self.source, state='readonly')
        self.source_entry.grid(row=0,column=1,sticky='ew')
        self.browse = ttk.Button(form, text='Browse…', command=self.choose_input)
        self.browse.grid(row=0,column=2,padx=(8,0))
        ttk.Label(form,text='Worksheet').grid(row=1,column=0,sticky='w',pady=6)
        self.sheets = ttk.Combobox(form, textvariable=self.sheet, values=['All worksheets'], state='disabled')
        self.sheets.grid(row=1,column=1,sticky='ew')
        ttk.Label(form,text='Table type').grid(row=2,column=0,sticky='w',pady=6)
        self.types = ttk.Combobox(form,textvariable=self.kind,values=['Column','XY'],state='readonly')
        self.types.grid(row=2,column=1,sticky='ew')
        ttk.Label(form,text='Save PZFX as').grid(row=3,column=0,sticky='w',pady=6)
        self.out_entry = ttk.Entry(form,textvariable=self.output)
        self.out_entry.grid(row=3,column=1,sticky='ew')
        self.save_button = ttk.Button(form,text='Choose…',command=self.choose_output)
        self.save_button.grid(row=3,column=2,padx=(8,0))
        self.tip = ttk.Label(outer,text='Column: one group per column. XY: X first, then Y datasets.',padding=(0,12))
        self.tip.pack(anchor='w')
        self.types.bind('<<ComboboxSelected>>', lambda e: self.tip.configure(text=(
            'XY: first column is X; all remaining columns are Y datasets.' if self.kind.get()=='XY'
            else 'Column: each column is a separate group of observations.')))
        actions = ttk.Frame(outer)
        actions.pack(fill='x')
        self.convert_button = ttk.Button(actions,text='Convert to Prism',style='Accent.TButton',command=self.convert)
        self.convert_button.pack(side='left')
        self.open_button = ttk.Button(actions,text='Open result',command=self.open_result,state='disabled')
        self.open_button.pack(side='left',padx=8)
        self.progress = ttk.Progressbar(outer,mode='indeterminate')
        self.progress.pack(fill='x',pady=(14,8))
        ttk.Label(outer,textvariable=self.status,wraplength=620).pack(anchor='w')
        ttk.Label(outer,text='Conversion details',padding=(0,16,0,6)).pack(anchor='w')
        logframe=ttk.Frame(outer)
        logframe.pack(fill='both',expand=True)
        self.log=tk.Text(logframe,wrap='word',height=7,state='disabled',font=('Segoe UI',10))
        scroll=ttk.Scrollbar(logframe,command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y')
        self.log.pack(side='left',fill='both',expand=True)
        root.protocol('WM_DELETE_WINDOW',self.close)
        self.apply_theme()
        root.after(100,self.poll)

    def apply_theme(self):
        bg,panel,fg,accent,onaccent=PALETTES[self.theme.get()]
        self.root.configure(bg=bg)
        self.style.configure('.',background=bg,foreground=fg,font=('Segoe UI',10))
        self.style.configure('TFrame',background=bg)
        self.style.configure('TLabel',background=bg,foreground=fg)
        self.style.configure('Title.TLabel',font=('Georgia',19),foreground=accent if self.theme.get()=='Light' else '#edb962')
        self.style.configure('TButton',background=panel,foreground=fg,padding=7)
        self.style.map('TButton',background=[('active',accent)],foreground=[('active',onaccent)])
        self.style.configure('Accent.TButton',background=accent,foreground=onaccent)
        self.style.configure('TEntry',fieldbackground=panel,foreground=fg,insertcolor=fg)
        self.style.configure('TCombobox',fieldbackground=panel,foreground=fg,arrowcolor=fg)
        self.style.map('TCombobox',fieldbackground=[('readonly',panel)],foreground=[('readonly',fg)])
        self.root.option_add('*TCombobox*Listbox.background',panel)
        self.root.option_add('*TCombobox*Listbox.foreground',fg)
        self.log.configure(bg=panel,fg=fg,insertbackground=fg)

    def write(self,text):
        self.log.configure(state='normal')
        self.log.insert('end',text+'\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def set_busy(self,value):
        self.busy=value
        for widget in [self.browse,self.save_button,self.out_entry,self.convert_button]:
            widget.configure(state='disabled' if value else 'normal')
        self.types.configure(state='disabled' if value else 'readonly')
        self.sheets.configure(state='disabled' if value or not self.source.get() else 'readonly')
        self.open_button.configure(state='normal' if self.result and not value else 'disabled')
        if value: self.progress.start(12)
        else: self.progress.stop()

    def choose_input(self):
        path=filedialog.askopenfilename(title='Select Excel workbook',filetypes=[('Excel workbooks','*.xlsx *.xlsm *.xls')])
        if not path: return
        self.set_busy(True)
        self.status.set('Reading worksheet names…')
        def load():
            try:
                with pd.ExcelFile(path) as book: names=book.sheet_names
                self.events.put(('loaded',(path,names)))
            except Exception as error: self.events.put(('error',str(error)))
        threading.Thread(target=load,daemon=True).start()

    def choose_output(self):
        path=filedialog.asksaveasfilename(title='Choose a NEW output filename',defaultextension='.pzfx',
            initialfile=Path(self.output.get()).name or 'converted.pzfx',filetypes=[('Prism XML','*.pzfx')])
        if path: self.output.set(path)

    def convert(self):
        if self.busy: return
        if not self.source.get() or not self.output.get().strip():
            messagebox.showwarning(TITLE,'Choose an Excel workbook and output filename.'); return
        source,output=self.source.get(),self.output.get().strip()
        kind=self.kind.get().lower()
        sheet=None if self.sheets.current()==0 else self.sheet.get()
        self.result=None
        self.set_busy(True)
        self.status.set('Converting worksheets…')
        self.write(f'Converting {Path(source).name} as {kind.upper()} tables…')
        def work():
            try:
                result=convert_excel_to_prism(source,output,kind,sheet)
                count=len(ET.parse(result).getroot().find('TableSequence'))
                self.events.put(('done',(result,count)))
            except Exception as error: self.events.put(('error',str(error)))
        threading.Thread(target=work,daemon=True).start()

    def poll(self):
        try:
            while True:
                event,payload=self.events.get_nowait()
                if event=='loaded':
                    path,names=payload
                    self.source.set(path)
                    self.output.set(str(Path(path).with_suffix('.pzfx')))
                    self.sheets.configure(values=['All worksheets']+names)
                    self.sheets.current(0)
                    self.status.set(f'{len(names)} worksheet(s) available. Choose a table type and output filename.')
                    self.write(f'Loaded {Path(path).name}: '+', '.join(names))
                elif event=='done':
                    self.result,count=payload
                    self.status.set(f'Created {count} table(s). Open the result in Prism to verify the data.')
                    self.write(f'Saved: {self.result}\nConverted {count} worksheet(s); empty/header-only worksheets are skipped.')
                else:
                    self.status.set('Operation failed. See conversion details.')
                    self.write('Error: '+payload)
                    messagebox.showerror(TITLE,payload)
                self.set_busy(False)
        except queue.Empty: pass
        self.root.after(100,self.poll)

    def open_result(self):
        if not self.result: return
        try:
            if sys.platform=='win32': os.startfile(str(self.result))
            elif sys.platform=='darwin': subprocess.Popen(['open',str(self.result)])
            else: subprocess.Popen(['xdg-open',str(self.result)])
        except OSError as error: messagebox.showerror(TITLE,f'Could not open result. Open it from Prism File > Open.\n{error}')

    def help(self):
        window=tk.Toplevel(self.root)
        window.title('Quick Start Guide')
        window.geometry('650x490')
        box=tk.Text(window,wrap='word',font=('Segoe UI',11),padx=18,pady=18)
        scroll=ttk.Scrollbar(window,command=box.yview)
        box.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y')
        box.pack(fill='both',expand=True)
        box.insert('1.0',HELP)
        box.configure(state='disabled')

    def close(self):
        if self.busy:
            messagebox.showinfo(TITLE,'Please wait for the current operation to finish before closing.'); return
        self.root.destroy()

def main():
    root=tk.Tk()
    App(root)
    if '--smoke-test' in sys.argv:
        root.after(800,root.destroy)
    root.mainloop()

if __name__=='__main__': main()
