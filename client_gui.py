import gi
import socket

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Pango

import numpy as np

from matplotlib.backends.backend_gtk4agg import \
    FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.figure import Figure

from conversao import *
from Enlace.enquadramento import *
from Enlace.correcao import *
from Fisica.modulacaodigital import *
from Fisica.mod_portadora import *

# Variáveis
crc_len = 32
generator = [1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,0,1,1,1] # Representação do polinômio gerador, neste caso CRC32 IEEE 802-3

class SignalWindow(Gtk.Window):
    def __init__(self, parent, encoding_type, modulation_type, bit_list):
        super().__init__(title='Sinal', transient_for=parent)
        
        self.set_default_size(1000, 500)

        self.encoding_type = encoding_type
        self.modulation_type = modulation_type
        signal_y = self.modulate_signal(bit_list)
        self.create_signal_curve(bit_list, signal_y)

    def modulate_signal (self, bit_list_in: list):
        amp = 1.0
        freq = 1.0
        samplen = 100
        signal_y = []
        bit_list = list(bit_list_in)

        match self.encoding_type:

            case 0: # Sem código
                match self.modulation_type:
                    case 0: # Amplitude
                        signal_y = amplitude_sk(amp, freq, bit_list, samplen)
                    case 1: # Frequência
                        signal_y = frequency_sk(amp, freq, freq*2, bit_list, samplen)
                    case 2: # 8QAM
                        signal_y = eight_qam(amp, freq, bit_list, samplen)
                    case _:
                        print("Invalid modulation type (" + str(self.modulation_type) + ") for encoding type: " + str(self.encoding_type))
                        signal_y = bit_list
            case 1: # NRZ Polar
                match self.modulation_type:
                    case 0: signal_y = ask_nrz(amp, freq, bit_list, samplen)
                    case 1: signal_y = fsk_nrz(amp, freq, freq*2, bit_list, samplen)
                    case 2: signal_y = eight_qam_nrz(amp, freq, bit_list, samplen)
                    case _:
                        print("Invalid modulation type (" + str(self.modulation_type) + ") for encoding type: " + str(self.encoding_type))
                        signal_y = bit_list
            case 2: # Manchester
                match self.modulation_type:
                    case 0: signal_y = ask_manchester(amp, freq, bit_list, samplen)
                    case 1: signal_y = fsk_manchester(amp, freq, freq*2, bit_list, samplen)
                    case 2: signal_y = eight_qam_manchester(amp, freq, bit_list, samplen)
                    case _:
                        print("Invalid modulation type (" + str(self.modulation_type) + ") for encoding type: " + str(self.encoding_type))
                        signal_y = bit_list
            case 3: # Bipolar
                match self.modulation_type:
                    case 0: signal_y = ask_bipolar(amp, freq, bit_list, samplen)
                    case 1: signal_y = fsk_bipolar(amp, freq, freq*4, bit_list, samplen)
                    case 2: signal_y = eight_qam_bipolar_amplitude(amp, freq, bit_list, samplen)
                    case _:
                        print("Invalid modulation type (" + str(self.modulation_type) + ") for encoding type: " + str(self.encoding_type))
                        signal_y = bit_list

        return signal_y
    
    def create_signal_curve (self, bit_list, signal_y: list):
        
        # Para debug
        index_list = [i for i in range(len(bit_list))]
        print([(i,j) for i, j in zip(index_list, bit_list)])
        length_x = len(bit_list)
        signal_x = np.linspace(0, length_x, len(signal_y))
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        # Código tirado de https://stackoverflow.com/a/10378357
        # Impede que a curva fique conectada quando houver descontinuidade na função
        pos = np.where(np.abs(np.diff(signal_y)) >= 0.5)[0]+1

        signal_x = np.insert(signal_x, pos, np.nan)
        signal_y = np.insert(signal_y, pos, np.nan)

        ax.plot(signal_x, signal_y)
        ax.xaxis.set_ticks(np.arange(0, len(bit_list), 1))
        # Adiciona linhas verticais a cada intervalo igual a 1
        for i in range(len(bit_list)):
            ax.vlines(x=i, ymin=-1, ymax=1, colors='gray', ls=':', lw=1)

        ax.axis('tight')

        sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10,
                                margin_start=10, margin_end=10)
        self.set_child(sw)

        canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        canvas.set_size_request(100*len(bit_list), 100)
        sw.set_child(canvas)
        return


class GUIClient(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Cliente')

        self.msgs_to_send = ""
        
        # Configuração de parâmetros de comunicação
        self.encoding_type = 0 # Código usado: 0 - Sem código; 1 - NRZ Polar; 2 - Manchester; 3 - Bipolar
        self.framing_type = 0 # Enquadramento: 0 - Contagem de caracteres; 1 - Delimitação por flag
        self.error_handling_type = 0 # Método de detecção/correção: 0 - Sem método; 1 - Bit de paridade par; 2 - CRC32; 3 - Hamming
        self.modulation_type = 0 # Método de modulação por portadora: 0 - Amplitude; 1 - Frequência; 2 - 8QAM

        self.set_default_size(500, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        self.create_textview()
        self.create_toolbar()
        self.create_buttons()

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
            self.msgs_to_send += text + "\n"
            self.textbuffer.insert(self.textbuffer.get_end_iter(), text + "\n")
            # Código abaixo retirado de https://stackoverflow.com/a/70511445
            # Create a mark at the end of all the text
            mark = self.textbuffer.create_mark("end", self.textbuffer.get_end_iter(), False)
            # Scroll so we can see the end mark
            self.textview.scroll_mark_onscreen(mark)

    def on_enviar_clicked (self, button):

        # Impede envio nulo
        if self.msgs_to_send == "":
            return

        host = "127.0.0.1"
        port = 7777

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((host, port))
        # try:
        #     tcp_client.connect((host, port))
        # except socket.error as msg:
        #     raise socket.error(f"Failed to connect: {msg}")

        msg_list = self.msgs_to_send.split("\n")[:-1]
        self.msgs_to_send = "" # Esvazia buffer de mensagens a enviar
        self.textbuffer.insert(self.textbuffer.get_end_iter(), "----\n") # Coloca um separador para indicar que as mensages na seção anterior foram enviadas


        bit_string = []
        for msg in msg_list:
            bit_string += self.create_frame(msg)

        encoded_bit_stream = self.encode_stream(bit_string)

        self.display_modulated_signal(encoded_bit_stream)

        # Convertendo -1 para 255
        encoded_bit_stream = makeByteArrayFriendly(encoded_bit_stream)
        encoded_byte_stream = bytearray(encoded_bit_stream)
        
        # Para que o programa Meio saiba qual codificação e enquadramento usados
        code = bytearray([self.encoding_type])
        framing_type = bytearray([self.framing_type])
        encoded_byte_stream = code + framing_type + encoded_byte_stream

        status = tcp_client.send(encoded_byte_stream)

        if status > 0:
            data = tcp_client.recv(2048)
            print('Got', repr(data))
        tcp_client.close()

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.props.hexpand = True
        scrolledwindow.props.vexpand = True
        self.box.append(scrolledwindow)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("Log de mensagens enviadas\n\n")
        self.textview.props.editable = False
        self.textview.props.cursor_visible = False

        scrolledwindow.set_child(self.textview)

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


        radio_amplitude = Gtk.CheckButton(label='Amplitude')
        radio_amplitude.props.active = True
        grid.attach(radio_amplitude, 0, 3, 1, 1)

        radio_frequency = Gtk.CheckButton(label='Frequência')
        radio_frequency.set_group(radio_amplitude)
        grid.attach_next_to(
            radio_frequency, radio_amplitude, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_8qam = Gtk.CheckButton(label='8QAM')
        radio_8qam.set_group(radio_amplitude)
        grid.attach_next_to(
            radio_8qam, radio_frequency, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_amplitude.connect(
            'toggled', self.on_modulation_toggled, 0
        )

        radio_frequency.connect(
            'toggled', self.on_modulation_toggled, 1
        )

        radio_8qam.connect(
            'toggled', self.on_modulation_toggled, 2
        )

    def on_code_toggled(self, _widget, mode):
        self.encoding_type = mode

    def on_frame_toggled(self, _widget, mode):
        self.framing_type = mode

    def on_errortype_toggled(self, _widget, mode):
        self.error_handling_type = mode

    def on_modulation_toggled(self, _widget, mode):
        self.modulation_type = mode

    
    def create_frame (self, msg:str) -> list:
        bin_msg = bytearray(msg, 'utf8')
        msg_byte_list = [byte for byte in bin_msg]
        bit_list = byte2bit_string(msg_byte_list)

        # Detecção/Correção de error
        match self.error_handling_type:

            case 0:
                pass # Nada a ser feito

            case 1: # Bit de paridade par
                bit_list = add_bit_de_paridade_par(bit_list)

            case 2: # CRC 32
                bit_list = add_crc(bit_list, crc_len, generator)

            case 3: # Hamming
                bit_list = cod_hamming(bit_list)
                pass

            case _:
                pass

        # Enquadramento

        match self.framing_type:

            case 0: # Contagem de caracteres
                bit_list = list(enquadrar_com_contagem(bit_list))
            
            case 1: # Inserção de byte de flag
                bit_list = list(enquadrar_com_flag(bit_list))
            
            case _:
                pass
        
        frame = bit_list
        return frame

    def encode_stream (self, bit_string: list) -> list:

        encoded_bit_stream = list(bit_string)

        match self.encoding_type:

            case 0: # Sem código
                pass

            case 1: # NRZ Polar
                encoded_bit_stream = mod_NRZpolar(encoded_bit_stream)
                pass
            
            case 2: # Manchester
                encoded_bit_stream, _ = mod_Manchester(encoded_bit_stream, 1)
                pass

            case 3: # Bipolar
                encoded_bit_stream = mod_Bipolar(encoded_bit_stream)
                pass

            case _:
                pass

        return encoded_bit_stream
    
    def modulate_stream (self, bit_string: list):
        """Modula o sinal"""
        # todo
        pass

    def display_modulated_signal (self, bit_string: list):
        """Faz desenho da curva do sinal e apresenta na tela. """
        # todo
        self.signalwin = SignalWindow(self, self.encoding_type, self.modulation_type, bit_string)
        self.signalwin.present()


def on_activate(app):
    win = GUIClient(application=app)
    win.present()


app = Gtk.Application(application_id='com.client_tr2024.App')
app.connect('activate', on_activate)

app.run(None)