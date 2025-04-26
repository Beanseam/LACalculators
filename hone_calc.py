import streamlit as st
import math
# Percentage increases by .05 of the percentage created by the honing attempt
# Artisian Energy = Honing Percfentage * .465

def expected_attempts_t3(p_start=0.03, p_increment=0.0015, p_max=1.0, threshold=1e-10,
                         hone_gold=1100, hone_books=0, hone_oreha=0, num_oreha=12,
                         hone_leapstone=0, num_leapstone=19, hone_solar=200, total_gold=0):
    expected = 0.0
    cumulative_failure = 1.0
    n = 1
    cur_p = p_start
    expected_books_used = 0.0

    while True:
        book_worthwhile = (hone_books * p_start) <= (cur_p * hone_gold + hone_oreha * num_oreha + hone_leapstone * num_leapstone)

        if book_worthwhile:
            expected_books_used += cumulative_failure
            cur_p = min(cur_p + 2 * p_increment, p_max)
        else:
            cur_p = min(cur_p + p_increment, p_max)

        prob_success = cumulative_failure * cur_p
        contribution = n * prob_success
        expected += contribution

        if contribution < threshold:
            break

        cumulative_failure *= (1 - cur_p)
        n += 1

    num_hones = math.ceil(expected)
    num_books_used = round(expected_books_used)
    num_oreha_used = num_hones * num_oreha
    num_leapstone_used = num_hones * num_leapstone
    total_gold = (
        num_hones * hone_gold +
        num_books_used * hone_books +
        num_oreha_used * hone_oreha +
        num_leapstone_used * hone_leapstone
    )

    return num_hones, num_books_used, num_oreha_used, num_leapstone_used, 0, round(total_gold)

#Expecting to reach 100% artisan energy
def optimal_honing_attempts_t3(p_start=3, p_increment=0.15, hone_gold = 1100, hone_books = 0, 
                               hone_oreha = 0, num_oreha = 12, hone_leapstone = 0, num_leapstone = 19, 
                               hone_solar = 200, total_gold = 0):
    required_percentage = 100 / .465
    cur_p = p_start
    num_hones = 0
    num_books_used = 0
    num_oreha_used = 0
    num_leapstone_used = 0
    num_solar = 0
    while required_percentage > 0:
        book_worthwhile = (hone_books * p_start) <= (cur_p * hone_gold + hone_oreha * num_oreha + hone_leapstone * num_leapstone) # checks if using books is worth less gold than honing
        if required_percentage - cur_p <= 0:
            num_hones += 1
            num_oreha_used += num_oreha
            num_leapstone_used += num_leapstone
            required_percentage = 0
            break
        elif required_percentage - cur_p - .17*6 <= 0:
            while required_percentage - cur_p - .17*num_solar > 0:
                num_solar += 1
            if (num_solar * hone_solar <= hone_gold + hone_oreha * num_oreha + hone_leapstone * num_leapstone):
                num_hones += 1
                num_oreha_used += num_oreha
                num_leapstone_used += num_leapstone
                required_percentage = 0
            elif book_worthwhile:
                num_books_used += 1
                num_hones += 1
                num_oreha_used += num_oreha
                num_leapstone_used += num_leapstone
                required_percentage = 0
            else:
                num_hones += 2
                num_oreha_used += 2*num_oreha
                num_leapstone_used += 2*num_leapstone
                required_percentage = 0
            break
        elif required_percentage - cur_p - p_start <= 0 & book_worthwhile:
            num_books_used += 1
            num_hones += 1
            num_oreha_used += num_oreha
            num_leapstone_used += num_leapstone
            required_percentage = 0
            break
        elif book_worthwhile:
            bonus_percent = p_increment * 2
            cur_p += bonus_percent
            required_percentage -= (cur_p + p_start)
            num_books_used += 1
            num_hones += 1
            num_oreha_used += num_oreha
            num_leapstone_used += num_leapstone
        else:
            cur_p += p_increment
            required_percentage -= cur_p
            num_hones += 1
            num_oreha_used += num_oreha
            num_leapstone_used += num_leapstone
    total_gold = (num_hones * hone_gold) + (num_books_used * hone_books) + (num_oreha_used * hone_oreha) + (num_leapstone_used * hone_leapstone) + (num_solar * hone_solar)
    return num_hones, num_books_used, num_oreha_used, num_leapstone_used, num_solar, total_gold

presets_armor_t3 = {
    13 : {"p_start": 10, "p_increment": .5, "hone_gold": 656, "num_oreha": 4, "num_leapstone": 10},
    14 : {"p_start": 5, "p_increment": .25, "hone_gold": 688, "num_oreha": 6, "num_leapstone": 11},
    15 : {"p_start": 5, "p_increment": .25, "hone_gold": 728, "num_oreha": 6, "num_leapstone": 12},
    16 : {"p_start": 4, "p_increment": .2, "hone_gold": 970, "num_oreha": 7, "num_leapstone": 15},
    17 : {"p_start": 4, "p_increment": .2, "hone_gold": 1030, "num_oreha": 7, "num_leapstone": 18},
    18 : {"p_start": 3, "p_increment": .15, "hone_gold": 1100, "num_oreha": 12, "num_leapstone": 19},
    19 : {"p_start": 3, "p_increment": .15, "hone_gold": 1190, "num_oreha": 12, "num_leapstone": 21}
}

presets_weapon_t3 = {
    13 : {"p_start": 10, "p_increment": .5, "hone_gold": 1088, "num_oreha": 7, "num_leapstone": 16},
    14 : {"p_start": 5, "p_increment": .25, "hone_gold": 1144, "num_oreha": 10, "num_leapstone": 16},
    15 : {"p_start": 5, "p_increment": .25, "hone_gold": 1216, "num_oreha": 10, "num_leapstone": 17},
    16 : {"p_start": 4, "p_increment": .2, "hone_gold": 1610, "num_oreha": 12, "num_leapstone": 22},
    17 : {"p_start": 4, "p_increment": .2, "hone_gold": 1720, "num_oreha": 12, "num_leapstone": 24},
    18 : {"p_start": 3, "p_increment": .15, "hone_gold": 1840, "num_oreha": 20, "num_leapstone": 26},
    19 : {"p_start": 3, "p_increment": .15, "hone_gold": 1980, "num_oreha": 20, "num_leapstone": 28}
}

armor_parts = ["Helm", "Shoulders", "Chestpiece", "Pants", "Gloves"]
weapon_part = ["Weapon"]
levels = list(range(13, 20))

st.title("Lost Ark Honing Calculator")

# Material and Cost Inputs
st.sidebar.header("Input Additional Material Costs")
hone_books = st.sidebar.number_input("Honing Book Price", value=0)
hone_oreha = st.sidebar.number_input("Oreha Fusion Material Price", value=0)
hone_leapstone = st.sidebar.number_input("Leapstone Price", value=0)
hone_solar = st.sidebar.number_input("Solar Grace/Protection Price", value=200)

# Method selection
method = st.sidebar.radio("Select Calculation Method", ("Expected Odds", "Optimal Pity"))

# Table Grid
selections = {}
st.write("### Select Items to Hone:")
cols = st.columns([1] + [1 for _ in levels])
cols[0].markdown("**Part / +Level**")
for i, level in enumerate(levels):
    cols[i+1].markdown(f"**+{level}**")

# Armor rows
for part in armor_parts:
    row = st.columns([1] + [1 for _ in levels])
    row[0].markdown(f"**{part}**")
    for i, level in enumerate(levels):
        selections[(part, level)] = row[i+1].checkbox("", key=f"{part}_{level}")

# Weapon row
row = st.columns([1] + [1 for _ in levels])
row[0].markdown("**Weapon**")
for i, level in enumerate(levels):
    selections[("Weapon", level)] = row[i+1].checkbox("", key=f"Weapon_{level}")

# Process button
if st.button("Calculate Honing Costs"):
    total_hones = 0
    total_books = 0
    total_oreha = 0
    total_leapstone = 0
    total_solar = 0
    total_gold_cost = 0

    for (part, level), selected in selections.items():
        if selected:
            if part == "Weapon":
                preset = presets_weapon_t3.get(level)
            else:
                preset = presets_armor_t3.get(level)

            if preset:
                if method == "Optimal Pity":
                    result = optimal_honing_attempts_t3(
                        p_start=preset["p_start"],
                        p_increment=preset["p_increment"],
                        hone_gold=preset["hone_gold"],
                        hone_books=hone_books,
                        hone_oreha=hone_oreha,
                        num_oreha=preset["num_oreha"],
                        hone_leapstone=hone_leapstone,
                        num_leapstone=preset["num_leapstone"],
                        hone_solar=hone_solar
                    )
                else:
                    result = expected_attempts_t3(
                        p_start=preset["p_start"] / 100,
                        p_increment=preset["p_increment"] / 100,
                        hone_gold=preset["hone_gold"],
                        hone_books=hone_books,
                        hone_oreha=hone_oreha,
                        num_oreha=preset["num_oreha"],
                        hone_leapstone=hone_leapstone,
                        num_leapstone=preset["num_leapstone"],
                        hone_solar=hone_solar
                    )

                num_hones, num_books_used, num_oreha_used, num_leapstone_used, num_solar, total_gold = result
                total_hones += num_hones
                total_books += num_books_used
                total_oreha += num_oreha_used
                total_leapstone += num_leapstone_used
                total_solar += num_solar
                total_gold_cost += total_gold

    st.success(f"Total Honing Attempts: {total_hones}")
    st.success(f"Total Books Used: {total_books}")
    st.success(f"Total Oreha Used: {total_oreha}")
    st.success(f"Total Leapstone Used: {total_leapstone}")
    st.success(f"Total Solar Materials Used: {total_solar}")
    st.success(f"Total Gold Cost: {total_gold_cost:,.0f}g")