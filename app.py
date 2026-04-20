import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("SKU Search System")

# ---------------- CLEAR FUNCTION ----------------
def clear_search():
    st.session_state.search = ""

# ---------------- DATA LOAD ----------------
url = "https://docs.google.com/spreadsheets/d/1J9GQA2pg8jSl0ydN0CeFVVIJz7bRVP9VyOIAh2hv_Vs/export?format=csv&gid=42975298"
img_sheet_url = "https://docs.google.com/spreadsheets/d/1mBTa0m7gZ-57wbVf5kshc6hYNAT1o68HPzWsrlhd6cs/export?format=csv&gid=0"
link_sheet_url = "https://docs.google.com/spreadsheets/d/1J9GQA2pg8jSl0ydN0CeFVVIJz7bRVP9VyOIAh2hv_Vs/export?format=csv&gid=565493070"
link_df = pd.read_csv(link_sheet_url, header=1,on_bad_lines='skip')
link_df.columns = link_df.columns.str.strip()

df = pd.read_csv(url, header=1, on_bad_lines='skip')
img_df = pd.read_csv(img_sheet_url)

img_df.columns = img_df.columns.str.strip()

df = df[[
    "Image link 1", "New Color SKU", "New SKU", "Parent SKU",
    "Color 1", "Color 2", "EAN CODE", "Box code",
    "Amazon SKU", "FK SKU", "AJIO SKU", "Myntra SKU",
    "Meesho Catalog ID", "Amazon Child ASIN", "Amazon Parent ASIN"
]]

# ---------------- SEARCH BAR ----------------
if "search" not in st.session_state:
    st.session_state.search = ""

col1, col2, col3 = st.columns([1,2,1])

with col1:
    search_column = st.selectbox(
        "Search Field",
        [
            "New SKU",
            "Parent SKU",
            "New Color SKU",
            "EAN CODE",
            "Amazon SKU", "Amazon Child ASIN", "Amazon Parent ASIN",
            "FK SKU",
            "Myntra SKU",
            "AJIO SKU",  
            "Meesho Catalog ID"
        ]
    )

with col2:
    st.text_input("Enter Value", key="search")

with col3:
    st.button("❌", on_click=clear_search)

# ---------------- SEARCH ----------------
if st.session_state.search:
    search = st.session_state.search.lower()
    
    result = df[df[search_column].astype(str).str.lower().str.contains(search, na=False)]

    if not result.empty:
        row = result.iloc[0]
        color_sku = str(row["New Color SKU"]).strip()
        link_row = link_df[link_df["New Color SKU"].astype(str).str.strip() == color_sku]
        if not link_row.empty:
            link_row = link_row.iloc[0]
            
            amazon_link = link_row.get("Amazon Link", "")
            flipkart_link = link_row.get("Flipkart Link", "")
            myntra_link = link_row.get("Myntra Link", "")
            ajio_link = link_row.get("Ajio Link", "")
            meesho_link = link_row.get("Meesho Link", "")
        else:
            amazon_link = flipkart_link = myntra_link = ajio_link = meesho_link = ""

        # ---------------- MAIN LAYOUT ----------------
        left_col, right_col = st.columns([1,2])

        # -------- IMAGE --------
        with left_col:
            color_sku = str(row["New Color SKU"]).strip()

            img_row = img_df[
                img_df["Link slug"].astype(str).str.strip() == color_sku
            ]

            if not img_row.empty:
                img_url = str(img_row.iloc[0]["Original URL"]).strip()

                # Dropbox FIX for iPhone
                if "dropbox.com" in img_url:
                    if "dl=1" in img_url:
                        img_url = img_url.replace("dl=1", "raw=1")
                    elif "dl=0" in img_url:
                        img_url = img_url.replace("dl=0", "raw=1")
                    else:
                        img_url = img_url + "&raw=1"

                st.markdown(
                    f'<img src="{img_url}" style="width:100%; border-radius:10px;">',
                    unsafe_allow_html=True
                )
            else:
                st.warning("No image found")

        # -------- DATA --------
        with right_col:

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.write("**Parent SKU**")
                st.write(str(row["Parent SKU"]))
            with col2:
                st.write("**Color SKU**") 
                st.write(row["New Color SKU"])
            with col3:
                st.write("**New SKU**")
                st.write(row["New SKU"])
            with col4: 
                st.write("**Color 1**") 
                st.write(row["Color 1"]) 
            with col5: 
                st.write("**Color 2**") 
                st.write(row["Color 2"])

            st.markdown("---")

            col1, col2, col3, col4, col5 = st.columns(5)
                
            with col1: 
                st.write("**EAN CODE**") 
                st.write(str(row["EAN CODE"]).replace(".0", ""))
            with col2:
                st.write("**Box code**")
                st.write(row["Box code"])
            with col3:
                if amazon_link:
                    st.markdown(f"**Amazon SKU**  [🔗]({amazon_link})")
                    st.write(row["Amazon SKU"])
                else:
                    st.write("**Amazon SKU**", row["Amazon SKU"])
            with col4:
                st.write("**Amazon Child ASIN**")
                st.write(row["Amazon Child ASIN"])
            with col5:
                st.write("**Amazon Parent ASIN**")
                st.write(row["Amazon Parent ASIN"])

            st.markdown("---")

            col1, col2,col3, col4 = st.columns(4)

            with col1:
                if amazon_link:
                    st.markdown(f"**Flipkart SKU**  [🔗]({flipkart_link})")
                    st.write(row["FK SKU"])
                else:
                    st.write("**Flipkart SKU**", row["FK SKU"])
            with col2: 
                if amazon_link:
                    st.markdown(f"**Myntra SKU**  [🔗]({myntra_link})")
                    st.write(row["Myntra SKU"])
                else:
                    st.write("**Myntra SKU**", row["Myntra SKU"])
            with col3: 
                if amazon_link:
                    st.markdown(f"**AJIO SKU**  [🔗]({ajio_link})")
                    st.write(row["AJIO SKU"])
                else:
                    st.write("**AJIO SKU**", row["AJIO SKU"])
            with col4:
                if amazon_link:
                    st.markdown(f"**Meesho Catalog ID**  [🔗]({meesho_link})")
                    st.write(str(row["Meesho Catalog ID"]).replace(".0",""))
                else:
                    st.write("**Meesho Catalog ID**", str(row["Meesho Catalog ID"]).replace(".0",""))

    else:
        st.error("No data found ❌")

