import requests
import difflib
import os
import json

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

WORD_LIST = [
    "aberration", "ambiguous", "analogy", "anecdote", "antagonist",
    "apathy", "articulate", "astute", "benevolent", "brevity",
    "candid", "catalyst", "coherent", "compassion", "concise",
    "condescending", "connotation", "contemplate", "context", "contradiction",
    "credible", "criteria", "critique", "cynical", "deduce",
    "deliberate", "diligent", "discrepancy", "disdain", "eloquent",
    "empathy", "enigma", "ephemeral", "ethics", "euphemism",
    "facade", "fallacy", "foreshadow", "frugal", "fundamental",
    "haphazard", "hypothesis", "ideology", "illuminate", "implicit",
    "inference", "integrity", "irony", "juxtapose", "latent",
    "legitimate", "lucid", "melancholy", "metaphor", "meticulous",
    "morale", "narrative", "neutral", "objective", "obsolete",
    "ominous", "opportunist", "optimism", "paradox", "perspective",
    "pessimism", "pragmatic", "precedent", "profound", "prolific",
    "propaganda", "rational", "relevant", "resilient", "rhetoric",
    "scrutinize", "serendipity", "skeptical", "sophisticated", "subjective",
    "subtle", "superficial", "tangible", "tenacious", "transparent",
    "trivial", "unanimous", "vague", "validate", "versatile",
    "viable", "vindicate", "virtue", "volatile", "zealous"
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def fetch_definition(word):
    try:
        response = requests.get(API_URL + word.lower(), timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        print("\n  ✗  No internet connection. Please check your network.\n")
        return None
    except requests.exceptions.Timeout:
        print("\n  ✗  Request timed out. Try again.\n")
        return None


def suggest_word(word):
    matches = difflib.get_close_matches(word.lower(), WORD_LIST, n=1, cutoff=0.6)
    return matches[0] if matches else None


def display_result(data):
    entry = data[0]
    word  = entry.get("word", "")
    phonetic = entry.get("phonetic", "")

    print(f"\n  ┌─────────────────────────────────────────┐")
    print(f"  │  {word.upper():<41}│")
    if phonetic:
        print(f"  │  {phonetic:<41}│")
    print(f"  └─────────────────────────────────────────┘")

    for meaning in entry.get("meanings", []):
        part = meaning.get("partOfSpeech", "")
        print(f"\n  [{part}]")
        for i, definition in enumerate(meaning.get("definitions", [])[:3], 1):
            defn = definition.get("definition", "")
            example = definition.get("example", "")
            print(f"\n  {i}. {defn}")
            if example:
                print(f'     e.g. "{example}"')

    synonyms = []
    for meaning in entry.get("meanings", []):
        synonyms.extend(meaning.get("synonyms", [])[:3])
    if synonyms:
        print(f"\n  Synonyms: {', '.join(synonyms[:5])}")

    print()


def main():
    clear()
    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║         ENGLISH DICTIONARY               ║")
    print("  ║   Powered by Free Dictionary API         ║")
    print("  ╚══════════════════════════════════════════╝")
    print("\n  Type any word to look it up.")
    print("  Type  'list'  to see all preloaded words.")
    print("  Type  'q'     to quit.\n")

    while True:
        try:
            word = input("  Search: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye! 👋\n")
            break

        if not word:
            continue

        if word.lower() == "q":
            print("\n  Goodbye! 👋\n")
            break

        if word.lower() == "list":
            print("\n  Preloaded words:\n")
            for i, w in enumerate(WORD_LIST, 1):
                end = "\n" if i % 5 == 0 else "  "
                print(f"  {w:<18}", end=end)
            print("\n")
            continue

        data = fetch_definition(word)

        if data:
            display_result(data)
        else:
            suggestion = suggest_word(word)
            if suggestion:
                print(f"\n  ✗  '{word}' not found.")
                print(f"  Did you mean: '{suggestion}'? (y/n) ", end="")
                try:
                    confirm = input().strip().lower()
                except (KeyboardInterrupt, EOFError):
                    break
                if confirm == "y":
                    data = fetch_definition(suggestion)
                    if data:
                        display_result(data)
                    else:
                        print(f"\n  ✗  Could not find '{suggestion}' either.\n")
                else:
                    print()
            else:
                print(f"\n  ✗  '{word}' not found and no close match available.\n")


if __name__ == "__main__":
    main()