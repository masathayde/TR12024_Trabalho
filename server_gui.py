import gi
import socket
import threading

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Pango

from conversao import *
from Enlace.enquadramento import *
from Enlace.correcao import *
from Fisica.modulacaodigital import *

# Variáveis
crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3


class GUIServer(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Servidor')

        self.set_default_size(500, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        self.create_textview()
        # self.create_toolbar()
        self.create_buttons()


        # Configuração de parâmetros de comunicação
        self.encoding_type = 0 # Código usado: 0 - Sem código; 1 - NRZ Polar; 2 - Manchester; 3 - Bipolar
        self.framing_type = 0 # Enquadramento: 0 - Contagem de caracteres; 1 - Delimitação por flag
        self.error_handling_type = 0 # Método de detecção/correção: 0 - Sem método; 1 - Bit de paridade par; 2 - CRC32; 3 - Hamming

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

        radio_nocode = Gtk.CheckButton(label='Sem Código')
        radio_nocode.props.active = True
        grid.attach(radio_nocode, 0, 0, 1, 1)

        radio_nrzp = Gtk.CheckButton(label='NRZ Polar')
        radio_nrzp.set_group(radio_nocode)
        grid.attach_next_to(
            radio_nrzp, radio_nocode, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_manchester = Gtk.CheckButton(label='Manchester')
        radio_manchester.set_group(radio_nocode)
        grid.attach_next_to(
            radio_manchester, radio_nrzp, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_bipolar = Gtk.CheckButton(label='Bipolar')
        radio_bipolar.set_group(radio_nocode)
        grid.attach_next_to(
            radio_bipolar, radio_manchester, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_nocode.connect(
            'toggled', self.on_code_toggled, 0
        )
        radio_nrzp.connect(
            'toggled', self.on_code_toggled, 1
        )
        radio_manchester.connect(
            'toggled', self.on_code_toggled, 2
        )
        radio_bipolar.connect(
            'toggled', self.on_code_toggled, 3
        )


        radio_ccount = Gtk.CheckButton(label='Contagem de caracteres')
        radio_ccount.props.active = True
        grid.attach(radio_ccount, 0, 1, 1, 1)

        radio_flag = Gtk.CheckButton(label='Flag delimitadora')
        radio_flag.set_group(radio_ccount)
        grid.attach_next_to(
            radio_flag, radio_ccount, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_ccount.connect(
            'toggled', self.on_frame_toggled, 0
        )

        radio_flag.connect(
            'toggled', self.on_frame_toggled, 1
        )


        radio_noerror = Gtk.CheckButton(label='Sem detecção/correção')
        radio_noerror.props.active = True
        grid.attach(radio_noerror, 0, 2, 1, 1)

        radio_parity = Gtk.CheckButton(label='Bit de paridade par')
        radio_parity.set_group(radio_noerror)
        grid.attach_next_to(
            radio_parity, radio_noerror, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_CRC32 = Gtk.CheckButton(label='CRC-32')
        radio_CRC32.set_group(radio_noerror)
        grid.attach_next_to(
            radio_CRC32, radio_parity, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_hamming = Gtk.CheckButton(label='Hamming')
        radio_hamming.set_group(radio_noerror)
        grid.attach_next_to(
            radio_hamming, radio_CRC32, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_noerror.connect(
            'toggled', self.on_errortype_toggled, 0
        )

        radio_parity.connect(
            'toggled', self.on_errortype_toggled, 1
        )

        radio_CRC32.connect(
            'toggled', self.on_errortype_toggled, 2
        )

        radio_hamming.connect(
            'toggled', self.on_errortype_toggled, 3
        )
    

    def on_code_toggled(self, _widget, mode):
        self.encoding_type = mode

    def on_frame_toggled(self, _widget, mode):
        self.framing_type = mode

    def on_errortype_toggled(self, _widget, mode):
        self.error_handling_type = mode


    def server_routine(self):

        msgs = ""
        host = "127.0.0.1"
        port = 7778

        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((host, port))
        tcp_server.listen()
        while 1:
            conn, addr = tcp_server.accept()
            data = conn.recv(2048)
            if data:
                msgs = self.get_all_msgs(data)
                self.textbuffer.set_text(msgs)
                conn.sendall(data)
            conn.close()

    def decode_data (self, data: bytearray) -> list:

        bit_stream = [bit for bit in data]
        bit_stream = reverseMakeByteArrayFriendly(bit_stream)
        
        match self.encoding_type:

            case 0: # Sem código
                pass

            case 1: # NRZ Polar
                bit_stream = demod_NRZpolar(bit_stream)
                pass
            
            case 2: # Manchester
                bit_stream = demod_Manchester(bit_stream)
                pass

            case 3: # Bipolar
                bit_stream = demod_Bipolar(bit_stream)
                pass

            case _:
                pass

        return bit_stream

    def separate_frame (self, bit_string: list):
        frame = []
        remaining_string = []

        match self.framing_type:

            case 0: # Contagem de caracteres
                frame, _, remaining_string = desenquadrar_com_contagem(bit_string)
            
            case 1: # Inserção de byte de flag
                frame, remaining_string = desenquadrar_com_flag(bit_string)
            
            case _:
                pass

        return (frame, remaining_string)
    
    def check_error (self, bit_list: list):

        corrected_bit_list = list(bit_list)
        error_present = False

        # Detecção/Correção de error
        match self.error_handling_type:

            case 0:
                pass # Nada a ser feito

            case 1: # Bit de paridade par
                error_present = not checar_bit_de_paridade_par(bit_list)
            
            case 2: # CRC 32
                error_present = not check_crc(bit_list, crc_len, generator)

            case 3: # Hamming
                # Altera a entrada.
                corrected_bit_list, error_present = decod_hamming (bit_list)
                pass

            case _:
                pass

        return corrected_bit_list, error_present
    
    def strip_error_code (self, bit_string: list) -> list:

        frame = list(bit_string)
        match self.error_handling_type:

            case 0:
                pass # Nada a ser feito

            case 1: # Bit de paridade par
                frame = frame[:-1]
            
            case 2: # CRC 32
                frame = frame[:-32]

            case 3: # Hamming
                # Nada a ser feito se for Hamming
                pass

            case _:
                pass

        return frame


    def get_msg_from_frame (self, frame: list):
        
        corrected_frame, error_present = self.check_error(frame)
        payload = self.strip_error_code(corrected_frame)

        byte_payload = bit2byte_string(payload)

        bin_msg = bytearray(byte_payload)
        msg = ""

        if error_present:
            msg += "Erro detectado na mensagem."
            match self.error_handling_type:
                case 1:
                    msg += " Número de bits não é par."
                case 2:
                    msg += " Resto de CRC não é zero."
                case 3:
                    msg += " Aplicada correção de erro. Ainda podem existir erros."
                    msg += "\n"
                    try:
                        msg += bin_msg.decode('utf8')
                    except UnicodeDecodeError:
                        msg += "Não foi possível decodificar mensagem. A mensagem não pode ser exibida."
                case _:
                    pass
            msg += "\n"
        else:
            msg += "Nenhum erro detectado."
            msg += "\n"
            msg += bin_msg.decode('utf8') + "\n"
        
        return msg

    def get_all_msgs (self, data: bytearray) -> list:
        bit_string = self.decode_data(data) # Converte para uma lista no formato usado aqui
        print(bit_string)
        msgs = ""
        while len(bit_string) > 0:
            frame, bit_string = self.separate_frame(bit_string)
            if frame == []: # Não conseguimos criar uma frame por erro na sequência de bits
                break
            msgs += self.get_msg_from_frame(frame)
        return msgs

def on_activate(app):
    win = GUIServer(application=app)
    win.present()
    
    server_thread = threading.Thread(target=win.server_routine, args=[])
    server_thread.daemon = True
    server_thread.start()


app = Gtk.Application(application_id='com.server_tr2024.App')
app.connect('activate', on_activate)

app.run(None)