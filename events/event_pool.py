# pula wydarzen

event_pool = [
    {
        "text": "Protesty w stolicy! Co robisz?",
        "options": {
            "Wezwij wojsko": {"opinia_publiczna": -20, "wojsko": -5},
            "Negocjuj z liderami": {"opinia_publiczna": +10, "gospodarka": -5}
        }
    },
    {
        "text": "Kryzys finansowy! Co robisz?",
        "options": {
            "Dodruk pieniądza": {"gospodarka": +10, "opinia_publiczna": -10},
            "Podnieś podatki": {"gospodarka": +5, "opinia_publiczna": -15}
        }
    },
    {
        "text": "Obcy dyktator chce współpracy militarnej.",
        "options": {
            "Zgoda": {"wojsko": +15, "opinia_publiczna": -10},
            "Odmowa": {"wojsko": -5, "opinia_publiczna": +5}
        }
    },
    {
        "text": "Twoje państwo wygrywa konkurs na najczystsze miasto!",
        "options": {
            "Świętuj z obywatelami": {"opinia_publiczna": +15},
            "Ignoruj sukces": {"opinia_publiczna": -5}
        }
    },
    {
        "text": "kolejny event placeholder ",
        "options": {
            "opcja1": {"opinia_publiczna": +15},
            "opcja2": {"opinia_publiczna": -5}
        }
    }
]