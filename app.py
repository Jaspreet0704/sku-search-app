import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("SKU Search System")

# ---------------- CLEAR FUNCTION ----------------
def clear_search():
    st.session_state.search = ""

# ---------------- DATA LOAD ----------------
url = "https://docs.google.com/spreadsheets/d/1J9GQA2pg8jSl0ydN0CeFVVIJz7bRVP9VyOIAh2hv_Vs/export?format=csv&gid=42975298"

# ✅ FIXED IMAGE SHEET LINK
img_sheet_url = "https://docs.google.com/spreadsheets/d/1mBTa0m7gZ-57wbVf5kshc6hYNAT1o68HPzWsrlhd6cs/export?format=csv&gid=0"

df = pd.read_csv(url, header=1, on_bad_lines='skip')
img_df = pd.read_csv(img_sheet_url)

# ✅ CLEAN COLUMN NAMES (IMPORTANT)
img_df.columns = img_df.columns.str.strip()

df = df[[
    "Image link 1", "New Color SKU", "New SKU", "Parent SKU",
    "Color 1", "Color 2", "EAN CODE", "Box code",
    "Amazon SKU", "FK SKU", "AJIO SKU", "Myntra SKU",
    "Meesho Product ID", "Amazon Child ASIN", "Amazon Parent ASIN"
]]

# ---------------- SEARCH BAR ----------------
if "search" not in st.session_state:
    st.session_state.search = ""

col1, col2 = st.columns([0.5,1])

with col1:
    st.text_input("Enter SKU", key="search")

with col2:
    st.button("❌", on_click=clear_search)

# ---------------- SEARCH ----------------
if st.session_state.search:
    search = st.session_state.search.lower()

    result = df[
        df.apply(lambda col: col.astype(str).str.lower().str.contains(search, na=False)).any(axis=1)
    ]

    if not result.empty:
        row = result.iloc[0]

        # ---------------- MAIN LAYOUT ----------------
        left_col, right_col = st.columns([1,2])

        # -------- IMAGE --------
        with left_col:
            color_sku = str(row["New Color SKU"]).strip()

            # ✅ MATCH USING LINK SLUG
            img_row = img_df[
                img_df["Link slug"].astype(str).str.strip() == color_sku
            ]

            if not img_row.empty:
                img_url = str(img_row.iloc[0]["Original URL"]).strip()

                st.markdown(
                    f'<img src="{img_url}" style="width:100%; border-radius:10px;">',
                    unsafe_allow_html=True
                )
            else:
                st.warning("No image found")

        # -------- DATA --------
        with right_col:

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Parent SKU**")
                st.write(row["Parent SKU"])

                st.write("**New SKU**")
                st.write(row["New SKU"])

                st.write("**Color 2**")
                st.write(row["Color 2"])

                st.write("**Box code**")
                st.write(row["Box code"])

                st.write("**Amazon Child ASIN**")
                st.write(row["Amazon Child ASIN"])

                st.write("**Flipkart SKU**")
                st.write(row["FK SKU"])

                st.write("**Ajio SKU**")
                st.write(row["AJIO SKU"])

            with col2:
                st.write("**Color SKU**")
                st.write(row["New Color SKU"])

                st.write("**Color 1**")
                st.write(row["Color 1"])

                st.write("**EAN CODE**")
                st.write(str(row["EAN CODE"]).replace(".0", ""))

                st.write("**Amazon SKU**")
                st.write(row["Amazon SKU"])

                st.write("**Amazon Parent ASIN**")
                st.write(row["Amazon Parent ASIN"])

                st.write("**Myntra SKU**")
                st.write(row["Myntra SKU"])

                st.write("**Meesho Product ID**")
                st.write(row["Meesho Product ID"])

    else:
        st.error("No data found ❌")
