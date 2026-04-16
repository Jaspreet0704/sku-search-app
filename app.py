#import streamlit as st
#import pandas as pd

#st.title("SKU Search App 🚀")

## Google Sheet CSV link (temporary example)
##url = "https://docs.google.com/spreadsheets/d/1J9GQA2pg8jSl0ydN0CeFVVIJz7bRVP9VyOIAh2hv_Vs/export?format=csv&gid=42975298"
#df = pd.read_csv(url, header=1, on_bad_lines='skip')
#df = df[["Image link 1", "New Color SKU", "Parent SKU", "Color 1", "Color 2", "Color (For Uniware)", "Primary category", "Amazon SKU", "Amazon Child ASIN", "FK SKU","FK FSN", "FK Listing ID", "AJIO SKU", "Ajio JioCode", "Ajio EAN", "Myntra SKU", "Myntra Style ID", "Meesho Catalog ID","Meesho Product ID"]]
##st.write("Columns:", df.columns)
#search = st.text_input("Enter SKU")

#if search:
 #   result = df[df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)]
    
  #  if not result.empty:
   #     row = result.iloc[0]
#    st.success("Data found ✅")

#       #st.image(row["Image"], width=550)
 #       img_url = str(row["Image link 1"])
  #  if pd.notna(img_url) and img_url != "":
   #     if "dropbox.com" in img_url:
    #        img_url = img_url.replace("www.dropbox.com", "dl.dropboxusercontent.com")
     #       img_url = img_url.split("?")[0]
      #  st.image(img_url, width=250)
    
    # #Convert dropbox link to direct image
  
    # #🧾 Basic Info
       # st.write("Parent SKU:", row["Parent SKU"])
        #st.write("New SKU:", row["New Color SKU"])

    # 🎨 #Colors
      #  st.write("Color:", row["Color 1"], "/", row["Color 2"])

      #  st.subheader("Platform SKUs")

    # #🛒 Platforms
       # st.write("Amazon SKU:", row["Amazon SKU"])
        #st.write("Flipkart SKU:", row["FK SKU"])
      #  st.write("Myntra SKU:", row["Myntra SKU"])
       ##st.write("Meesho Product ID:", row["Meesho Product ID"])
        
    #else:
     #   st.error("No data found ❌")




import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
st.title("SKU Search System")
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CLEAR FUNCTION ----------------
def clear_search():
    st.session_state.search = ""

# ---------------- DATA LOAD ----------------
url = "https://docs.google.com/spreadsheets/d/1J9GQA2pg8jSl0ydN0CeFVVIJz7bRVP9VyOIAh2hv_Vs/export?format=csv&gid=42975298"
img_sheet_url = "https://docs.google.com/spreadsheets/d/1Fohl2VC-u6RQZaUsslUTvEU3RvfXLBKZ/export?format=csv&gid=1702009625"

df = pd.read_csv(url, header=1, on_bad_lines='skip')
img_df = pd.read_csv(img_sheet_url)

df = df[[
    "Image link 1", "New Color SKU", "New SKU", "Parent SKU",
    "Color 1", "Color 2", "EAN CODE", "Box code",
    "Amazon SKU", "FK SKU", "AJIO SKU", "Myntra SKU",
    "Meesho Product ID", "Amazon Child ASIN", "Amazon Parent ASIN", "FK FSN", "FK Listing ID", "Ajio JioCode", "Ajio EAN", "Myntra Style ID", "Meesho Catalog ID", "Meesho Product ID"
]]

# ---------------- SEARCH BAR (TOP LEFT) ----------------
if "search" not in st.session_state:
    st.session_state.search = ""

col1, col2 = st.columns([0.5,1])

with col1:
    st.text_input("Enter SKU", key="search")

with col2:
    st.button("❌", on_click=clear_search)

# ---------------- SEARCH LOGIC ----------------
if st.session_state.search:
    search = st.session_state.search

    search = search.lower()
    result = df[
        df.apply(lambda col: col.astype(str).str.lower().str.contains(search, na=False)).any(axis=1)
        ]
    if not result.empty:
        row = result.iloc[0]
      

        # ---------------- MAIN LAYOUT ----------------
        left_col, right_col = st.columns([1,2])

        # -------- LEFT (IMAGE BELOW SEARCH) --------
        with left_col:
            color_sku = str(row["New Color SKU"]).strip()
            img_row = img_df[img_df["New Color SKU"] == color_sku]

            if not img_row.empty:
                img_url = img_row.iloc[0]["Image link"]
                st.image(img_url, width=220)
            else:
                st.warning("No image")

        # -------- RIGHT (ALL DATA TOP ALIGNED) --------
        with right_col:

            # TOP ROW
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.write("**Parent SKU**")
                st.write(row["Parent SKU"])
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

            # PLATFORM GRID
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.write("**EAN CODE**")
                st.write(row["EAN CODE"])
            with col2:
                st.write("**Box code**")
                st.write(row["Box code"])
            with col3:
                st.write("**Amazon SKU**")
                st.write(row["Amazon SKU"])
            with col4:
                st.write("**Amazon Child ASIN**")
                st.write(row["Amazon Child ASIN"])
            with col5:
                st.write("**Amazon Parent ASIN**")
                st.write(row["Amazon Parent ASIN"])

            st.markdown("---")

            col1, col2,col3 = st.columns(3)
            with col1:
                st.write("**Flipkart**")
                st.write(row["FK SKU"])
            with col2:
                st.write("**Myntra**")
                st.write(row["Myntra SKU"])
            with col3:
                st.write("**Ajio**")
                st.write(row["AJIO SKU"])

    else:
        st.error("No data found ❌")