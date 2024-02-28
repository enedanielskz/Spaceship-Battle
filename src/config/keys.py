import pygame

keys = {
        # Letters
        "Q": pygame.K_q,
        "W": pygame.K_w,
        "E": pygame.K_e,
        "R": pygame.K_r,
        "T": pygame.K_t,
        "Y": pygame.K_y,
        "U": pygame.K_u,
        "I": pygame.K_i,
        "O": pygame.K_o,
        "P": pygame.K_p,
        "A": pygame.K_a,
        "S": pygame.K_s,
        "D": pygame.K_d,
        "F": pygame.K_f,
        "G": pygame.K_g,
        "H": pygame.K_h,
        "J": pygame.K_j,
        "K": pygame.K_k,
        "L": pygame.K_l,
        "Z": pygame.K_z,
        "X": pygame.K_x,
        "C": pygame.K_c,
        "V": pygame.K_v,
        "B": pygame.K_b,
        "N": pygame.K_n,
        "M": pygame.K_m,

        # Numbers
        "1": pygame.K_1,
        "2": pygame.K_2,
        "3": pygame.K_3,
        "4": pygame.K_4,
        "5": pygame.K_5,
        "6": pygame.K_6,
        "7": pygame.K_7,
        "8": pygame.K_8,
        "9": pygame.K_9,
        "0": pygame.K_0,

        # Symbols
        "`": pygame.K_BACKQUOTE,
        "-": pygame.K_MINUS,
        "=": pygame.K_EQUALS,
        "[": pygame.K_LEFTBRACKET,
        "]": pygame.K_RIGHTBRACKET,
        ";": pygame.K_SEMICOLON,
        "'": pygame.K_QUOTE,
        "\\": pygame.K_BACKSLASH,
        ",": pygame.K_COMMA,
        ".": pygame.K_PERIOD,
        "/": pygame.K_SLASH,

        # Numpad
        "NUMPAD_/": pygame.K_KP_DIVIDE,
        "NUMPAD_*": pygame.K_KP_MULTIPLY,
        "NUMPAD_-": pygame.K_KP_MINUS,
        "NUMPAD_+": pygame.K_KP_PLUS,
        "NUMPAD_.": pygame.K_KP_PERIOD,
        "NUMPAD_ENTER": pygame.K_KP_ENTER,
        "NUMPAD_0": pygame.K_KP_0,
        "NUMPAD_1": pygame.K_KP_1,
        "NUMPAD_2": pygame.K_KP_2,
        "NUMPAD_3": pygame.K_KP_3,
        "NUMPAD_4": pygame.K_KP_4,
        "NUMPAD_5": pygame.K_KP_5,
        "NUMPAD_6": pygame.K_KP_6,
        "NUMPAD_7": pygame.K_KP_7,
        "NUMPAD_8": pygame.K_KP_8,
        "NUMPAD_9": pygame.K_KP_9,

        # Arrows
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT,
        "UP": pygame.K_UP,
        "DOWN": pygame.K_DOWN,

        # Other
        "ENTER": pygame.K_RETURN,
        "ESC": pygame.K_ESCAPE,
        "TAB": pygame.K_TAB,
        "CAPSLOCK": pygame.K_CAPSLOCK,
        "LSHIFT": pygame.K_LSHIFT,
        "LCTRL": pygame.K_LCTRL,
        "LALT": pygame.K_LALT,
        "SPACE": pygame.K_SPACE,
        "RALT": pygame.K_RALT,
        "RCTRL": pygame.K_RCTRL,
        "BACKSPACE": pygame.K_BACKSPACE,
        "RSHIFT": pygame.K_RSHIFT
       }


def get_key(key: str):
    return keys[key]


def get_key_name(keys_pressed):
    for key in keys:
        if keys_pressed[keys[key]]:
            return key
    return False
