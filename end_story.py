from config import PLAYER1_NAME, PLAYER2_NAME


def generate_story(score):
    if score == 0:
        return (
            f"{PLAYER1_NAME} zrobiła zawrotną karierę – została szefową wszystkich szefowych, miała swój talk-show, kolekcję dresów i hodowlę fok. "
            f"{PLAYER2_NAME} próbował ją dogonić, ale jedyne co złapał, to zadyszkę. Dzieci? Może kiedyś. Może jedno. A może nie.",
            "story_0.png"
        )
    elif score == 1:
        return (
            f"Niemożliwe! {PLAYER2_NAME} trafił! Ale tylko raz. I to przypadkiem. "
            "Następnego dnia obudził się sławny – gazety pisały: „Jedno dziecko, ale jakie!”. "
            f"{PLAYER1_NAME} wciąż ucieka, ale teraz z wózkiem.",
            "story_1.png"
        )
    elif score == 2:
        return (
            "Dwójka dzieci? Jedno codziennie ma obsrane gacie, drugie próbuje zjeść kota. "
            f"{PLAYER2_NAME}? Twierdzi, że jest gotów na trzecie. {PLAYER1_NAME}? Szuka paszportu i lotów last minute.",
            "story_2.png"
        )
    elif score == 3:
        return (
            f"{PLAYER1_NAME} robiła uniki jak ninja, ale {PLAYER2_NAME} był szybszy. "
            "Troje to już tłum! Krzyczą naraz, jedzą tapetę i nie uznają nocnej ciszy! "
            f"{PLAYER1_NAME} się śmieje. Nerwowo. Bardzo nerwowo.",
            "story_3.png"
        )
    elif score == 4:
        return (
            f"{PLAYER2_NAME} miał więcej determinacji niż baba na promocji w Lidlu! "
            f"{PLAYER1_NAME} nauczyła się medytować, a {PLAYER2_NAME} – przewijać jedno dziecko nogą, trzymając drugie zębami.",
            "story_4.png"
        )
    elif score == 5:
        return (
            f"{PLAYER2_NAME} włączył tryb 'Ojciec roku' i posłał pięć strzałów jak z kałasznikowa. "
            "Pięcioro dzieci! Troje już pisze kod w JavaScripcie, inne otwiera sklep z kawą, a ostatnie pisze autobiografię. "
            f"{PLAYER1_NAME}? Na terapii. {PLAYER2_NAME}? Szczęśliwy jak nigdy.",
            "story_5.png"
        )