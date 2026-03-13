"""
Stuttgart Eats — Restaurant Finder for International Students
==============================================================
A simple tool to find affordable, good restaurants in Stuttgart
with filters for cuisine, budget, and dietary preferences.
Built because I needed this when I first moved here.

Author: Aishwarya Sonawane
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stuttgart Eats", page_icon="🍛", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem;}
    .restaurant-card {background: #f8f9fa; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #CFA64E;}
    .price-tag {background: #e8f5e9; color: #2e7d32; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;}
    .rating-tag {color: #f59e0b; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# RESTAURANT DATA — personally curated
# ============================================================
@st.cache_data
def load_restaurants():
    """
    Curated restaurant list for Stuttgart. 
    Mix of personal visits and Google Maps research.
    Prices and ratings as of early 2026.
    """
    data = [
        # Indian
        {"name": "Namaste India", "cuisine": "Indian", "area": "Mitte", "price_range": "€8–14",
         "avg_price": 11, "rating": 4.5, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Solid thali for under €10. Lunch buffet is the move."},
        {"name": "Taj Mahal", "cuisine": "Indian", "area": "Bad Cannstatt", "price_range": "€9–15",
         "avg_price": 12, "rating": 4.3, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Best biryani in Stuttgart. Not fancy, but authentic."},
        {"name": "Chennai Masala", "cuisine": "Indian", "area": "Vaihingen", "price_range": "€7–12",
         "avg_price": 9, "rating": 4.4, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "South Indian dosa and idli. Closest to home cooking."},
        
        # German
        {"name": "Platzhirsch", "cuisine": "German", "area": "Mitte", "price_range": "€10–18",
         "avg_price": 14, "rating": 4.3, "vegetarian": False, "vegan_options": False,
         "student_friendly": False, "note": "Maultaschen done right. Go for the Swabian classics."},
        {"name": "Stuttgarter Stäffele", "cuisine": "German", "area": "Süd", "price_range": "€9–16",
         "avg_price": 12, "rating": 4.4, "vegetarian": False, "vegan_options": False,
         "student_friendly": True, "note": "Great Schnitzel, reasonable prices for the quality."},
        {"name": "Brauhaus Schönbuch", "cuisine": "German", "area": "Mitte", "price_range": "€10–17",
         "avg_price": 13, "rating": 4.2, "vegetarian": False, "vegan_options": False,
         "student_friendly": True, "note": "House-brewed beer + traditional food. Tourist-y but good."},
        
        # Asian
        {"name": "Mandu", "cuisine": "Korean", "area": "Mitte", "price_range": "€8–14",
         "avg_price": 11, "rating": 4.5, "vegetarian": False, "vegan_options": True,
         "student_friendly": True, "note": "Bibimbap that actually fills you up. Fast service."},
        {"name": "Lemon Leaf", "cuisine": "Thai", "area": "West", "price_range": "€9–15",
         "avg_price": 12, "rating": 4.6, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Green curry is exceptional. Small place, go early."},
        {"name": "Tokyo Dining", "cuisine": "Japanese", "area": "Mitte", "price_range": "€10–20",
         "avg_price": 15, "rating": 4.4, "vegetarian": False, "vegan_options": False,
         "student_friendly": False, "note": "Good ramen, pricey but worth it occasionally."},
        {"name": "Pho Saigon", "cuisine": "Vietnamese", "area": "Bad Cannstatt", "price_range": "€7–12",
         "avg_price": 9, "rating": 4.3, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Best pho in the city. Huge portions, tiny prices."},
        
        # Mediterranean & Middle Eastern
        {"name": "Café Galao", "cuisine": "Portuguese", "area": "Heslach", "price_range": "€5–10",
         "avg_price": 7, "rating": 4.5, "vegetarian": False, "vegan_options": False,
         "student_friendly": True, "note": "Coffee + pastéis = perfect afternoon. Under €8 always."},
        {"name": "Damaskus", "cuisine": "Syrian", "area": "Mitte", "price_range": "€6–11",
         "avg_price": 8, "rating": 4.6, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Falafel plate is €7 and it's massive. Best value in town."},
        {"name": "Mezze House", "cuisine": "Lebanese", "area": "West", "price_range": "€8–14",
         "avg_price": 11, "rating": 4.4, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Sharing mezze plates with friends — the way to go."},
        
        # Italian
        {"name": "Da Franco", "cuisine": "Italian", "area": "Süd", "price_range": "€9–16",
         "avg_price": 12, "rating": 4.5, "vegetarian": True, "vegan_options": False,
         "student_friendly": True, "note": "Real Neapolitan pizza. Cash only. Worth the trip."},
        {"name": "Trattoria da Enzo", "cuisine": "Italian", "area": "Mitte", "price_range": "€10–18",
         "avg_price": 14, "rating": 4.3, "vegetarian": True, "vegan_options": False,
         "student_friendly": False, "note": "Pasta is handmade daily. Date night spot, not budget."},
        
        # Vegetarian / Vegan
        {"name": "Vegi", "cuisine": "Vegetarian", "area": "Mitte", "price_range": "€6–10",
         "avg_price": 8, "rating": 4.4, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Cheapest good lunch in city center. Daily changing menu."},
        {"name": "Body Kitchen", "cuisine": "Health Food", "area": "Mitte", "price_range": "€8–14",
         "avg_price": 11, "rating": 4.2, "vegetarian": True, "vegan_options": True,
         "student_friendly": True, "note": "Bowl-style meals. Good after gym. A bit Instagram-y."},
    ]
    return pd.DataFrame(data)

df = load_restaurants()

# ============================================================
# HEADER
# ============================================================
st.title("🍛 Stuttgart Eats")
st.markdown("A curated restaurant guide for international students in Stuttgart. Personally tested, honestly reviewed.")
st.markdown("---")

# ============================================================
# FILTERS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    cuisine_filter = st.multiselect(
        "🍽️ Cuisine",
        options=sorted(df["cuisine"].unique()),
        default=[]
    )

with col2:
    budget = st.selectbox(
        "💰 Budget",
        ["All", "Under €10", "Under €12", "Under €15"]
    )

with col3:
    dietary = st.multiselect(
        "🥗 Dietary",
        ["Vegetarian", "Vegan Options"],
        default=[]
    )

with col4:
    student_only = st.checkbox("🎓 Student-friendly only", value=False)

# Apply filters
filtered = df.copy()

if cuisine_filter:
    filtered = filtered[filtered["cuisine"].isin(cuisine_filter)]

if budget == "Under €10":
    filtered = filtered[filtered["avg_price"] <= 10]
elif budget == "Under €12":
    filtered = filtered[filtered["avg_price"] <= 12]
elif budget == "Under €15":
    filtered = filtered[filtered["avg_price"] <= 15]

if "Vegetarian" in dietary:
    filtered = filtered[filtered["vegetarian"] == True]
if "Vegan Options" in dietary:
    filtered = filtered[filtered["vegan_options"] == True]

if student_only:
    filtered = filtered[filtered["student_friendly"] == True]

# Sort
sort_by = st.radio("Sort by", ["Rating ⭐", "Price 💰", "Name"], horizontal=True)
if sort_by == "Rating ⭐":
    filtered = filtered.sort_values("rating", ascending=False)
elif sort_by == "Price 💰":
    filtered = filtered.sort_values("avg_price")
else:
    filtered = filtered.sort_values("name")

# ============================================================
# RESULTS
# ============================================================
st.markdown(f"### Showing {len(filtered)} restaurants")

if filtered.empty:
    st.info("No restaurants match your filters. Try broadening your search.")
else:
    # Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Price", f"€{filtered['avg_price'].mean():.0f}")
    c2.metric("Avg Rating", f"⭐ {filtered['rating'].mean():.1f}")
    c3.metric("Student-Friendly", f"{filtered['student_friendly'].sum()}/{len(filtered)}")
    
    st.markdown("")
    
    # Cards
    for _, r in filtered.iterrows():
        budget_color = "#2e7d32" if r['avg_price'] <= 10 else "#e65100" if r['avg_price'] > 14 else "#f57f17"
        
        col_a, col_b = st.columns([3, 1])
        
        with col_a:
            st.markdown(f"""
            **{r['name']}** · {r['cuisine']} · 📍 {r['area']}  
            ⭐ **{r['rating']}** · {r['price_range']}
            {"🥗 Vegetarian" if r['vegetarian'] else ""} {"🌱 Vegan options" if r['vegan_options'] else ""} {"🎓 Student-friendly" if r['student_friendly'] else ""}  
            *"{r['note']}"*
            """)
        
        with col_b:
            st.markdown(f"""
            <div style='text-align:center;padding:8px;background:#f0f4f8;border-radius:8px;'>
                <div style='font-size:1.5rem;font-weight:700;color:{budget_color};'>€{r['avg_price']}</div>
                <div style='font-size:0.7rem;color:#888;'>avg meal</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

# ============================================================
# ABOUT
# ============================================================
with st.expander("ℹ️ About this project"):
    st.markdown("""
    **Why I built this:** When I moved to Stuttgart from India, finding good affordable food was harder 
    than it should be. Google Maps reviews are noisy, and most food blogs are written for tourists 
    with different budgets and tastes.
    
    **How it works:** I personally visited or researched each restaurant. Ratings are from Google Maps 
    (as of early 2026). The "student-friendly" tag means you can eat a full meal for under €12. 
    My personal notes are honest — not everything is amazing, but it's all worth trying.
    
    **Data:** Currently manually curated. Future version will scrape Google Maps reviews 
    and auto-update ratings and prices.
    
    **Want to add a restaurant?** Open an issue on [GitHub](https://github.com/aishwaryasanjaysonawane-a11y/stuttgart-eats) 
    or message me on [LinkedIn](https://linkedin.com/in/aishwarya-sonawane).
    """)

# Footer
st.markdown("""
<div style='text-align:center;color:#888;font-size:0.8rem;margin-top:2rem;'>
Built by Aishwarya Sonawane · Stuttgart, 2026 · 
<a href='https://github.com/aishwaryasanjaysonawane-a11y'>GitHub</a> · 
<a href='https://aishwaryasanjaysonawane-a11y.github.io/Portfolio/'>Portfolio</a>
</div>
""", unsafe_allow_html=True)
