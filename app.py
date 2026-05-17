import streamlit as st

# ============================================
# AMINO ACID MASS TABLE
# ============================================

aa_mass = {
    "A": 71.08,
    "R": 156.19,
    "N": 114.10,
    "D": 115.09,
    "C": 103.15,
    "E": 129.12,
    "Q": 128.13,
    "G": 57.05,
    "H": 137.14,
    "I": 113.16,
    "L": 113.16,
    "K": 128.17,
    "M": 131.19,
    "F": 147.18,
    "P": 97.12,
    "S": 87.08,
    "T": 101.11,
    "W": 186.21,
    "Y": 163.18,
    "V": 99.13
}

# ============================================
# HYDROPHOBICITY TABLE
# ============================================

hydro_table = {
    "A": 1.8,
    "R": -4.5,
    "N": -3.5,
    "D": -3.5,
    "C": 2.5,
    "Q": -3.5,
    "E": -3.5,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "L": 3.8,
    "K": -3.9,
    "M": 1.9,
    "F": 2.8,
    "P": -1.6,
    "S": -0.8,
    "T": -0.7,
    "W": -0.9,
    "Y": -1.3,
    "V": 4.2
}

# ============================================
# FUNCTIONS
# ============================================

def pep_mw(seq):
    mw = 18.015

    for aa in seq:
        if aa in aa_mass:
            mw += aa_mass[aa]

    return round(mw, 2)


def hydrophobicity(seq):
    total = 0

    for aa in seq:
        if aa in hydro_table:
            total += hydro_table[aa]

    return round(total / len(seq), 2)


def net_charge(seq):
    positive = seq.count("K") + seq.count("R")
    negative = seq.count("D") + seq.count("E")

    return positive - negative


def aggregation_score(seq):

    score = (
        seq.count("V")
        + seq.count("I")
        + seq.count("L")
        + seq.count("F")
        + seq.count("W")
    )

    if score >= 10:
        return "HIGH"
    elif score >= 5:
        return "MEDIUM"
    else:
        return "LOW"


def aspartimide_risk(seq):

    motifs = ["DG", "DS", "DT", "NG"]

    for m in motifs:
        if m in seq:
            return "YES - ASPARTIMIDE RISK"

    return "LOW"


def oxidation_risk(seq):

    if "M" in seq or "W" in seq or "C" in seq:
        return "YES - OXIDATION POSSIBLE"

    return "LOW"


def pseudoproline(seq):

    motifs = ["SS", "TT", "TS", "ST"]

    for m in motifs:
        if m in seq:
            return "RECOMMENDED"

    return "NOT REQUIRED"


def difficult_coupling(seq):

    motifs = ["GG", "FF", "VV", "II", "LL"]

    for m in motifs:
        if m in seq:
            return "HIGH RISK"

    return "NORMAL"


def difficulty_score(seq):

    score = 0

    if len(seq) > 30:
        score += 2

    if len(seq) > 50:
        score += 3

    score += seq.count("V")
    score += seq.count("I")
    score += seq.count("L")

    if "DG" in seq:
        score += 3

    if "GG" in seq:
        score += 2

    if "FF" in seq:
        score += 2

    if score <= 5:
        return "EASY"

    elif score <= 10:
        return "MODERATE"

    elif score <= 20:
        return "DIFFICULT"

    else:
        return "VERY DIFFICULT"


def deletion_mass(seq):

    result = ""

    for aa in seq:
        if aa in aa_mass:
            result += f"{aa}-{aa_mass[aa]}; "

    return result


# ============================================
# STREAMLIT UI
# ============================================

st.title("PEPTIDE PREDICTION TOOL")

st.write("Developed by Himanshu Singh")

sequence = st.text_input("Enter Peptide Sequence")

if sequence:

    sequence = sequence.upper()

    st.subheader("RESULTS")

    st.write(f"Sequence Length: {len(sequence)}")

    st.write(f"Molecular Weight: {pep_mw(sequence)}")

    st.write(f"Hydrophobicity: {hydrophobicity(sequence)}")

    st.write(f"Net Charge: {net_charge(sequence)}")

    st.write(f"Aggregation Score: {aggregation_score(sequence)}")

    st.write(f"Aspartimide Risk: {aspartimide_risk(sequence)}")

    st.write(f"Oxidation Risk: {oxidation_risk(sequence)}")

    st.write(f"PseudoProline Suggestion: {pseudoproline(sequence)}")

    st.write(f"Difficult Coupling: {difficult_coupling(sequence)}")

    st.write(f"Overall Difficulty: {difficulty_score(sequence)}")

    st.subheader("Deletion Mass Table")

    st.write(deletion_mass(sequence))