from mood_machine import MoodMachine

BREAKER_SENTENCES = [
    "Oh great, another meeting—my favorite way to spend a Tuesday.",
    "That concert was sick, honestly fire vibes all night.",
    "I'm fine 🙂",
    "I'm exhausted but proud of myself for getting through it.",
    "Wicked move—totally intentional.",
    "You want it done now? Sure, right after I finish breathing.",
    "He's mad? Nah, he's chill—kind of.",
    "This is literally the best worst idea I've ever had.",
    "I'm down, unless you're down, then I'm not.",
    "Cool, cool... no, really, cool.",
    "Sick? You mean ill, or amazing?",
    "I'm happy 😅 but also low-key worried.",
]


def run():
    mm = MoodMachine()
    for sent in BREAKER_SENTENCES:
        res = mm.analyze(sent)
        print("Sentence:", sent)
        print("Score:", res["score"])
        print("Contributions:")
        for tok, val, src in res["contributions"]:
            print(f"  {tok!r}: {val} ({src})")
        print("Ignored tokens:", res["ignored"]) 
        dom = res["dominant"]
        if dom:
            print("Dominant token:", dom)
        print("-" * 50)


if __name__ == "__main__":
    run()
