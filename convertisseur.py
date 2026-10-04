#!/usr/bin/env python3
"""
Convertisseur Universel - Projet 03 de la Forteresse YUAN.
Conversion entre unites de longueur, masse, temperature, temps, volume, devises.
"""

import sys


# ============================================================
# DONNEES DE CONVERSION
# ============================================================

LONGUEURS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "miles": 1609.344,
    "pieds": 0.3048,
    "pouces": 0.0254,
    "yards": 0.9144,
}

MASSES = {
    "kg": 1.0,
    "g": 0.001,
    "mg": 0.000001,
    "tonnes": 1000.0,
    "livres": 0.45359237,
    "onces": 0.028349523125,
}

TEMPS = {
    "secondes": 1.0,
    "minutes": 60.0,
    "heures": 3600.0,
    "jours": 86400.0,
}

VOLUMES = {
    "L": 1.0,
    "mL": 0.001,
    "m3": 1000.0,
    "gallons_us": 3.785411784,
    "pintes_us": 0.473176473,
}

DEVISES = {
    "EUR": 1.0,
    "USD": 1.08,
    "XOF": 655.957,
    "GBP": 0.85,
}


# ============================================================
# CONVERSION TEMPERATURE
# ============================================================

def convertir_temperature(valeur, source, cible):
    """Convertit une temperature entre C, F, K."""
    if source == "C":
        celsius = valeur
    elif source == "F":
        celsius = (valeur - 32) * 5 / 9
    elif source == "K":
        celsius = valeur - 273.15
    else:
        raise ValueError(f"Unite source inconnue : {source}")

    if cible == "C":
        return celsius
    elif cible == "F":
        return celsius * 9 / 5 + 32
    elif cible == "K":
        return celsius + 273.15
    else:
        raise ValueError(f"Unite cible inconnue : {cible}")


# ============================================================
# UTILITAIRES
# ============================================================

def convertir(valeur, source, cible, table):
    """Conversion generique via facteurs."""
    if source not in table:
        raise ValueError(f"Unite source inconnue : {source}")
    if cible not in table:
        raise ValueError(f"Unite cible inconnue : {cible}")
    return valeur * (table[cible] / table[source])


def afficher_menu(titre, options, retour=True):
    """Affiche un menu numerote et retourne le choix."""
    print()
    print("=" * 50)
    print(f"  {titre}")
    print("=" * 50)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    if retour:
        print("  0. Retour")
    print("=" * 50)

    while True:
        try:
            choix = input("Ton choix : ").strip()
            if retour and choix == "0":
                return None
            idx = int(choix) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print("Choix invalide.")
        except ValueError:
            print("Entre un nombre.")


def demander_valeur(prompt="Valeur a convertir : "):
    """Demande une valeur numerique."""
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Entre un nombre valide.")


# ============================================================
# MENUS
# ============================================================

def menu_conversion_generique(nom, table):
    """Menu generique pour longueurs, masses, temps, volumes."""
    unites = list(table.keys())

    source = afficher_menu(f"{nom} - Unite SOURCE", unites)
    if source is None:
        return

    cible = afficher_menu(f"{nom} - Unite CIBLE", unites)
    if cible is None:
        return

    valeur = demander_valeur(f"Valeur en {source} : ")

    try:
        resultat = convertir(valeur, source, cible, table)
        print(f"\n[OK] {valeur} {source} = {resultat:.6g} {cible}")
    except ValueError as e:
        print(f"[ERREUR] {e}")


def menu_temperature():
    """Menu specifique temperature."""
    unites = ["C", "F", "K"]

    source = afficher_menu("Temperature - Unite SOURCE", unites)
    if source is None:
        return

    cible = afficher_menu("Temperature - Unite CIBLE", unites)
    if cible is None:
        return

    valeur = demander_valeur(f"Valeur en deg{source} : ")

    try:
        resultat = convertir_temperature(valeur, source, cible)
        print(f"\n[OK] {valeur}deg{source} = {resultat:.4f}deg{cible}")
    except ValueError as e:
        print(f"[ERREUR] {e}")


def menu_devises():
    """Menu specifique devises."""
    unites = list(DEVISES.keys())

    source = afficher_menu("Devise - SOURCE", unites)
    if source is None:
        return

    cible = afficher_menu("Devise - CIBLE", unites)
    if cible is None:
        return

    valeur = demander_valeur(f"Montant en {source} : ")

    try:
        resultat = convertir(valeur, source, cible, DEVISES)
        print(f"\n[OK] {valeur} {source} = {resultat:.2f} {cible}")
        print("   (taux indicatifs)")
    except ValueError as e:
        print(f"[ERREUR] {e}")


def menu_principal():
    """Menu principal."""
    while True:
        categorie = afficher_menu(
            "CONVERTISSEUR UNIVERSEL",
            [
                "Longueurs",
                "Masses",
                "Temperatures",
                "Temps",
                "Volumes",
                "Devises",
                "Quitter"
            ],
            retour=False
        )

        if categorie == "Quitter":
            print("\nAu revoir !")
            break
        elif categorie == "Longueurs":
            menu_conversion_generique("Longueurs", LONGUEURS)
        elif categorie == "Masses":
            menu_conversion_generique("Masses", MASSES)
        elif categorie == "Temperatures":
            menu_temperature()
        elif categorie == "Temps":
            menu_conversion_generique("Temps", TEMPS)
        elif categorie == "Volumes":
            menu_conversion_generique("Volumes", VOLUMES)
        elif categorie == "Devises":
            menu_devises()


def main():
    """Point d'entree."""
    print()
    print("=" * 50)
    print("  CONVERTISSEUR UNIVERSEL v1.0")
    print("  Projet 03 - Forteresse YUAN")
    print("=" * 50)

    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nInterrompu. Au revoir !")
        return 1
    except Exception as e:
        print(f"\n[FATAL] {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
