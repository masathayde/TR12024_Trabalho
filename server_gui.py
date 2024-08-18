import gi
import socket
import threading

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Pango

# from ..conversao import *
from Enlace.enquadramento import *

# Variáveis
crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3


class TextViewWindow(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Servidor')

        self.set_default_size(500, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        self.create_textview()
        # self.create_toolbar()
        # self.create_buttons()

    def create_toolbar(self):
        toolbar = Gtk.Box(spacing=6)
        toolbar.props.margin_top = 6
        toolbar.props.margin_start = 6
        toolbar.props.margin_end = 6
        self.box.prepend(toolbar)

        button_bold = Gtk.Button(icon_name='format-text-bold-symbolic')
        toolbar.append(button_bold)

        button_italic = Gtk.Button(icon_name='format-text-italic-symbolic')
        toolbar.append(button_italic)

        button_underline = Gtk.Button(
            icon_name='format-text-underline-symbolic'
        )
        toolbar.append(button_underline)

        button_bold.connect('clicked', self.on_button_clicked, self.tag_bold)
        button_italic.connect(
            'clicked', self.on_button_clicked, self.tag_italic
        )
        button_underline.connect(
            'clicked', self.on_button_clicked, self.tag_underline
        )

        toolbar.append(Gtk.Separator())

        justifyleft = Gtk.ToggleButton(
            icon_name='format-justify-left-symbolic'
        )
        toolbar.append(justifyleft)

        justifycenter = Gtk.ToggleButton(
            icon_name='format-justify-center-symbolic'
        )
        justifycenter.set_group(justifyleft)
        toolbar.append(justifycenter)

        justifyright = Gtk.ToggleButton(
            icon_name='format-justify-right-symbolic'
        )
        justifyright.set_group(justifyleft)
        toolbar.append(justifyright)

        justifyfill = Gtk.ToggleButton(
            icon_name='format-justify-fill-symbolic'
        )
        justifyfill.set_group(justifyleft)
        toolbar.append(justifyfill)

        justifyleft.connect(
            'toggled', self.on_justify_toggled, Gtk.Justification.LEFT
        )
        justifycenter.connect(
            'toggled', self.on_justify_toggled, Gtk.Justification.CENTER
        )
        justifyright.connect(
            'toggled', self.on_justify_toggled, Gtk.Justification.RIGHT
        )
        justifyfill.connect(
            'toggled', self.on_justify_toggled, Gtk.Justification.FILL
        )

        toolbar.append(Gtk.Separator())

        button_clear = Gtk.Button(icon_name='edit-clear-symbolic')
        button_clear.connect('clicked', self.on_clear_clicked)
        toolbar.append(button_clear)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.props.hexpand = True
        scrolledwindow.props.vexpand = True
        self.box.append(scrolledwindow)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text('Esperando mensagem')
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


def separate_frame (byte_string: list):
    frame, characer_count, remaining_string = desenquadrar_com_contagem(byte_string)
    return (frame, characer_count, remaining_string)

def get_msg_from_frame (data: list, character_count: int):
    bin_msg = bytearray(data)
    msg = "Character count: " + str(character_count) + "\n" + bin_msg.decode('utf8') + "\n"
    return msg

def get_all_msgs (data: bytearray) -> list:
    byte_string = [byte for byte in data] # Converte para uma lista de bytes no formato usado aqui
    msgs = ""
    while len(byte_string) > 0:
        frame, character_count, byte_string = separate_frame(byte_string)
        msgs += get_msg_from_frame(frame, character_count)
    return msgs

def server_routine(window: TextViewWindow):

    msgs = ""
    host = "127.0.0.1"
    port = 6969

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((host, port))
    tcp_server.listen()
    conn, addr = tcp_server.accept()
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        msgs = get_all_msgs(data)
        window.textbuffer.set_text(msgs)
        conn.sendall(data)
    conn.close()

def on_activate(app):
    win = TextViewWindow(application=app)
    win.present()
    
    server_thread = threading.Thread(target=server_routine, args=[win])
    server_thread.daemon = True
    server_thread.start()


app = Gtk.Application(application_id='com.server_tr2024.App')
app.connect('activate', on_activate)

app.run(None)