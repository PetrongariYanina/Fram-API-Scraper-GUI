import threading
import queue
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from APP_FRAM import buscar_hoteles_riu_api, destinos_ids, ciudad_salida_dict


def sanitize_filename(s: str) -> str:
    return s.replace('/', '-').replace('\\\n', '').replace(' ', '_')


class App:
    def __init__(self, root):
        self.root = root
        root.title('FRAM RIU Scraper - Interfaz')

        frm = ttk.Frame(root, padding=10)
        frm.grid(sticky='nsew')

        ttk.Label(frm, text='Destino:').grid(row=0, column=0, sticky='w')
        self.destino_cb = ttk.Combobox(frm, values=sorted(list(destinos_ids.keys())), state='readonly')
        self.destino_cb.grid(row=0, column=1, sticky='ew')
        self.destino_cb.set(sorted(list(destinos_ids.keys()))[0])

        ttk.Label(frm, text='Ciudad salida:').grid(row=1, column=0, sticky='w')
        self.ciudad_cb = ttk.Combobox(frm, values=sorted(list(ciudad_salida_dict.keys())), state='readonly')
        self.ciudad_cb.grid(row=1, column=1, sticky='ew')
        self.ciudad_cb.set(sorted(list(ciudad_salida_dict.keys()))[0])

        ttk.Label(frm, text='Fecha (DD/MM/YYYY):').grid(row=2, column=0, sticky='w')
        self.fecha_entry = ttk.Entry(frm)
        self.fecha_entry.grid(row=2, column=1, sticky='ew')
        self.fecha_entry.insert(0, '30/01/2026')

        self.run_btn = ttk.Button(frm, text='Ejecutar', command=self.on_run)
        self.run_btn.grid(row=3, column=0, columnspan=2, pady=(6, 10), sticky='ew')

        self.log = scrolledtext.ScrolledText(frm, width=80, height=20, wrap='word')
        self.log.grid(row=4, column=0, columnspan=2, sticky='nsew')

        # grid config
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(4, weight=1)

        self.q = None
        self.worker_thread = None

        # start polling loop placeholder
        self.root.after(100, lambda: None)

    def append_log(self, text: str):
        self.log.insert(tk.END, text + '\n')
        self.log.see(tk.END)

    def on_run(self):
        destino = self.destino_cb.get()
        ciudad = self.ciudad_cb.get()
        fecha = self.fecha_entry.get().strip()

        if not destino or not ciudad or not fecha:
            messagebox.showwarning('Faltan datos', 'Selecciona destino, ciudad y escribe la fecha.')
            return

        if destino not in destinos_ids or ciudad not in ciudad_salida_dict:
            messagebox.showerror('Error', 'Destino o ciudad no válidos.')
            return

        id_dest = destinos_ids[destino]
        id_ciud = ciudad_salida_dict[ciudad]

        # desactivar controles
        self.run_btn.config(state='disabled')
        self.destino_cb.config(state='disabled')
        self.ciudad_cb.config(state='disabled')
        self.fecha_entry.config(state='disabled')

        # limpiar log
        self.log.delete('1.0', tk.END)

        # cola para mensajes desde el hilo
        self.q = queue.Queue()

        def worker():
            try:
                # pasar la cola.put como callback
                resultados = buscar_hoteles_riu_api(id_dest, id_ciud, fecha, log_callback=self.q.put)

                # Guardar resultados en archivo
                safe_fecha = fecha.replace('/', '-')
                downloads_dir = "Web_FRAM"
                os.makedirs(downloads_dir, exist_ok=True)
                filename = os.path.join(downloads_dir, f"Web_FRAM_{destino}_desde_{ciudad}_{safe_fecha}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"--- Búsqueda para {destino} desde {ciudad} en fecha {fecha} ---\n\n")
                    f.write("=== RESULTADOS RIU ENCONTRADOS ===\n\n")
                    if resultados:
                        for h in resultados:
                            f.write(f"✓ {h['titulo']}\n")
                            f.write(f"  Precio: {h['precio']} | Pág: {h['pagina']} | Pos: {h['posicion']}\n")
                            f.write(f"  Link: {h['url']}\n\n")
                    else:
                        f.write("No se encontraron hoteles RIU.\n")

                # notificar fin
                self.q.put(("done", filename))
            except Exception as e:
                self.q.put(("error", str(e)))

        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()

        # iniciar polling de la cola
        self.root.after(100, self._poll_queue)

    def _poll_queue(self):
        try:
            while True:
                item = self.q.get_nowait()
                if isinstance(item, tuple):
                    tag, payload = item
                    if tag == 'done':
                        self.append_log(f"\n✓ Resultados guardados en: {payload}")
                        messagebox.showinfo('Finalizado', f'Resultados guardados en:\n{payload}')
                        # reactivar controles
                        self.run_btn.config(state='normal')
                        self.destino_cb.config(state='readonly')
                        self.ciudad_cb.config(state='readonly')
                        self.fecha_entry.config(state='normal')
                    elif tag == 'error':
                        self.append_log(f"Error: {payload}")
                        messagebox.showerror('Error', payload)
                        self.run_btn.config(state='normal')
                        self.destino_cb.config(state='readonly')
                        self.ciudad_cb.config(state='readonly')
                        self.fecha_entry.config(state='normal')
                else:
                    # item es texto
                    try:
                        self.append_log(str(item))
                    except Exception:
                        pass
        except queue.Empty:
            pass
        # si el hilo sigue vivo, seguir, si no, reactivar controles por si algo falló
        if self.worker_thread and self.worker_thread.is_alive():
            self.root.after(100, self._poll_queue)
        else:
            # si la cola quedó vacía y hilo terminó, asegurar controles habilitados
            self.run_btn.config(state='normal')
            self.destino_cb.config(state='readonly')
            self.ciudad_cb.config(state='readonly')
            self.fecha_entry.config(state='normal')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()






#convertir en un .exe con pyinstaller:
#pyinstaller.exe --onefile --noconsole --add-data "APP_FRAM.py;."  "APP_FRAM_tk.py" --icon=icon.ico --name="Scrap-FRAM"