# import sys
# sys.path.insert(0, "C:\\msys64\\ucrt64\\lib\\python3.11\\site-packages")

import gi
import socket

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Pango

# from ..conversao import *
from Enlace.enquadramento import *

# Variáveis
crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3

def create_frame (msg:str) -> list:
    bin_msg = bytearray(msg, 'utf8')
    msg_byte_list = [byte for byte in bin_msg]
    frame = enquadrar_com_contagem(msg_byte_list)
    return frame


class TextViewWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Cliente')

        self.msgs = ""

        self.set_default_size(500, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        self.create_textview()
        self.create_toolbar()
        # self.create_buttons()

    def create_toolbar(self):
        toolbar = Gtk.Box(spacing=6)
        toolbar.props.margin_top = 6
        toolbar.props.margin_start = 6
        toolbar.props.margin_end = 6
        self.box.append(toolbar)

        self.entry = Gtk.Entry()
        self.entry.set_text('Inserir mensagem')
        self.entry.connect("activate", self.on_entry_activate)
        self.box.append(self.entry)

        self.send_button = Gtk.Button.new_with_label('Enviar')
        self.send_button.connect('clicked', self.on_enviar_clicked)
        self.box.append(self.send_button)

    def on_entry_activate (self, entry):
        text = entry.get_text()
        if text != "":
            entry.set_text("")
            self.msgs += text + "\n"
            self.textbuffer.set_text(self.msgs)

    def on_enviar_clicked (self, button):

        # Impede envio nulo
        if self.msgs == "":
            return

        host = "127.0.0.1"
        port = 6969

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect((host, port))
        except socket.error as msg:
            raise socket.error(f"Failed to connect: {msg}")

        self.msgs = self.msgs.split("\n")[:-1]

        # print(self.msgs.split("\n")[:-1])
        byte_string = []
        for msg in self.msgs:
            byte_string += create_frame(msg)
        byte_stream = bytearray(byte_string)
        status = tcp_client.send(byte_stream)

        if status > 0:
            data = tcp_client.recv(1024)
            print('Got', repr(data))
        tcp_client.close()

        # Agora desabilitar botão e caixa de texto para impedir mais entrada
        button.set_label("Enviado")
        button.set_sensitive(False)
        self.textview.set_sensitive(False)
        self.entry.set_editable(False)


    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.props.hexpand = True
        scrolledwindow.props.vexpand = True
        self.box.append(scrolledwindow)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(self.msgs)
        self.textview.props.editable = False
        self.textview.props.cursor_visible = False

        scrolledwindow.set_child(self.textview)

        self.tag_bold = self.textbuffer.create_tag(
            'bold', weight=Pango.Weight.BOLD
        )
        self.tag_italic = self.textbuffer.create_tag(
            'italic', style=Pango.Style.ITALIC
        )
        self.tag_underline = self.textbuffer.create_tag(
            'underline', underline=Pango.Underline.SINGLE
        )
        self.tag_found = self.textbuffer.create_tag(
            'found', background='yellow'
        )

    def create_buttons(self):
        grid = Gtk.Grid()
        self.box.append(grid)

        check_editable = Gtk.CheckButton(label='Editable')
        check_editable.props.active = True
        check_editable.connect('toggled', self.on_editable_toggled)
        grid.attach(check_editable, 0, 0, 1, 1)

        check_cursor = Gtk.CheckButton(label='Cursor Visible')
        check_cursor.props.active = True
        check_editable.connect('toggled', self.on_cursor_toggled)
        grid.attach_next_to(
            check_cursor, check_editable, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone = Gtk.CheckButton(label='No Wrapping')
        radio_wrapnone.props.active = True
        grid.attach(radio_wrapnone, 0, 1, 1, 1)

        radio_wrapchar = Gtk.CheckButton(label='Character Wrapping')
        radio_wrapchar.set_group(radio_wrapnone)
        grid.attach_next_to(
            radio_wrapchar, radio_wrapnone, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapword = Gtk.CheckButton(label='Word Wrapping')
        radio_wrapword.set_group(radio_wrapnone)
        grid.attach_next_to(
            radio_wrapword, radio_wrapchar, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone.connect(
            'toggled', self.on_wrap_toggled, Gtk.WrapMode.NONE
        )
        radio_wrapchar.connect(
            'toggled', self.on_wrap_toggled, Gtk.WrapMode.CHAR
        )
        radio_wrapword.connect(
            'toggled', self.on_wrap_toggled, Gtk.WrapMode.WORD
        )

    def on_button_clicked(self, _widget, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)

    def on_clear_clicked(self, _widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_editable_toggled(self, widget):
        self.textview.props.editable = widget.props.active

    def on_cursor_toggled(self, widget):
        self.textview.props.cursor_visible = widget.props.active

    def on_wrap_toggled(self, _widget, mode):
        self.textview.props.wrap_mode = mode

    def on_justify_toggled(self, _widget, justification):
        self.textview.props.justification = justification

def on_activate(app):
    win = TextViewWindow(application=app)
    win.present()


app = Gtk.Application(application_id='com.client_tr2024.App')
app.connect('activate', on_activate)

app.run(None)