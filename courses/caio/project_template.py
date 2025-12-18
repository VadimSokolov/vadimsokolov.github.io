"""
Orange Juice Pricing Analytics Agent
=====================================
CAIO Executive Program - Final Project

This template provides the scaffolding for your AI pricing agent.
Follow the instructions in each section to complete your project.

Author: [Your Name]
Date: [Date]
"""

# ============================================
# SECTION 1: IMPORT LIBRARIES
# ============================================
# These libraries are already installed. Just run this section.

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import warnings
warnings.filterwarnings('ignore')

print("✓ Libraries loaded successfully!")


# ============================================
# SECTION 2: LOAD THE DATA
# ============================================
# TODO: Make sure oj_data.csv is in the same folder as this script

print("\n" + "="*50)
print("Loading Orange Juice Sales Data...")
print("="*50)

# Load the dataset
df = pd.read_csv('oj_data.csv')

# Display basic information about the data
print(f"\n✓ Loaded {len(df):,} sales records")
print(f"✓ Columns: {list(df.columns)}")
print(f"✓ Brands: {df['brand'].unique().tolist()}")
print(f"✓ Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")

# Show sample of data
print("\nSample data (first 5 rows):")
print(df.head())


# ============================================
# SECTION 3: BUILD THE REGRESSION MODEL
# ============================================
# This section creates the pricing model that predicts sales
# based on price, brand, and advertising.

print("\n" + "="*50)
print("Building the Pricing Model...")
print("="*50)

# Create dummy variables for brand
# This converts brand names into numbers the model can use
brand_dummies = pd.get_dummies(df['brand'], prefix='brand', drop_first=False)

# Build the feature matrix (X)
# Features: price, advertising (feat), brand indicators, and interactions
X = pd.DataFrame({
    'price': df['price'],
    'feat': df['feat'],
    'brand_minute.maid': brand_dummies['brand_minute.maid'],
    'brand_tropicana': brand_dummies['brand_tropicana'],
    # Interaction terms capture how price effect differs by brand
    'price_x_minute.maid': df['price'] * brand_dummies['brand_minute.maid'],
    'price_x_tropicana': df['price'] * brand_dummies['brand_tropicana']
})

# Target variable (y) - what we're predicting
y = df['logmove']  # Log of sales volume

# Fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Display model results
print("\n✓ Model trained successfully!")
print("\nModel Coefficients:")
print("-" * 40)
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.4f}")
print(f"  intercept: {model.intercept_:.4f}")

# Model quality
r_squared = model.score(X, y)
print(f"\n✓ Model R-squared: {r_squared:.3f}")
print(f"  (Explains {r_squared*100:.1f}% of variation in sales)")


# ============================================
# SECTION 4: HELPER FUNCTIONS
# ============================================
# These functions help the agent answer business questions.
# You don't need to modify these - just understand what they do.

def predict_sales(brand, price, featured=0):
    """
    Predict sales volume for a given scenario.
    
    Parameters:
    - brand: 'tropicana', 'minute.maid', or 'dominicks'
    - price: price in dollars (e.g., 2.50)
    - featured: 1 if in ad circular, 0 if not
    
    Returns:
    - Predicted sales volume (units)
    """
    # Build feature vector for this prediction
    features = {
        'price': price,
        'feat': featured,
        'brand_minute.maid': 1 if brand.lower() == 'minute.maid' else 0,
        'brand_tropicana': 1 if brand.lower() == 'tropicana' else 0,
        'price_x_minute.maid': price if brand.lower() == 'minute.maid' else 0,
        'price_x_tropicana': price if brand.lower() == 'tropicana' else 0
    }
    
    X_pred = pd.DataFrame([features])
    log_sales = model.predict(X_pred)[0]
    sales = np.exp(log_sales)  # Convert from log back to units
    
    return sales


def get_price_elasticity(brand):
    """
    Get price elasticity for a brand.
    
    Elasticity tells us: if price increases 1%, 
    how much does quantity change (%)?
    
    More negative = more price sensitive
    """
    base_coef = model.coef_[0]  # price coefficient
    
    if brand.lower() == 'minute.maid':
        interaction = model.coef_[4]
    elif brand.lower() == 'tropicana':
        interaction = model.coef_[5]
    else:
        interaction = 0
    
    return base_coef + interaction


def get_advertising_lift(brand):
    """
    Calculate % sales increase from advertising.
    """
    feat_coef = model.coef_[1]
    return (np.exp(feat_coef) - 1) * 100


def find_optimal_price(brand, min_price=1.0, max_price=4.0, featured=0):
    """
    Find the revenue-maximizing price.
    Revenue = Price × Quantity
    """
    best_price = min_price
    best_revenue = 0
    
    for price in np.arange(min_price, max_price, 0.05):
        sales = predict_sales(brand, price, featured)
        revenue = price * sales
        if revenue > best_revenue:
            best_revenue = revenue
            best_price = price
    
    return best_price, best_revenue


def compare_elasticities():
    """Compare price sensitivity across all brands."""
    return {
        'dominicks': get_price_elasticity('dominicks'),
        'minute.maid': get_price_elasticity('minute.maid'),
        'tropicana': get_price_elasticity('tropicana')
    }


print("\n✓ Helper functions loaded!")


# ============================================
# SECTION 5: TEST THE MODEL
# ============================================
# Let's verify everything works before building the agent.

print("\n" + "="*50)
print("Testing the Model...")
print("="*50)

# Test prediction
test_sales = predict_sales('tropicana', 2.50, featured=0)
print(f"\n✓ Test: Tropicana at $2.50 = {test_sales:,.0f} units predicted")

# Test elasticity
test_elast = get_price_elasticity('tropicana')
print(f"✓ Test: Tropicana elasticity = {test_elast:.3f}")

# Test advertising lift
test_lift = get_advertising_lift('tropicana')
print(f"✓ Test: Advertising lift = {test_lift:.1f}%")

print("\n✓ All tests passed! Model is ready.")


# ============================================
# SECTION 6: THE AI AGENT
# ============================================
# TODO: Review and understand this agent logic.
# The agent interprets questions and calls the appropriate function.

def answer_question(question):
    """
    Process a natural language question and return an answer.
    """
    q = question.lower()
    
    # ---- QUESTION TYPE 1: Sales Prediction ----
    if 'predict' in q or 'sales volume' in q or 'predicted sales' in q:
        # Determine brand
        if 'tropicana' in q:
            brand = 'tropicana'
        elif 'minute maid' in q:
            brand = 'minute.maid'
        else:
            brand = 'dominicks'
        
        # Extract price (look for numbers)
        import re
        price_match = re.search(r'\$?(\d+\.?\d*)', q)
        price = float(price_match.group(1)) if price_match else 2.50
        
        # Check for advertising
        featured = 0
        if 'advertis' in q or 'feature' in q:
            featured = 1
        if 'no advertis' in q or 'without' in q:
            featured = 0
        
        sales = predict_sales(brand, price, featured)
        
        return f"""
📊 **Sales Prediction**

Brand: {brand.replace('.', ' ').title()}
Price: ${price:.2f}
Featured in Ad: {'Yes' if featured else 'No'}

**Predicted Sales: {sales:,.0f} units**
"""
    
    # ---- QUESTION TYPE 2: Price Sensitivity ----
    elif 'price-sensitive' in q or 'price sensitive' in q or 'most sensitive' in q:
        elasticities = compare_elasticities()
        most_sensitive = min(elasticities, key=elasticities.get)
        
        result = "📈 **Price Sensitivity Analysis**\n\n"
        for brand, elast in sorted(elasticities.items(), key=lambda x: x[1]):
            result += f"• {brand.replace('.', ' ').title()}: {elast:.3f}\n"
        
        result += f"\n**Most Price-Sensitive: {most_sensitive.replace('.', ' ').title()}**"
        return result
    
    # ---- QUESTION TYPE 3: Advertising Impact ----
    elif 'feature' in q or 'ad circular' in q or 'advertising' in q:
        if 'minute maid' in q:
            brand = 'minute.maid'
        elif 'tropicana' in q:
            brand = 'tropicana'
        else:
            brand = 'dominicks'
        
        lift = get_advertising_lift(brand)
        
        return f"""
📺 **Advertising Impact for {brand.replace('.', ' ').title()}**

Expected Sales Lift: **{lift:.1f}%**

Recommendation: {'Yes, feature this brand!' if lift > 20 else 'Consider costs vs. benefits.'}
"""
    
    # ---- QUESTION TYPE 4: Optimal Price ----
    elif 'optimal' in q or 'maximize revenue' in q or 'best price' in q:
        if 'minute maid' in q:
            brand = 'minute.maid'
        elif 'tropicana' in q:
            brand = 'tropicana'
        else:
            brand = 'dominicks'
        
        opt_price, opt_rev = find_optimal_price(brand)
        
        return f"""
💰 **Revenue Optimization for {brand.replace('.', ' ').title()}**

**Optimal Price: ${opt_price:.2f}**
Expected Revenue: ${opt_rev:,.2f} per store-week
"""
    
    # ---- QUESTION TYPE 5: Compare Elasticities ----
    elif 'compare' in q or 'elasticity' in q or 'across' in q:
        elasticities = compare_elasticities()
        
        result = "📊 **Price Elasticity Comparison**\n\n"
        result += "| Brand | Elasticity | Meaning |\n"
        result += "|-------|------------|----------|\n"
        
        for brand, elast in sorted(elasticities.items(), key=lambda x: x[1]):
            meaning = f"1% price ↑ = {abs(elast):.1f}% sales ↓"
            result += f"| {brand.replace('.', ' ').title()} | {elast:.3f} | {meaning} |\n"
        
        return result
    
    # ---- DEFAULT: Help Message ----
    else:
        return """
🤔 I can help with these questions:

1. "What is the predicted sales if we price Tropicana at $2.50?"
2. "Which brand is most price-sensitive?"
3. "Should we feature Minute Maid in the ad circular?"
4. "What price maximizes revenue for Dominick's?"
5. "Compare price elasticity across brands"

Try one of these!
"""


# ============================================
# SECTION 7: RUN THE AGENT
# ============================================
# This creates the interactive chat interface.

def run_agent():
    """Start the interactive agent."""
    print("\n" + "="*60)
    print("🍊 ORANGE JUICE PRICING AGENT 🍊")
    print("="*60)
    print("\nAsk me about OJ pricing and promotions!")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! 👋")
            break
        
        if question:
            print("\n" + "-"*40)
            print(answer_question(question))
            print("-"*40 + "\n")


# ============================================
# MAIN EXECUTION
# ============================================
# When you run this file, it will:
# 1. Load data
# 2. Build the model
# 3. Start the interactive agent

if __name__ == "__main__":
    run_agent()

