import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import time
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random
import os
from io import BytesIO
import base64
import hashlib
from scipy import stats

# Set page configuration
st.set_page_config(
    page_title="Manufacturing Central Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Professional Green Theme & LARGER FONT SIZES
st.markdown("""
<style>
    :root {
        --primary-green: #006400;
        --secondary-green: #228B22;
        --light-green: #90EE90;
        --dark-green: #004d00;
        --accent-orange: #FF8C00;
        --accent-blue: #1E90FF;
        --bg-light: #f8f9fa;
        --bg-white: #ffffff;
        --text-dark: #333333;
        --text-light: #666666;
        --border-color: #e0e0e0;
    }
    
    /* DRAMATICALLY INCREASED FONT SIZES */
    html, body, .stApp {
        font-size: 18px !important;
    }
    
    .main-header {
        font-size: 4rem !important;
        color: var(--primary-green);
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1.8rem !important;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    .section-header {
        font-size: 2.8rem !important;
        color: var(--primary-green);
        border-bottom: 4px solid var(--primary-green);
        padding-bottom: 1rem;
        margin-top: 2.5rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
    }
    .subsection-header {
        font-size: 2.2rem !important;
        color: var(--secondary-green);
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        font-size: 2.2rem !important;
        color: var(--primary-green);
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sidebar-section {
        background: var(--bg-white);
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 6px solid var(--primary-green);
        box-shadow: 0 3px 6px rgba(0,0,0,0.08);
    }
    .sidebar-item {
        padding: 15px 18px;
        margin: 8px 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 500;
        font-size: 1.3rem !important;
    }
    .sidebar-item:hover {
        background: linear-gradient(90deg, var(--light-green) 0%, #e8f5e8 100%);
        transform: translateX(8px);
    }
    .sidebar-item.active {
        background: linear-gradient(90deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        color: white;
        box-shadow: 0 6px 12px rgba(0,100,0,0.25);
    }
    
    /* Cards and Metrics - LARGER */
    .metric-card {
        background: var(--bg-white);
        border-radius: 15px;
        padding: 2rem;
        border: 2px solid var(--border-color);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    .metric-value {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: var(--primary-green);
        line-height: 1;
    }
    .metric-label {
        font-size: 1.4rem !important;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    .metric-change {
        font-size: 1.3rem !important;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 15px;
        display: inline-block;
        margin-top: 10px;
    }
    .metric-change.positive {
        background: #d4edda;
        color: #155724;
    }
    .metric-change.negative {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Alert Badges - LARGER */
    .alert-badge {
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 1.3rem !important;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .alert-critical {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    .alert-warning {
        background: linear-gradient(135deg, #ff9900 0%, #cc7a00 100%);
        color: white;
    }
    .alert-info {
        background: linear-gradient(135deg, #0099ff 0%, #0066cc 100%);
        color: white;
    }
    .alert-success {
        background: linear-gradient(135deg, #00cc66 0%, #00994d 100%);
        color: white;
    }
    
    /* Widget Cards */
    .widget-card {
        background: var(--bg-white);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid var(--border-color);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    .widget-header {
        font-size: 1.8rem !important;
        color: var(--primary-green);
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Button Styling - LARGER */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 1.4rem !important;
        height: auto;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,100,0,0.25);
    }
    .primary-btn {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%) !important;
    }
    .secondary-btn {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%) !important;
    }
    .danger-btn {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
    }
    
    /* Table Styling - LARGER */
    .data-table {
        font-size: 1.2rem !important;
    }
    .table-header {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        color: white;
        font-size: 1.4rem !important;
        padding: 15px !important;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .status-active { background-color: #28a745; }
    .status-inactive { background-color: #6c757d; }
    .status-pending { background-color: #ffc107; }
    .status-critical { background-color: #dc3545; }
    
    /* Progress Bars */
    .progress-bar {
        height: 12px;
        background: #e9ecef;
        border-radius: 6px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-green), var(--secondary-green));
        border-radius: 6px;
    }
    
    /* Form Styling - LARGER */
    .form-section {
        background: var(--bg-white);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid var(--border-color);
        margin-bottom: 30px;
    }
    
    /* Chat Styles - LARGER */
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        border-radius: 15px;
        background: var(--bg-light);
        margin-bottom: 25px;
        font-size: 1.4rem !important;
    }
    .chat-message {
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 22px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 1.4rem !important;
    }
    .user-message {
        background: var(--primary-green);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 8px;
    }
    .bot-message {
        background: var(--bg-white);
        color: var(--text-dark);
        margin-right: auto;
        border-bottom-left-radius: 8px;
        border: 2px solid var(--border-color);
    }
    .grok-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 8px;
    }
    
    /* DRAMATICALLY INCREASE ALL Streamlit text sizes */
    .stTextInput > div > div > input {
        font-size: 1.4rem !important;
        padding: 15px 18px !important;
        height: auto !important;
    }
    .stSelectbox > div > div > div {
        font-size: 1.4rem !important;
        padding: 12px !important;
    }
    .stNumberInput > div > div > input {
        font-size: 1.4rem !important;
        padding: 15px !important;
    }
    .stTextArea > div > div > textarea {
        font-size: 1.4rem !important;
        padding: 15px !important;
        min-height: 120px !important;
    }
    .stDateInput > div > div > input {
        font-size: 1.4rem !important;
        padding: 15px !important;
    }
    .stMultiSelect > div > div > div {
        font-size: 1.4rem !important;
        padding: 12px !important;
    }
    
    /* Chart titles - LARGER */
    .js-plotly-plot .plotly .main-svg .gtitle {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
    
    /* Streamlit metric values - MUCH LARGER */
    div[data-testid="stMetricValue"] {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
    }
    
    /* Tabs - LARGER */
    .stTabs [data-baseweb="tab-list"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        gap: 20px !important;
    }
    
    /* Expanders - LARGER */
    .streamlit-expanderHeader {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        padding: 20px !important;
    }
    .streamlit-expanderContent {
        font-size: 1.4rem !important;
        padding: 20px !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        font-size: 1.4rem !important;
        line-height: 1.6 !important;
    }
    
    /* Captions */
    .stCaption {
        font-size: 1.2rem !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        font-size: 1.3rem !important;
    }
    
    /* Checkboxes and Radio buttons */
    .stCheckbox label, .stRadio label {
        font-size: 1.4rem !important;
    }
    
    /* Sliders */
    .stSlider label {
        font-size: 1.4rem !important;
    }
    
    /* Select sliders */
    .stSelectSlider label {
        font-size: 1.4rem !important;
    }
    
    /* Info, success, warning, error boxes */
    .stAlert {
        font-size: 1.4rem !important;
        padding: 20px !important;
    }
    
    /* Divider */
    hr {
        margin: 30px 0 !important;
        border-width: 2px !important;
    }
    
    /* Help text */
    .stTooltipIcon {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MANUFACTURING DATA MODELS & INITIALIZATION
# ============================================

class ManufacturingPortal:
    def __init__(self):
        self.products = self.initialize_products()
        self.customers = self.initialize_customers()
        self.orders = self.initialize_orders()
        self.suppliers = self.initialize_suppliers()
        self.inventory = self.initialize_inventory()
        self.leads = self.initialize_leads()
        self.marketing_campaigns = self.initialize_marketing()
        self.financial_data = self.initialize_finance()
        
    def initialize_products(self):
        """Initialize product catalog for manufacturing business"""
        products = {
            "Storage and Mobile Lockers": [
                {"id": "PROD001", "name": "Mild Steel Worker Locker", "category": "Lockers", "price": 8500, "cost": 5200, "stock": 45, "min_stock": 20, "lead_time": 7, "image": "locker1.jpg"},
                {"id": "PROD002", "name": "Swimming Pool Locker", "category": "Lockers", "price": 12500, "cost": 7800, "stock": 22, "min_stock": 10, "lead_time": 10, "image": "locker2.jpg"},
                {"id": "PROD003", "name": "Laptop Storage Lockers", "category": "Lockers", "price": 9500, "cost": 5800, "stock": 38, "min_stock": 15, "lead_time": 7, "image": "locker3.jpg"},
            ],
            "HVAC Ducting System": [
                {"id": "PROD004", "name": "SS Industrial Duct", "category": "HVAC", "price": 3200, "cost": 1850, "stock": 120, "min_stock": 50, "lead_time": 5, "image": "duct1.jpg"},
                {"id": "PROD005", "name": "Round Spiral Ducting", "category": "HVAC", "price": 2800, "cost": 1650, "stock": 95, "min_stock": 40, "lead_time": 5, "image": "duct2.jpg"},
                {"id": "PROD006", "name": "GI Ducting Services", "category": "HVAC", "price": 4500, "cost": 2800, "stock": 65, "min_stock": 25, "lead_time": 7, "image": "duct3.jpg"},
            ],
            "Electrical Control Panel": [
                {"id": "PROD007", "name": "Generator Control Panel", "category": "Electrical", "price": 18500, "cost": 11200, "stock": 18, "min_stock": 8, "lead_time": 14, "image": "panel1.jpg"},
                {"id": "PROD008", "name": "Electric Control Panel", "category": "Electrical", "price": 15200, "cost": 9200, "stock": 25, "min_stock": 10, "lead_time": 12, "image": "panel2.jpg"},
                {"id": "PROD009", "name": "Mild Steel Electrical Panel", "category": "Electrical", "price": 12800, "cost": 7800, "stock": 32, "min_stock": 12, "lead_time": 10, "image": "panel3.jpg"},
            ],
            "Sheet Metal Fabrication": [
                {"id": "PROD010", "name": "Sheet Metal Fabrication Services", "category": "Fabrication", "price": 5000, "cost": 3000, "stock": 0, "min_stock": 0, "lead_time": 10, "image": "fabrication1.jpg"},
                {"id": "PROD011", "name": "Metal Cutting Service", "category": "Fabrication", "price": 3000, "cost": 1800, "stock": 0, "min_stock": 0, "lead_time": 5, "image": "fabrication2.jpg"},
            ],
            "Laser Cutting": [
                {"id": "PROD012", "name": "SS Laser Cutting", "category": "Laser", "price": 4000, "cost": 2400, "stock": 0, "min_stock": 0, "lead_time": 3, "image": "laser1.jpg"},
                {"id": "PROD013", "name": "CNC Laser Cutting Services", "category": "Laser", "price": 4500, "cost": 2700, "stock": 0, "min_stock": 0, "lead_time": 4, "image": "laser2.jpg"},
            ],
            "Storage Rack": [
                {"id": "PROD014", "name": "Industrial Storage Rack", "category": "Racks", "price": 7500, "cost": 4500, "stock": 52, "min_stock": 20, "lead_time": 7, "image": "rack1.jpg"},
                {"id": "PROD015", "name": "MS Slotted Angle Racks", "category": "Racks", "price": 6800, "cost": 4200, "stock": 48, "min_stock": 18, "lead_time": 6, "image": "rack2.jpg"},
            ]
        }
        return products
    
    def initialize_customers(self):
        """Initialize customer database"""
        customers = []
        industries = ['Manufacturing', 'Construction', 'Hospitality', 'Education', 'Healthcare', 
                     'Retail', 'Government', 'Corporate', 'Infrastructure', 'Real Estate']
        
        for i in range(150):
            customers.append({
                'customer_id': f"CUST{10000 + i}",
                'name': f"Customer {i+1}",
                'company': f"Company {chr(65 + i%26)}{i//26 + 1}",
                'email': f"customer{i+1}@example.com",
                'phone': f"+91{random.randint(70000, 99999)}{random.randint(10000, 99999)}",
                'industry': random.choice(industries),
                'region': random.choice(['North India', 'South India', 'West India', 'East India', 'Middle East', 'Europe', 'Asia Pacific']),
                'status': random.choice(['Active', 'Active', 'Active', 'Inactive']),
                'credit_limit': random.choice([100000, 200000, 300000, 500000, 1000000]),
                'total_orders': random.randint(1, 50),
                'total_spent': random.randint(50000, 5000000),
                'customer_since': (date.today() - timedelta(days=random.randint(30, 1825))).strftime("%Y-%m-%d"),
                'last_order': (date.today() - timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
                'sales_rep': random.choice(['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Neha Gupta', 'Vikram Singh'])
            })
        return pd.DataFrame(customers)
    
    def initialize_orders(self):
        """Initialize order database"""
        orders = []
        statuses = ['Quote', 'Confirmed', 'Production', 'QC', 'Ready for Shipment', 'Shipped', 'Delivered', 'Cancelled']
        
        for i in range(300):
            order_date = date.today() - timedelta(days=random.randint(0, 365))
            delivery_date = order_date + timedelta(days=random.randint(7, 60))
            
            orders.append({
                'order_id': f"ORD{20000 + i}",
                'customer_id': f"CUST{10000 + random.randint(0, 149)}",
                'order_date': order_date.strftime("%Y-%m-%d"),
                'delivery_date': delivery_date.strftime("%Y-%m-%d"),
                'status': random.choice(statuses),
                'amount': random.randint(25000, 500000),
                'payment_status': random.choice(['Paid', 'Partial', 'Pending']),
                'payment_terms': random.choice(['Net 30', '50% Advance', '100% Advance']),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'products': f"Product {random.randint(1, 15)}",
                'quantity': random.randint(1, 25),
                'sales_rep': random.choice(['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Neha Gupta', 'Vikram Singh']),
                'notes': random.choice(['Urgent delivery', 'Standard order', 'Bulk discount applied', 'Export order'])
            })
        return pd.DataFrame(orders)
    
    def initialize_suppliers(self):
        """Initialize supplier database"""
        suppliers = []
        materials = ['Steel Sheets', 'GI Coils', 'SS Plates', 'Fasteners', 'Electrical Components', 
                    'Powder Coating', 'Paints', 'Packaging Material', 'CNC Tools', 'Laser Consumables']
        
        for i in range(50):
            suppliers.append({
                'supplier_id': f"SUPP{30000 + i}",
                'name': f"Supplier {i+1} Pvt Ltd",
                'contact_person': f"Mr. {random.choice(['Raj', 'Amit', 'Suresh', 'Kumar', 'Patel'])}",
                'email': f"supplier{i+1}@example.com",
                'phone': f"+91{random.randint(70000, 99999)}{random.randint(10000, 99999)}",
                'materials': random.sample(materials, random.randint(1, 4)),
                'lead_time': random.randint(3, 21),
                'rating': round(random.uniform(3.0, 5.0), 1),
                'status': random.choice(['Active', 'Active', 'Active', 'On Hold']),
                'last_order': (date.today() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
                'payment_terms': random.choice(['Net 45', 'Net 60', '30% Advance']),
                'location': random.choice(['Mumbai', 'Delhi', 'Chennai', 'Bangalore', 'Hyderabad', 'Pune', 'Ahmedabad'])
            })
        return pd.DataFrame(suppliers)
    
    def initialize_inventory(self):
        """Initialize inventory tracking"""
        inventory = []
        categories = ['Raw Materials', 'Work in Progress', 'Finished Goods', 'Spare Parts', 'Consumables']
        
        for i in range(200):
            category = random.choice(categories)
            if category == 'Raw Materials':
                items = ['Steel Sheets', 'GI Coils', 'SS Plates', 'MS Rods', 'Aluminum Sheets']
            elif category == 'Finished Goods':
                items = ['Lockers', 'Ducts', 'Panels', 'Racks', 'Fabricated Parts']
            else:
                items = ['Fasteners', 'Paints', 'Electrical Parts', 'Tools', 'Packaging']
            
            inventory.append({
                'item_id': f"INV{40000 + i}",
                'name': random.choice(items),
                'category': category,
                'current_stock': random.randint(0, 500),
                'min_stock': random.randint(10, 100),
                'max_stock': random.randint(200, 1000),
                'unit': random.choice(['kg', 'pcs', 'meters', 'liters']),
                'location': random.choice(['Warehouse A', 'Warehouse B', 'Production Area', 'Finished Goods Store']),
                'last_updated': (date.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                'status': 'In Stock' if random.random() > 0.2 else 'Low Stock',
                'value': random.randint(500, 50000)
            })
        return pd.DataFrame(inventory)
    
    def initialize_leads(self):
        """Initialize lead generation database"""
        leads = []
        sources = ['Website', 'Referral', 'Trade Show', 'LinkedIn', 'Email Campaign', 
                  'Google Ads', 'Phone Inquiry', 'WhatsApp', 'Social Media', 'Direct Visit']
        statuses = ['New', 'Contacted', 'Qualified', 'Proposal Sent', 'Negotiation', 'Closed Won', 'Closed Lost']
        
        for i in range(500):
            lead_date = date.today() - timedelta(days=random.randint(0, 180))
            followup_date = lead_date + timedelta(days=random.randint(1, 14))
            
            leads.append({
                'lead_id': f"LEAD{50000 + i}",
                'name': f"Lead Prospect {i+1}",
                'company': f"Company {chr(65 + i%26)}{i//26 + 1}",
                'email': f"lead{i+1}@example.com",
                'phone': f"+91{random.randint(70000, 99999)}{random.randint(10000, 99999)}",
                'source': random.choice(sources),
                'status': random.choice(statuses),
                'product_interest': random.choice(['Lockers', 'HVAC Ducts', 'Electrical Panels', 'Fabrication', 'Laser Cutting']),
                'value': random.randint(25000, 500000),
                'created_date': lead_date.strftime("%Y-%m-%d"),
                'last_contact': (lead_date + timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
                'next_followup': followup_date.strftime("%Y-%m-%d"),
                'assigned_to': random.choice(['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Neha Gupta', 'Vikram Singh']),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'notes': random.choice(['Very interested', 'Requested quote', 'Budget approved', 'Comparing vendors']),
                'conversion_probability': random.randint(10, 90)
            })
        return pd.DataFrame(leads)
    
    def initialize_marketing(self):
        """Initialize marketing campaigns"""
        campaigns = []
        platforms = ['Email', 'LinkedIn', 'Google Ads', 'Trade Show', 'Direct Mail', 
                    'Social Media', 'WhatsApp Broadcast', 'SMS', 'Telemarketing']
        
        for i in range(30):
            start_date = date.today() - timedelta(days=random.randint(0, 90))
            end_date = start_date + timedelta(days=random.randint(14, 60))
            
            campaigns.append({
                'campaign_id': f"CAMP{60000 + i}",
                'name': f"{random.choice(['Q4', 'Summer', 'Monsoon', 'Festive', 'Year-End'])} {random.choice(['Promotion', 'Campaign', 'Drive', 'Launch'])}",
                'platform': random.choice(platforms),
                'target_audience': random.choice(['Manufacturing Companies', 'Construction Firms', 'Hospitality Sector', 'Government Projects']),
                'budget': random.randint(10000, 200000),
                'spent': random.randint(5000, 180000),
                'leads_generated': random.randint(10, 200),
                'conversions': random.randint(1, 50),
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'status': random.choice(['Active', 'Completed', 'Planning', 'Paused']),
                'roi': random.randint(50, 500),
                'ctr': random.uniform(0.5, 8.0),
                'cost_per_lead': random.randint(500, 5000),
                'campaign_manager': random.choice(['Marketing Team', 'Sales Team', 'External Agency'])
            })
        return pd.DataFrame(campaigns)
    
    def initialize_finance(self):
        """Initialize financial data"""
        finance = {
            'revenue': [],
            'expenses': [],
            'invoices': [],
            'cashflow': []
        }
        
        # Monthly revenue for last 12 months
        months = [(date.today() - timedelta(days=30*i)).strftime("%Y-%m") for i in range(12, 0, -1)]
        base_revenue = 8000000
        trend = 1.05  # 5% growth trend
        
        for i, month in enumerate(months):
            month_revenue = int(base_revenue * (trend ** i) * random.uniform(0.9, 1.1))
            cost_of_goods = int(month_revenue * 0.65)
            gross_profit = month_revenue - cost_of_goods
            operating_expenses = int(month_revenue * 0.25)
            net_profit = gross_profit - operating_expenses
            
            finance['revenue'].append({
                'month': month,
                'revenue': month_revenue,
                'cost_of_goods': cost_of_goods,
                'gross_profit': gross_profit,
                'operating_expenses': operating_expenses,
                'net_profit': net_profit
            })
        
        # Expenses by category
        categories = ['Raw Materials', 'Labor', 'Utilities', 'Marketing', 'Logistics', 'Maintenance', 'Administration']
        for cat in categories:
            amount = random.randint(100000, 1000000)
            budget = int(amount * random.uniform(0.9, 1.2))
            variance = int(((amount - budget) / budget) * 100) if budget > 0 else 0
            
            finance['expenses'].append({
                'category': cat,
                'amount': amount,
                'budget': budget,
                'variance': variance
            })
        
        # Invoices
        for i in range(100):
            invoice_date = date.today() - timedelta(days=random.randint(0, 90))
            due_date = invoice_date + timedelta(days=30)
            
            finance['invoices'].append({
                'invoice_id': f"INV{70000 + i}",
                'customer_id': f"CUST{10000 + random.randint(0, 149)}",
                'amount': random.randint(10000, 500000),
                'date': invoice_date.strftime("%Y-%m-%d"),
                'due_date': due_date.strftime("%Y-%m-%d"),
                'status': random.choice(['Paid', 'Pending', 'Overdue', 'Partially Paid']),
                'payment_method': random.choice(['Bank Transfer', 'Cheque', 'Cash', 'Online Payment'])
            })
        
        # Cashflow
        balance = 5000000
        for i in range(30):
            day_date = date.today() - timedelta(days=29-i)
            inflow = random.randint(100000, 1000000)
            outflow = random.randint(80000, 900000)
            balance = balance + inflow - outflow
            
            finance['cashflow'].append({
                'date': day_date.strftime("%Y-%m-%d"),
                'inflow': inflow,
                'outflow': outflow,
                'balance': balance
            })
        
        finance['revenue'] = pd.DataFrame(finance['revenue'])
        finance['expenses'] = pd.DataFrame(finance['expenses'])
        finance['invoices'] = pd.DataFrame(finance['invoices'])
        finance['cashflow'] = pd.DataFrame(finance['cashflow'])
        
        return finance

# Initialize the portal
if 'portal' not in st.session_state:
    st.session_state.portal = ManufacturingPortal()

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'grok_chat_history' not in st.session_state:
    st.session_state.grok_chat_history = []

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_dashboard_metrics():
    """Calculate dashboard metrics"""
    portal = st.session_state.portal
    
    metrics = {
        'total_revenue': portal.orders['amount'].sum(),
        'active_customers': len(portal.customers[portal.customers['status'] == 'Active']),
        'pending_orders': len(portal.orders[portal.orders['status'].isin(['Quote', 'Confirmed', 'Production'])]),
        'low_stock_items': len(portal.inventory[portal.inventory['current_stock'] < portal.inventory['min_stock']]),
        'new_leads': len(portal.leads[portal.leads['status'] == 'New']),
        'conversion_rate': (len(portal.leads[portal.leads['status'] == 'Closed Won']) / len(portal.leads) * 100) if len(portal.leads) > 0 else 0,
        'active_campaigns': len(portal.marketing_campaigns[portal.marketing_campaigns['status'] == 'Active']),
        'overdue_invoices': len(portal.financial_data['invoices'][portal.financial_data['invoices']['status'] == 'Overdue'])
    }
    
    return metrics

def create_ai_forecast():
    """Generate AI forecasting data for manufacturing business"""
    portal = st.session_state.portal
    
    # Get historical data for forecasting
    orders_by_month = portal.orders.copy()
    orders_by_month['order_date'] = pd.to_datetime(orders_by_month['order_date'])
    orders_by_month['month'] = orders_by_month['order_date'].dt.strftime('%Y-%m')
    monthly_sales = orders_by_month.groupby('month')['amount'].sum().reset_index()
    
    # Generate next 6 months forecast using linear regression
    months = list(monthly_sales['month'])[-6:]  # Last 6 months
    sales = list(monthly_sales['amount'])[-6:]
    
    # Create time indices
    x = np.arange(len(months))
    
    # Linear regression for forecasting
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, sales)
    
    # Forecast next 6 months
    forecast_months = []
    forecast_values = []
    confidence_intervals = []
    
    # Last historical date
    last_month = pd.to_datetime(months[-1] + '-01')
    
    for i in range(1, 7):
        forecast_month = last_month + pd.DateOffset(months=i)
        forecast_months.append(forecast_month.strftime('%b %Y'))
        
        # Predicted value with seasonality (simulated)
        trend_value = intercept + slope * (len(months) + i - 1)
        
        # Add some seasonality and randomness
        seasonality = 1 + 0.15 * np.sin((i-1) * np.pi / 3)  # 6-month cycle
        random_factor = 1 + np.random.normal(0, 0.08)  # 8% random variation
        
        forecast_value = trend_value * seasonality * random_factor
        forecast_values.append(max(100000, forecast_value))  # Ensure positive
        
        # Confidence interval (95%)
        ci = 0.1 * forecast_value  # 10% confidence interval
        confidence_intervals.append(ci)
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        'Month': forecast_months,
        'Forecast': forecast_values,
        'Confidence_Interval': confidence_intervals,
        'Lower_Bound': [max(0, f - ci) for f, ci in zip(forecast_values, confidence_intervals)],
        'Upper_Bound': [f + ci for f, ci in zip(forecast_values, confidence_intervals)]
    })
    
    # Calculate key forecast metrics
    total_forecast = sum(forecast_values)
    avg_monthly_forecast = total_forecast / 6
    growth_rate = ((forecast_values[-1] - forecast_values[0]) / forecast_values[0]) * 100 if forecast_values[0] > 0 else 0
    
    # Inventory forecast based on sales trends
    inventory_forecast = []
    current_inventory_value = portal.inventory['value'].sum()
    
    for i in range(6):
        # Simulate inventory needs based on forecasted sales
        inventory_needed = forecast_values[i] * 0.4 / 1000  # 40% of sales value, scaled down
        safety_stock = inventory_needed * 0.3
        inventory_forecast.append({
            'month': forecast_months[i],
            'projected_sales': forecast_values[i],
            'inventory_needed': inventory_needed,
            'safety_stock': safety_stock,
            'total_inventory': inventory_needed + safety_stock
        })
    
    # Demand forecast by product category
    product_demand = {}
    for category, products in portal.products.items():
        category_sales = sum(p['price'] * p['stock'] for p in products)
        # Project growth based on historical trends
        projected_growth = 1 + (growth_rate / 100) * np.random.uniform(0.8, 1.2)
        product_demand[category] = {
            'current_demand': category_sales,
            'projected_demand': category_sales * projected_growth,
            'growth_percentage': (projected_growth - 1) * 100
        }
    
    return {
        'sales_forecast': forecast_df,
        'inventory_forecast': pd.DataFrame(inventory_forecast),
        'product_demand': product_demand,
        'metrics': {
            'total_forecast': total_forecast,
            'avg_monthly_forecast': avg_monthly_forecast,
            'growth_rate': growth_rate,
            'confidence_level': 0.95,
            'forecast_period': '6 months'
        }
    }

def generate_ai_recommendations():
    """Generate AI-powered recommendations for manufacturing operations"""
    portal = st.session_state.portal
    
    recommendations = []
    
    # 1. Inventory Optimization
    low_stock_items = portal.inventory[portal.inventory['current_stock'] < portal.inventory['min_stock']]
    if len(low_stock_items) > 0:
        recommendations.append({
            'type': 'inventory',
            'priority': 'high',
            'title': 'Reorder Low Stock Items',
            'description': f'{len(low_stock_items)} items are below minimum stock levels',
            'action': 'Initiate purchase orders for critical items',
            'impact': 'Prevent production delays'
        })
    
    # 2. Production Efficiency
    wip_items = portal.inventory[portal.inventory['category'] == 'Work in Progress']
    if len(wip_items) > 0:
        avg_wip_time = random.randint(3, 10)  # Simulated data
        if avg_wip_time > 7:
            recommendations.append({
                'type': 'production',
                'priority': 'medium',
                'title': 'Reduce WIP Time',
                'description': f'Average WIP time is {avg_wip_time} days, target is 5 days',
                'action': 'Review production bottlenecks',
                'impact': 'Increase throughput by 15-20%'
            })
    
    # 3. Sales Opportunities
    high_value_leads = portal.leads[
        (portal.leads['value'] > 200000) & 
        (portal.leads['status'].isin(['New', 'Qualified']))
    ]
    if len(high_value_leads) > 0:
        recommendations.append({
            'type': 'sales',
            'priority': 'high',
            'title': 'Follow up High-Value Leads',
            'description': f'{len(high_value_leads)} leads with value > ₹2L awaiting follow-up',
            'action': 'Schedule sales calls this week',
            'impact': 'Potential revenue: ₹{:,}'.format(high_value_leads['value'].sum())
        })
    
    # 4. Quality Control
    recent_qc_issues = random.randint(0, 5)  # Simulated
    if recent_qc_issues > 2:
        recommendations.append({
            'type': 'quality',
            'priority': 'medium',
            'title': 'Address Quality Issues',
            'description': f'{recent_qc_issues} QC issues reported in last week',
            'action': 'Review production processes and training',
            'impact': 'Reduce reject rate by 30%'
        })
    
    # 5. Supplier Performance
    low_rated_suppliers = portal.suppliers[portal.suppliers['rating'] < 3.5]
    if len(low_rated_suppliers) > 0:
        recommendations.append({
            'type': 'supply_chain',
            'priority': 'low',
            'title': 'Review Low-Rated Suppliers',
            'description': f'{len(low_rated_suppliers)} suppliers with rating below 3.5',
            'action': 'Evaluate alternative suppliers',
            'impact': 'Improve material quality and reliability'
        })
    
    # 6. Maintenance Schedule
    overdue_maintenance = random.randint(0, 8)  # Simulated
    if overdue_maintenance > 3:
        recommendations.append({
            'type': 'maintenance',
            'priority': 'medium',
            'title': 'Schedule Equipment Maintenance',
            'description': f'{overdue_maintenance} pieces of equipment due for maintenance',
            'action': 'Create maintenance schedule',
            'impact': 'Reduce breakdowns by 40%'
        })
    
    # 7. Energy Efficiency
    energy_cost = portal.financial_data['expenses'][
        portal.financial_data['expenses']['category'] == 'Utilities'
    ]['amount'].iloc[0] if len(portal.financial_data['expenses']) > 0 else 0
    
    if energy_cost > 500000:
        recommendations.append({
            'type': 'sustainability',
            'priority': 'low',
            'title': 'Optimize Energy Consumption',
            'description': 'High utility costs detected',
            'action': 'Conduct energy audit',
            'impact': 'Potential savings: ₹50,000-75,000/month'
        })
    
    return recommendations

def get_production_efficiency():
    """Calculate production efficiency metrics"""
    # Simulated production data
    efficiency_data = []
    
    # Last 30 days
    for i in range(30):
        day = (date.today() - timedelta(days=29-i)).strftime('%Y-%m-%d')
        
        efficiency_data.append({
            'date': day,
            'planned_output': random.randint(80, 120),
            'actual_output': random.randint(75, 115),
            'downtime_minutes': random.randint(30, 180),
            'defect_rate': random.uniform(0.5, 3.5),
            'oee': random.uniform(75, 92)
        })
    
    df = pd.DataFrame(efficiency_data)
    
    # Calculate metrics
    avg_oee = df['oee'].mean()
    total_downtime = df['downtime_minutes'].sum()
    avg_defect_rate = df['defect_rate'].mean()
    utilization = (df['actual_output'].sum() / df['planned_output'].sum()) * 100
    
    return {
        'data': df,
        'metrics': {
            'avg_oee': avg_oee,
            'total_downtime': total_downtime,
            'avg_defect_rate': avg_defect_rate,
            'utilization': utilization
        }
    }

# ============================================
# SIDEBAR NAVIGATION
# ============================================

def sidebar():
    """Render sidebar navigation"""
    st.sidebar.markdown('<div class="sidebar-header">🏭 Manufacturing Portal</div>', unsafe_allow_html=True)
    
    # User profile section
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    col1, col2 = st.sidebar.columns([1, 3])
    with col1:
        st.markdown("👤")
    with col2:
        st.markdown("**Rajesh Kumar**")
        st.markdown("*Plant Manager*")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    
    pages = [
        {"icon": "📊", "name": "Dashboard", "key": "dashboard"},
        {"icon": "🏭", "name": "Production", "key": "production"},
        {"icon": "📦", "name": "Inventory", "key": "inventory"},
        {"icon": "💰", "name": "Sales & Orders", "key": "sales"},
        {"icon": "👥", "name": "Customers", "key": "customers"},
        {"icon": "📈", "name": "Finance", "key": "finance"},
        {"icon": "🎯", "name": "Marketing", "key": "marketing"},
        {"icon": "🤖", "name": "AI Assistant", "key": "ai"},
        {"icon": "⚙️", "name": "Settings", "key": "settings"}
    ]
    
    # Initialize session state for page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    for page in pages:
        is_active = st.session_state.current_page == page["key"]
        active_class = "active" if is_active else ""
        
        if st.sidebar.button(f"{page['icon']} {page['name']}", 
                           key=f"nav_{page['key']}",
                           use_container_width=True):
            st.session_state.current_page = page["key"]
            st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Quick stats
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("**Quick Stats**")
    
    metrics = get_dashboard_metrics()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Revenue", f"₹{metrics['total_revenue']:,.0f}")
        st.metric("Customers", metrics['active_customers'])
    with col2:
        st.metric("Orders", metrics['pending_orders'])
        st.metric("Leads", metrics['new_leads'])
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PAGE FUNCTIONS
# ============================================

def dashboard_page():
    """Main dashboard page"""
    st.markdown('<h1 class="main-header">Manufacturing Central Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time monitoring and analytics for manufacturing operations</p>', unsafe_allow_html=True)
    
    # Alert Bar
    alerts = [
        {"type": "critical", "message": "Machine #3 requires maintenance", "time": "2 hours ago"},
        {"type": "warning", "message": "Low stock: Steel Sheets (45 units)", "time": "4 hours ago"},
        {"type": "info", "message": "New lead from Google Ads: ₹2,50,000 potential", "time": "Today"},
        {"type": "success", "message": "Order #ORD21045 shipped successfully", "time": "Yesterday"}
    ]
    
    with st.container():
        cols = st.columns(len(alerts))
        for idx, alert in enumerate(alerts):
            with cols[idx]:
                st.markdown(f'<div class="alert-badge alert-{alert["type"]}">⚠️ {alert["message"]}</div>', unsafe_allow_html=True)
    
    # KPI Metrics
    st.markdown('<h2 class="section-header">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    metrics = get_dashboard_metrics()
    forecast_data = create_ai_forecast()
    
    # Create 4 columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Total Revenue", f"₹{metrics['total_revenue']:,.0f}", 
                 f"₹{forecast_data['metrics']['avg_monthly_forecast']/1000:,.0f}K forecast")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Active Customers", metrics['active_customers'], 
                 f"{len(st.session_state.portal.leads[st.session_state.portal.leads['status'] == 'New'])} new leads")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Production Efficiency", "86.5%", "2.3% ↑")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("On-time Delivery", "92.3%", "1.2% ↑")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Pending Orders", metrics['pending_orders'], "5 urgent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Inventory Value", "₹4.2M", "₹150K to order")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col7:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Quality Yield", "97.8%", "0.5% ↑")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="metric-card slide-in">', unsafe_allow_html=True)
        st.metric("Employee Productivity", "88.4%", "1.8% ↑")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<h2 class="section-header">Performance Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">📈 Revenue Trend & Forecast</div>', unsafe_allow_html=True)
        
        # Create sales forecast chart
        fig = go.Figure()
        
        # Historical data
        historical_months = st.session_state.portal.financial_data['revenue']['month'].tolist()[-6:]
        historical_revenue = st.session_state.portal.financial_data['revenue']['revenue'].tolist()[-6:]
        
        fig.add_trace(go.Scatter(
            x=historical_months,
            y=historical_revenue,
            mode='lines+markers',
            name='Historical Revenue',
            line=dict(color='#006400', width=3),
            marker=dict(size=10)
        ))
        
        # Forecast data
        forecast_df = forecast_data['sales_forecast']
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Month'],
            y=forecast_df['Forecast'],
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#FF8C00', width=3, dash='dash'),
            marker=dict(size=10)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['Month'].tolist() + forecast_df['Month'].tolist()[::-1],
            y=forecast_df['Upper_Bound'].tolist() + forecast_df['Lower_Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 140, 0, 0.2)',
            line=dict(color='rgba(255, 140, 0, 0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">🏭 Production Status</div>', unsafe_allow_html=True)
        
        # Production status
        status_data = get_production_efficiency()
        
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=status_data['metrics']['avg_oee'],
            title={'text': "OEE (%)"},
            domain={'x': [0, 0.45], 'y': [0.5, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#006400"},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 85], 'color': "gray"},
                    {'range': [85, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=status_data['metrics']['avg_defect_rate'],
            title={'text': "Defect Rate (%)"},
            domain={'x': [0.55, 1], 'y': [0.7, 1]},
            number={'suffix': "%"}
        ))
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=status_data['metrics']['total_downtime'] / 60,
            title={'text': "Downtime (hours)"},
            domain={'x': [0.55, 1], 'y': [0.3, 0.6]},
            number={'suffix': "h"}
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Third row: Orders and Inventory
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">📊 Order Status Distribution</div>', unsafe_allow_html=True)
        
        order_status = st.session_state.portal.orders['status'].value_counts()
        
        fig = px.pie(
            values=order_status.values,
            names=order_status.index,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">📦 Inventory Status</div>', unsafe_allow_html=True)
        
        inventory_status = st.session_state.portal.inventory['status'].value_counts()
        
        fig = px.bar(
            x=inventory_status.index,
            y=inventory_status.values,
            color=inventory_status.index,
            color_discrete_map={'In Stock': '#006400', 'Low Stock': '#FF8C00', 'Out of Stock': '#DC3545'},
            text=inventory_status.values
        )
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            showlegend=False,
            xaxis_title="Status",
            yaxis_title="Count"
        )
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Recommendations
    st.markdown('<h2 class="section-header">🤖 AI Recommendations</h2>', unsafe_allow_html=True)
    
    recommendations = generate_ai_recommendations()
    
    if recommendations:
        cols = st.columns(min(3, len(recommendations)))
        
        for idx, rec in enumerate(recommendations):
            with cols[idx % 3]:
                priority_color = {
                    'high': '#DC3545',
                    'medium': '#FF8C00',
                    'low': '#006400'
                }
                
                st.markdown(f'''
                <div class="widget-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>{rec['title']}</h4>
                        <span style="background-color: {priority_color[rec['priority']]}; 
                                    color: white; padding: 4px 12px; border-radius: 15px; 
                                    font-size: 0.9rem; font-weight: 600;">
                            {rec['priority'].upper()}
                        </span>
                    </div>
                    <p>{rec['description']}</p>
                    <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 10px;">
                        <strong>📌 Action:</strong> {rec['action']}<br>
                        <strong>🎯 Impact:</strong> {rec['impact']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<h2 class="section-header">🕒 Recent Activity</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">📝 Recent Orders</div>', unsafe_allow_html=True)
        
        recent_orders = st.session_state.portal.orders.sort_values('order_date', ascending=False).head(5)
        
        for _, order in recent_orders.iterrows():
            status_color = {
                'Quote': '#6c757d',
                'Confirmed': '#17a2b8',
                'Production': '#ffc107',
                'Shipped': '#28a745',
                'Delivered': '#006400',
                'Cancelled': '#dc3545'
            }.get(order['status'], '#6c757d')
            
            st.markdown(f'''
            <div style="padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {status_color}; background: #f8f9fa;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{order['order_id']}</strong>
                    <span style="color: {status_color}; font-weight: 600;">{order['status']}</span>
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    Customer: {order['customer_id']} | Amount: ₹{order['amount']:,.0f}<br>
                    Date: {order['order_date']} | Priority: {order['priority']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.markdown('<div class="widget-header">🔔 System Alerts</div>', unsafe_allow_html=True)
        
        system_alerts = [
            {"type": "success", "message": "Production target achieved for week 45", "time": "2 hours ago"},
            {"type": "warning", "message": "Maintenance due for CNC Machine #2", "time": "5 hours ago"},
            {"type": "info", "message": "New software update available", "time": "1 day ago"},
            {"type": "critical", "message": "Raw material delivery delayed", "time": "1 day ago"},
            {"type": "success", "message": "Quality check passed for batch #2045", "time": "2 days ago"}
        ]
        
        for alert in system_alerts:
            alert_icon = {
                'success': '✅',
                'warning': '⚠️',
                'info': 'ℹ️',
                'critical': '🚨'
            }.get(alert['type'], '📌')
            
            st.markdown(f'''
            <div style="padding: 12px; margin: 8px 0; border-radius: 8px; background: #f8f9fa; border-left: 4px solid #ccc;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.2rem;">{alert_icon}</span>
                    <div style="flex: 1;">
                        <div>{alert['message']}</div>
                        <div style="color: #666; font-size: 0.9rem;">{alert['time']}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def production_page():
    """Production management page"""
    st.markdown('<h1 class="main-header">🏭 Production Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Production Schedule", "Machine Status", "Quality Control", "Work Orders"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Production Schedule</h2>', unsafe_allow_html=True)
        
        # Create sample production schedule
        schedule_data = []
        products = ['Mild Steel Worker Locker', 'SS Industrial Duct', 'Generator Control Panel', 
                   'Industrial Storage Rack', 'Sheet Metal Fabrication']
        
        for i in range(10):
            start_date = date.today() + timedelta(days=random.randint(0, 7))
            end_date = start_date + timedelta(days=random.randint(1, 5))
            
            schedule_data.append({
                'Work Order': f"WO{1000 + i}",
                'Product': random.choice(products),
                'Quantity': random.randint(10, 100),
                'Start Date': start_date.strftime("%Y-%m-%d"),
                'End Date': end_date.strftime("%Y-%m-%d"),
                'Status': random.choice(['Scheduled', 'In Progress', 'Completed', 'Delayed']),
                'Machine': random.choice(['CNC #1', 'Laser Cutter #2', 'Assembly Line #3', 'Painting Booth #4']),
                'Priority': random.choice(['High', 'Medium', 'Low'])
            })
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True)
        
        # Gantt Chart Visualization
        st.markdown('<h3 class="subsection-header">Production Timeline</h3>', unsafe_allow_html=True)
        
        # Create Gantt-like visualization
        fig = go.Figure()
        
        for idx, row in schedule_df.iterrows():
            fig.add_trace(go.Bar(
                y=[row['Work Order']],
                x=[(pd.to_datetime(row['End Date']) - pd.to_datetime(row['Start Date'])).days],
                base=row['Start Date'],
                orientation='h',
                name=row['Product'],
                text=[row['Status']],
                textposition='inside',
                marker_color={
                    'Scheduled': '#17a2b8',
                    'In Progress': '#ffc107',
                    'Completed': '#28a745',
                    'Delayed': '#dc3545'
                }[row['Status']]
            ))
        
        fig.update_layout(
            height=400,
            title="Production Schedule Gantt Chart",
            xaxis_title="Timeline",
            yaxis_title="Work Order",
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Machine Status Monitor</h2>', unsafe_allow_html=True)
        
        # Machine status data
        machines = [
            {"name": "CNC Machine #1", "status": "Running", "utilization": 85, "maintenance": "15 days"},
            {"name": "Laser Cutter #2", "status": "Idle", "utilization": 45, "maintenance": "3 days"},
            {"name": "Press Brake #3", "status": "Maintenance", "utilization": 0, "maintenance": "Today"},
            {"name": "Assembly Line #4", "status": "Running", "utilization": 92, "maintenance": "30 days"},
            {"name": "Painting Booth #5", "status": "Running", "utilization": 78, "maintenance": "7 days"},
            {"name": "Welding Station #6", "status": "Running", "utilization": 88, "maintenance": "21 days"},
        ]
        
        cols = st.columns(3)
        for idx, machine in enumerate(machines):
            with cols[idx % 3]:
                status_color = {
                    'Running': '#28a745',
                    'Idle': '#ffc107',
                    'Maintenance': '#dc3545'
                }.get(machine['status'], '#6c757d')
                
                st.markdown(f'''
                <div class="widget-card">
                    <h4>{machine['name']}</h4>
                    <div style="display: flex; align-items: center; gap: 10px; margin: 15px 0;">
                        <div style="width: 15px; height: 15px; border-radius: 50%; background-color: {status_color};"></div>
                        <span style="font-weight: 600; color: {status_color};">{machine['status']}</span>
                    </div>
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between;">
                            <span>Utilization:</span>
                            <span>{machine['utilization']}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {machine['utilization']}%"></div>
                        </div>
                    </div>
                    <div style="color: #666; font-size: 0.9rem;">
                        Next Maintenance: {machine['maintenance']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Machine performance chart
        st.markdown('<h3 class="subsection-header">Machine Performance Trends</h3>', unsafe_allow_html=True)
        
        performance_data = []
        for day in range(30, 0, -1):
            for machine in machines[:3]:
                performance_data.append({
                    'Date': (date.today() - timedelta(days=day)).strftime('%Y-%m-%d'),
                    'Machine': machine['name'],
                    'Utilization': random.randint(60, 95),
                    'Output': random.randint(80, 120)
                })
        
        perf_df = pd.DataFrame(performance_data)
        
        fig = px.line(
            perf_df[perf_df['Machine'].isin(['CNC Machine #1', 'Laser Cutter #2', 'Press Brake #3'])],
            x='Date',
            y='Utilization',
            color='Machine',
            title='Machine Utilization Over Time'
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Quality Control Dashboard</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Quality Yield", "97.8%", "0.5% ↑")
        with col2:
            st.metric("Defect Rate", "2.2%", "0.3% ↓")
        with col3:
            st.metric("Customer Returns", "0.8%", "0.1% ↓")
        
        # Quality metrics by product
        st.markdown('<h3 class="subsection-header">Quality Metrics by Product Line</h3>', unsafe_allow_html=True)
        
        quality_data = []
        for category, products in st.session_state.portal.products.items():
            for product in products[:2]:  # Take first 2 products from each category
                quality_data.append({
                    'Product': product['name'],
                    'Category': category,
                    'Defect Rate': random.uniform(0.5, 3.5),
                    'Yield': 100 - random.uniform(0.5, 3.5),
                    'Inspections': random.randint(50, 200)
                })
        
        quality_df = pd.DataFrame(quality_data)
        
        fig = px.scatter(
            quality_df,
            x='Defect Rate',
            y='Yield',
            size='Inspections',
            color='Category',
            hover_name='Product',
            title='Quality Performance by Product'
        )
        
        fig.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Work Order Management</h2>', unsafe_allow_html=True)
        
        # Create new work order
        with st.expander("➕ Create New Work Order", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                product = st.selectbox("Product", ["Mild Steel Worker Locker", "SS Industrial Duct", 
                                                 "Generator Control Panel", "Industrial Storage Rack"])
                quantity = st.number_input("Quantity", min_value=1, value=10)
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            with col2:
                start_date = st.date_input("Start Date", value=date.today())
                due_date = st.date_input("Due Date", value=date.today() + timedelta(days=7))
                assigned_to = st.selectbox("Assigned To", ["Production Team A", "Production Team B", 
                                                          "CNC Operators", "Assembly Team"])
            
            notes = st.text_area("Special Instructions")
            
            if st.button("Create Work Order", type="primary"):
                st.success("Work order created successfully!")
        
        # Work order list
        st.markdown('<h3 class="subsection-header">Active Work Orders</h3>', unsafe_allow_html=True)
        
        # Sample work orders
        work_orders = []
        for i in range(15):
            work_orders.append({
                'WO #': f"WO{2000 + i}",
                'Product': random.choice(['Mild Steel Worker Locker', 'SS Industrial Duct', 
                                        'Generator Control Panel', 'Industrial Storage Rack']),
                'Qty': random.randint(5, 50),
                'Status': random.choice(['Not Started', 'In Progress', 'Waiting Materials', 'QC Pending', 'Completed']),
                'Progress': random.randint(0, 100),
                'Start Date': (date.today() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
                'Due Date': (date.today() + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
                'Priority': random.choice(['High', 'Medium', 'Low'])
            })
        
        work_df = pd.DataFrame(work_orders)
        st.dataframe(work_df, use_container_width=True)

def inventory_page():
    """Inventory management page"""
    st.markdown('<h1 class="main-header">📦 Inventory Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Stock Overview", "Reorder Analysis", "Inventory Valuation", "Warehouse Management"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Inventory Dashboard</h2>', unsafe_allow_html=True)
        
        # Inventory summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        portal = st.session_state.portal
        
        with col1:
            total_items = len(portal.inventory)
            st.metric("Total Items", total_items)
        
        with col2:
            total_value = portal.inventory['value'].sum()
            st.metric("Total Value", f"₹{total_value:,.0f}")
        
        with col3:
            low_stock = len(portal.inventory[portal.inventory['current_stock'] < portal.inventory['min_stock']])
            st.metric("Low Stock Items", low_stock, "Needs attention" if low_stock > 0 else "All good")
        
        with col4:
            turnover = random.uniform(3.5, 8.5)
            st.metric("Inventory Turnover", f"{turnover:.1f}x", "Good" if turnover > 5 else "Needs improvement")
        
        # Inventory by category
        st.markdown('<h3 class="subsection-header">Inventory by Category</h3>', unsafe_allow_html=True)
        
        category_summary = portal.inventory.groupby('category').agg({
            'current_stock': 'sum',
            'value': 'sum',
            'item_id': 'count'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                category_summary,
                x='category',
                y='current_stock',
                title='Stock Quantity by Category',
                color='category',
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                category_summary,
                values='value',
                names='category',
                title='Inventory Value Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Low stock alerts
        st.markdown('<h3 class="subsection-header">⚠️ Low Stock Alerts</h3>', unsafe_allow_html=True)
        
        low_stock_items = portal.inventory[
            portal.inventory['current_stock'] < portal.inventory['min_stock']
        ].sort_values('current_stock')
        
        if len(low_stock_items) > 0:
            for _, item in low_stock_items.head(5).iterrows():
                shortage = item['min_stock'] - item['current_stock']
                st.markdown(f'''
                <div style="padding: 15px; margin: 10px 0; border-radius: 10px; background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%); border-left: 4px solid #dc3545;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{item['name']}</strong> ({item['item_id']})<br>
                            <span style="color: #666; font-size: 0.9rem;">
                                Current: {item['current_stock']} {item['unit']} | Minimum: {item['min_stock']} {item['unit']}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #dc3545; font-weight: 600;">Shortage: {shortage} {item['unit']}</span><br>
                            <span style="color: #666; font-size: 0.9rem;">Location: {item['location']}</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            if len(low_stock_items) > 5:
                st.info(f"⚠️ {len(low_stock_items) - 5} more items are low on stock")
        else:
            st.success("✅ All inventory items are at or above minimum stock levels")
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Reorder Analysis</h2>', unsafe_allow_html=True)
        
        # Reorder analysis
        portal = st.session_state.portal
        
        # Calculate reorder points
        reorder_analysis = []
        for _, item in portal.inventory.iterrows():
            if item['max_stock'] > 0 and item['min_stock'] > 0:
                reorder_point = item['min_stock']
                order_qty = item['max_stock'] - item['current_stock']
                
                if item['current_stock'] <= reorder_point and order_qty > 0:
                    reorder_analysis.append({
                        'Item ID': item['item_id'],
                        'Item Name': item['name'],
                        'Current Stock': item['current_stock'],
                        'Min Stock': item['min_stock'],
                        'Max Stock': item['max_stock'],
                        'Reorder Qty': order_qty,
                        'Unit': item['unit'],
                        'Location': item['location'],
                        'Status': 'Critical' if item['current_stock'] < item['min_stock'] * 0.5 else 'Warning'
                    })
        
        if reorder_analysis:
            reorder_df = pd.DataFrame(reorder_analysis)
            
            # Summary
            col1, col2 = st.columns(2)
            with col1:
                critical_items = len(reorder_df[reorder_df['Status'] == 'Critical'])
                st.metric("Critical Items", critical_items)
            
            with col2:
                total_reorder_qty = reorder_df['Reorder Qty'].sum()
                st.metric("Total Reorder Qty", f"{total_reorder_qty:,}")
            
            # Display reorder list
            st.dataframe(reorder_df, use_container_width=True)
            
            # Generate purchase order
            st.markdown('<h3 class="subsection-header">Generate Purchase Orders</h3>', unsafe_allow_html=True)
            
            selected_items = st.multiselect(
                "Select items for purchase order",
                options=reorder_df['Item Name'].tolist(),
                default=reorder_df[reorder_df['Status'] == 'Critical']['Item Name'].tolist()[:3]
            )
            
            if selected_items:
                selected_df = reorder_df[reorder_df['Item Name'].isin(selected_items)]
                
                st.markdown("**Selected Items for Purchase Order:**")
                for _, item in selected_df.iterrows():
                    st.write(f"- {item['Item Name']}: {item['Reorder Qty']} {item['Unit']}")
                
                if st.button("📋 Generate Purchase Order", type="primary"):
                    po_number = f"PO{random.randint(10000, 99999)}"
                    st.success(f"Purchase Order {po_number} generated successfully!")
                    st.info("Purchase order has been sent to suppliers for quotation")
        else:
            st.success("✅ No items require reordering at this time")
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Inventory Valuation</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Inventory valuation metrics
        total_value = portal.inventory['value'].sum()
        avg_value_per_item = total_value / len(portal.inventory)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Inventory Value", f"₹{total_value:,.0f}")
        
        with col2:
            st.metric("Average Value per Item", f"₹{avg_value_per_item:,.0f}")
        
        with col3:
            slow_moving = len(portal.inventory[portal.inventory['value'] > 10000])
            st.metric("High-Value Items (>₹10K)", slow_moving)
        
        # Value distribution
        st.markdown('<h3 class="subsection-header">Value Distribution Analysis</h3>', unsafe_allow_html=True)
        
        fig = px.histogram(
            portal.inventory,
            x='value',
            nbins=20,
            title='Distribution of Item Values',
            color_discrete_sequence=['#006400']
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Item Value (₹)",
            yaxis_title="Count",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ABC Analysis
        st.markdown('<h3 class="subsection-header">ABC Analysis</h3>', unsafe_allow_html=True)
        
        # Sort items by value
        sorted_inventory = portal.inventory.sort_values('value', ascending=False).copy()
        sorted_inventory['cumulative_value'] = sorted_inventory['value'].cumsum()
        sorted_inventory['cumulative_percentage'] = (sorted_inventory['cumulative_value'] / total_value) * 100
        
        # Classify as A, B, or C items
        def classify_abc(cum_pct):
            if cum_pct <= 80:
                return 'A'
            elif cum_pct <= 95:
                return 'B'
            else:
                return 'C'
        
        sorted_inventory['ABC_Class'] = sorted_inventory['cumulative_percentage'].apply(classify_abc)
        
        # Display ABC analysis
        abc_summary = sorted_inventory.groupby('ABC_Class').agg({
            'item_id': 'count',
            'value': 'sum'
        }).reset_index()
        
        abc_summary['Percentage'] = (abc_summary['value'] / total_value) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(abc_summary, use_container_width=True)
        
        with col2:
            fig = px.pie(
                abc_summary,
                values='value',
                names='ABC_Class',
                title='ABC Analysis - Value Distribution',
                color='ABC_Class',
                color_discrete_map={'A': '#dc3545', 'B': '#ffc107', 'C': '#28a745'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **ABC Analysis Guide:**
        - **A Items (Top 80% of value):** High-value items requiring tight control
        - **B Items (Next 15% of value):** Moderate-value items
        - **C Items (Last 5% of value):** Low-value items, simplify control
        """)
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Warehouse Management</h2>', unsafe_allow_html=True)
        
        # Warehouse locations
        warehouses = {
            'Warehouse A': {'capacity': 10000, 'used': 6500, 'items': 45},
            'Warehouse B': {'capacity': 8000, 'used': 4200, 'items': 32},
            'Production Area': {'capacity': 3000, 'used': 2800, 'items': 28},
            'Finished Goods Store': {'capacity': 5000, 'used': 3200, 'items': 38}
        }
        
        cols = st.columns(4)
        for idx, (wh_name, wh_data) in enumerate(warehouses.items()):
            with cols[idx]:
                utilization = (wh_data['used'] / wh_data['capacity']) * 100
                
                st.markdown(f'''
                <div class="widget-card">
                    <h4>{wh_name}</h4>
                    <div style="margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between;">
                            <span>Utilization:</span>
                            <span>{utilization:.1f}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {utilization}%"></div>
                        </div>
                    </div>
                    <div style="color: #666; font-size: 0.9rem;">
                        📦 {wh_data['items']} items<br>
                        📊 {wh_data['used']} / {wh_data['capacity']} units
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Movement log
        st.markdown('<h3 class="subsection-header">Recent Inventory Movements</h3>', unsafe_allow_html=True)
        
        movements = []
        for i in range(20):
            movements.append({
                'Date': (date.today() - timedelta(days=random.randint(0, 7))).strftime('%Y-%m-%d'),
                'Time': f"{random.randint(8, 18)}:{random.randint(0, 59):02d}",
                'Item': random.choice(['Steel Sheets', 'GI Coils', 'Lockers', 'Ducts', 'Panels']),
                'Type': random.choice(['Receipt', 'Issue', 'Transfer', 'Adjustment']),
                'Quantity': random.randint(1, 100),
                'From': random.choice(list(warehouses.keys())),
                'To': random.choice(list(warehouses.keys())),
                'User': random.choice(['Rajesh', 'Priya', 'Amit', 'Neha', 'Vikram'])
            })
        
        movements_df = pd.DataFrame(movements)
        st.dataframe(movements_df, use_container_width=True)

def sales_orders_page():
    """Sales and orders management page"""
    st.markdown('<h1 class="main-header">💰 Sales & Orders Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Order Pipeline", "Sales Analytics", "Customer Quotes", "Order Fulfillment"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Order Pipeline</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Pipeline metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            quotes = len(portal.orders[portal.orders['status'] == 'Quote'])
            st.metric("Quotes", quotes)
        
        with col2:
            confirmed = len(portal.orders[portal.orders['status'] == 'Confirmed'])
            st.metric("Confirmed", confirmed)
        
        with col3:
            production = len(portal.orders[portal.orders['status'] == 'Production'])
            st.metric("Production", production)
        
        with col4:
            shipped = len(portal.orders[portal.orders['status'] == 'Shipped'])
            st.metric("Shipped", shipped)
        
        # Pipeline visualization
        st.markdown('<h3 class="subsection-header">Sales Pipeline Visualization</h3>', unsafe_allow_html=True)
        
        # Create funnel chart
        pipeline_stages = ['Quote', 'Confirmed', 'Production', 'QC', 'Ready for Shipment', 'Shipped', 'Delivered']
        pipeline_counts = []
        pipeline_values = []
        
        for stage in pipeline_stages:
            stage_orders = portal.orders[portal.orders['status'] == stage]
            pipeline_counts.append(len(stage_orders))
            pipeline_values.append(stage_orders['amount'].sum())
        
        fig = go.Figure(go.Funnel(
            y=pipeline_stages,
            x=pipeline_counts,
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.8,
            marker={"color": ["#006400", "#228B22", "#90EE90", "#FF8C00", "#1E90FF", "#6f42c1", "#20c997"]}
        ))
        
        fig.update_layout(
            height=500,
            title="Order Pipeline Funnel",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent orders table
        st.markdown('<h3 class="subsection-header">Recent Orders</h3>', unsafe_allow_html=True)
        
        recent_orders = portal.orders.sort_values('order_date', ascending=False).head(10)
        st.dataframe(recent_orders, use_container_width=True)
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Sales Analytics</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Sales metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_sales = portal.orders['amount'].sum()
            st.metric("Total Sales", f"₹{total_sales:,.0f}")
        
        with col2:
            avg_order_value = portal.orders['amount'].mean()
            st.metric("Average Order Value", f"₹{avg_order_value:,.0f}")
        
        with col3:
            orders_count = len(portal.orders)
            st.metric("Total Orders", orders_count)
        
        # Sales trend
        st.markdown('<h3 class="subsection-header">Sales Trend Analysis</h3>', unsafe_allow_html=True)
        
        # Aggregate sales by month
        orders_by_month = portal.orders.copy()
        orders_by_month['order_date'] = pd.to_datetime(orders_by_month['order_date'])
        orders_by_month['month'] = orders_by_month['order_date'].dt.strftime('%Y-%m')
        monthly_sales = orders_by_month.groupby('month')['amount'].sum().reset_index()
        
        fig = px.line(
            monthly_sales.tail(12),
            x='month',
            y='amount',
            title='Monthly Sales Trend',
            markers=True
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Month",
            yaxis_title="Sales Amount (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sales by region
        st.markdown('<h3 class="subsection-header">Sales by Region</h3>', unsafe_allow_html=True)
        
        # Merge orders with customer region
        sales_by_region = portal.orders.merge(
            portal.customers[['customer_id', 'region']],
            on='customer_id',
            how='left'
        )
        
        region_sales = sales_by_region.groupby('region')['amount'].sum().reset_index()
        
        fig = px.bar(
            region_sales.sort_values('amount', ascending=False),
            x='region',
            y='amount',
            title='Sales by Region',
            color='region'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Region",
            yaxis_title="Sales Amount (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Customer Quotes</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Quote metrics
        quotes = portal.orders[portal.orders['status'] == 'Quote']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_quotes = len(quotes)
            st.metric("Active Quotes", total_quotes)
        
        with col2:
            quote_value = quotes['amount'].sum()
            st.metric("Total Quote Value", f"₹{quote_value:,.0f}")
        
        with col3:
            avg_quote_value = quotes['amount'].mean() if len(quotes) > 0 else 0
            st.metric("Average Quote Value", f"₹{avg_quote_value:,.0f}")
        
        # Create new quote
        with st.expander("➕ Create New Quote", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                customer = st.selectbox("Customer", portal.customers['name'].tolist()[:20])
                product_category = st.selectbox("Product Category", list(portal.products.keys()))
            
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1)
                delivery_date = st.date_input("Delivery Date", value=date.today() + timedelta(days=14))
            
            # Get products for selected category
            if product_category in portal.products:
                product_options = [p['name'] for p in portal.products[product_category]]
                product = st.selectbox("Product", product_options)
                
                # Find product price
                product_price = next((p['price'] for p in portal.products[product_category] if p['name'] == product), 0)
                total_price = product_price * quantity
                
                st.markdown(f"**Price per unit:** ₹{product_price:,.0f}")
                st.markdown(f"**Total quote value:** ₹{total_price:,.0f}")
            
            notes = st.text_area("Quote Notes")
            
            if st.button("Generate Quote", type="primary"):
                quote_id = f"QUOTE{random.randint(10000, 99999)}"
                st.success(f"Quote {quote_id} generated successfully!")
                st.info(f"Total value: ₹{total_price:,.0f}")
        
        # Quote list
        st.markdown('<h3 class="subsection-header">Active Quotes</h3>', unsafe_allow_html=True)
        
        if len(quotes) > 0:
            # Convert to DataFrame for display
            quotes_display = quotes[['order_id', 'customer_id', 'order_date', 'amount', 'priority', 'sales_rep']].copy()
            quotes_display['actions'] = "🔍 View | ✏️ Edit | ✅ Convert"
            
            st.dataframe(quotes_display, use_container_width=True)
        else:
            st.info("No active quotes at the moment")
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Order Fulfillment</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Fulfillment metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            on_time_orders = len(portal.orders[portal.orders['status'] == 'Delivered'])
            total_delivered = len(portal.orders[portal.orders['status'].isin(['Delivered', 'Shipped'])])
            on_time_rate = (on_time_orders / total_delivered * 100) if total_delivered > 0 else 0
            st.metric("On-time Delivery", f"{on_time_rate:.1f}%")
        
        with col2:
            pending_shipment = len(portal.orders[portal.orders['status'] == 'Ready for Shipment'])
            st.metric("Ready for Shipment", pending_shipment)
        
        with col3:
            in_production = len(portal.orders[portal.orders['status'] == 'Production'])
            st.metric("In Production", in_production)
        
        # Orders requiring attention
        st.markdown('<h3 class="subsection-header">Orders Requiring Attention</h3>', unsafe_allow_html=True)
        
        urgent_orders = portal.orders[
            (portal.orders['priority'] == 'High') & 
            (portal.orders['status'].isin(['Confirmed', 'Production', 'QC']))
        ].sort_values('order_date')
        
        if len(urgent_orders) > 0:
            for _, order in urgent_orders.head(5).iterrows():
                days_open = (date.today() - pd.to_datetime(order['order_date']).date()).days
                
                st.markdown(f'''
                <div style="padding: 15px; margin: 10px 0; border-radius: 10px; background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border-left: 4px solid #ffc107;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{order['order_id']}</strong> - {order['status']}<br>
                            <span style="color: #666; font-size: 0.9rem;">
                                Customer: {order['customer_id']} | Amount: ₹{order['amount']:,.0f}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #dc3545; font-weight: 600;">Open for {days_open} days</span><br>
                            <span style="color: #666; font-size: 0.9rem;">Priority: {order['priority']}</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.success("✅ No urgent orders requiring attention")
        
        # Shipment tracking
        st.markdown('<h3 class="subsection-header">Shipment Tracking</h3>', unsafe_allow_html=True)
        
        shipments = portal.orders[portal.orders['status'].isin(['Shipped', 'Ready for Shipment'])]
        
        if len(shipments) > 0:
            for _, shipment in shipments.head(5).iterrows():
                tracking_status = random.choice(['In Transit', 'At Hub', 'Out for Delivery', 'Delivered'])
                estimated_delivery = (pd.to_datetime(shipment['order_date']) + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')
                
                st.markdown(f'''
                <div style="padding: 15px; margin: 10px 0; border-radius: 10px; background: #f8f9fa; border-left: 4px solid #17a2b8;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{shipment['order_id']}</strong><br>
                            <span style="color: #666; font-size: 0.9rem;">
                                To: {shipment['customer_id']} | Status: {tracking_status}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: #006400; font-weight: 600;">Est. Delivery: {estimated_delivery}</span><br>
                            <span style="color: #666; font-size: 0.9rem;">Carrier: {random.choice(['DTDC', 'Blue Dart', 'FedEx', 'Local'])}</span>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

def customers_page():
    """Customer management page"""
    st.markdown('<h1 class="main-header">👥 Customer Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Customer Database", "Customer Analytics", "Support Tickets", "Customer Feedback"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Customer Database</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Customer metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_customers = len(portal.customers)
            st.metric("Total Customers", total_customers)
        
        with col2:
            active_customers = len(portal.customers[portal.customers['status'] == 'Active'])
            st.metric("Active Customers", active_customers)
        
        with col3:
            avg_orders = portal.customers['total_orders'].mean()
            st.metric("Avg Orders per Customer", f"{avg_orders:.1f}")
        
        with col4:
            avg_spent = portal.customers['total_spent'].mean()
            st.metric("Avg Lifetime Value", f"₹{avg_spent:,.0f}")
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search Customers")
        
        with col2:
            industry_filter = st.multiselect(
                "Filter by Industry",
                options=portal.customers['industry'].unique(),
                default=[]
            )
        
        with col3:
            status_filter = st.multiselect(
                "Filter by Status",
                options=portal.customers['status'].unique(),
                default=['Active']
            )
        
        # Filter customers
        filtered_customers = portal.customers.copy()
        
        if search_term:
            filtered_customers = filtered_customers[
                filtered_customers['name'].str.contains(search_term, case=False) |
                filtered_customers['company'].str.contains(search_term, case=False) |
                filtered_customers['email'].str.contains(search_term, case=False)
            ]
        
        if industry_filter:
            filtered_customers = filtered_customers[filtered_customers['industry'].isin(industry_filter)]
        
        if status_filter:
            filtered_customers = filtered_customers[filtered_customers['status'].isin(status_filter)]
        
        # Display customers
        st.dataframe(
            filtered_customers[
                ['customer_id', 'name', 'company', 'industry', 'status', 
                 'total_orders', 'total_spent', 'last_order', 'sales_rep']
            ],
            use_container_width=True
        )
        
        # Customer details view
        st.markdown('<h3 class="subsection-header">Customer Details</h3>', unsafe_allow_html=True)
        
        selected_customer = st.selectbox(
            "Select a customer to view details",
            options=filtered_customers['name'].tolist()
        )
        
        if selected_customer:
            customer_data = filtered_customers[filtered_customers['name'] == selected_customer].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'''
                <div class="widget-card">
                    <h4>Customer Information</h4>
                    <p><strong>Customer ID:</strong> {customer_data['customer_id']}</p>
                    <p><strong>Company:</strong> {customer_data['company']}</p>
                    <p><strong>Industry:</strong> {customer_data['industry']}</p>
                    <p><strong>Region:</strong> {customer_data['region']}</p>
                    <p><strong>Status:</strong> <span style="color: {'#28a745' if customer_data['status'] == 'Active' else '#6c757d'}">
                        {customer_data['status']}
                    </span></p>
                    <p><strong>Sales Rep:</strong> {customer_data['sales_rep']}</p>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="widget-card">
                    <h4>Purchase History</h4>
                    <p><strong>Total Orders:</strong> {customer_data['total_orders']}</p>
                    <p><strong>Total Spent:</strong> ₹{customer_data['total_spent']:,.0f}</p>
                    <p><strong>Avg Order Value:</strong> ₹{customer_data['total_spent']/customer_data['total_orders']:,.0f if customer_data['total_orders'] > 0 else 0}</p>
                    <p><strong>Customer Since:</strong> {customer_data['customer_since']}</p>
                    <p><strong>Last Order:</strong> {customer_data['last_order']}</p>
                    <p><strong>Credit Limit:</strong> ₹{customer_data['credit_limit']:,.0f}</p>
                </div>
                ''', unsafe_allow_html=True)
            
            # Customer's recent orders
            customer_orders = portal.orders[portal.orders['customer_id'] == customer_data['customer_id']]
            
            if len(customer_orders) > 0:
                st.markdown("**Recent Orders:**")
                st.dataframe(
                    customer_orders[
                        ['order_id', 'order_date', 'status', 'amount', 'products', 'quantity']
                    ].sort_values('order_date', ascending=False).head(5),
                    use_container_width=True
                )
            else:
                st.info("No orders found for this customer")
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Customer Analytics</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Customer segmentation
        st.markdown('<h3 class="subsection-header">Customer Segmentation</h3>', unsafe_allow_html=True)
        
        # RFM Analysis
        # Recency: Days since last order
        # Frequency: Total number of orders
        # Monetary: Total amount spent
        
        # Calculate RFM scores
        customer_rfm = portal.customers.copy()
        
        # Convert dates
        customer_rfm['last_order'] = pd.to_datetime(customer_rfm['last_order'])
        customer_rfm['customer_since'] = pd.to_datetime(customer_rfm['customer_since'])
        
        # Recency: Days since last order (inverse for scoring)
        customer_rfm['recency_days'] = (pd.Timestamp.now() - customer_rfm['last_order']).dt.days
        customer_rfm['recency_score'] = pd.qcut(customer_rfm['recency_days'], q=4, labels=[4, 3, 2, 1])
        
        # Frequency: Total orders
        customer_rfm['frequency_score'] = pd.qcut(customer_rfm['total_orders'], q=4, labels=[1, 2, 3, 4])
        
        # Monetary: Total spent
        customer_rfm['monetary_score'] = pd.qcut(customer_rfm['total_spent'], q=4, labels=[1, 2, 3, 4])
        
        # RFM Segment
        customer_rfm['rfm_score'] = (
            customer_rfm['recency_score'].astype(str) +
            customer_rfm['frequency_score'].astype(str) +
            customer_rfm['monetary_score'].astype(str)
        )
        
        # Define segments
        def get_rfm_segment(score):
            if score in ['444', '443', '434', '433']:
                return 'Champions'
            elif score in ['344', '343', '334', '333', '342', '332']:
                return 'Loyal Customers'
            elif score in ['442', '441', '431', '422', '421', '411']:
                return 'Potential Loyalists'
            elif score in ['244', '243', '234', '233', '242', '232']:
                return 'Recent Customers'
            elif score in ['144', '143', '134', '133', '142', '132']:
                return 'Promising'
            elif score in ['424', '423', '414', '413', '412']:
                return 'Needs Attention'
            else:
                return 'Require Activation'
        
        customer_rfm['segment'] = customer_rfm['rfm_score'].apply(get_rfm_segment)
        
        # Display segmentation
        segment_counts = customer_rfm['segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        
        fig = px.bar(
            segment_counts,
            x='Segment',
            y='Count',
            title='Customer Segmentation',
            color='Segment'
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer lifetime value analysis
        st.markdown('<h3 class="subsection-header">Customer Lifetime Value Analysis</h3>', unsafe_allow_html=True)
        
        # Calculate CLV metrics
        clv_data = portal.customers.copy()
        clv_data['avg_order_value'] = clv_data['total_spent'] / clv_data['total_orders']
        clv_data['purchase_frequency'] = clv_data['total_orders'] / ((pd.Timestamp.now() - pd.to_datetime(clv_data['customer_since'])).dt.days / 365.25)
        clv_data['clv'] = clv_data['avg_order_value'] * clv_data['purchase_frequency']
        
        # Display top customers by CLV
        top_customers = clv_data.sort_values('clv', ascending=False).head(10)
        
        fig = px.bar(
            top_customers,
            x='name',
            y='clv',
            title='Top 10 Customers by Lifetime Value',
            color='clv',
            color_continuous_scale='Greens'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Customer",
            yaxis_title="Lifetime Value (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Churn risk analysis
        st.markdown('<h3 class="subsection-header">Churn Risk Analysis</h3>', unsafe_allow_html=True)
        
        # Calculate churn risk
        churn_data = portal.customers.copy()
        churn_data['last_order'] = pd.to_datetime(churn_data['last_order'])
        churn_data['days_since_last_order'] = (pd.Timestamp.now() - churn_data['last_order']).dt.days
        
        # Simple churn risk calculation
        def calculate_churn_risk(days_since, total_orders):
            if days_since > 180 and total_orders < 5:
                return 'High Risk'
            elif days_since > 90:
                return 'Medium Risk'
            elif days_since > 30:
                return 'Low Risk'
            else:
                return 'Active'
        
        churn_data['churn_risk'] = churn_data.apply(
            lambda x: calculate_churn_risk(x['days_since_last_order'], x['total_orders']),
            axis=1
        )
        
        # Display churn risk distribution
        churn_counts = churn_data['churn_risk'].value_counts().reset_index()
        churn_counts.columns = ['Risk Level', 'Count']
        
        fig = px.pie(
            churn_counts,
            values='Count',
            names='Risk Level',
            title='Customer Churn Risk Distribution',
            color='Risk Level',
            color_discrete_map={
                'Active': '#28a745',
                'Low Risk': '#ffc107',
                'Medium Risk': '#fd7e14',
                'High Risk': '#dc3545'
            }
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # High-risk customers
        high_risk_customers = churn_data[churn_data['churn_risk'] == 'High Risk']
        
        if len(high_risk_customers) > 0:
            st.warning(f"⚠️ {len(high_risk_customers)} customers are at high risk of churn")
            
            for _, customer in high_risk_customers.head(3).iterrows():
                st.markdown(f'''
                <div style="padding: 12px; margin: 8px 0; border-radius: 8px; background: #f8d7da; border-left: 4px solid #dc3545;">
                    <strong>{customer['name']}</strong> ({customer['company']})<br>
                    <span style="color: #721c24; font-size: 0.9rem;">
                        Last order: {customer['last_order'].strftime('%Y-%m-%d')} 
                        ({customer['days_since_last_order']} days ago) | 
                        Total orders: {customer['total_orders']}
                    </span>
                </div>
                ''', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Customer Support Tickets</h2>', unsafe_allow_html=True)
        
        # Sample support tickets
        tickets = []
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        priorities = ['High', 'Medium', 'Low']
        categories = ['Technical Support', 'Billing Inquiry', 'Product Issue', 'Delivery Problem', 'General Inquiry']
        
        for i in range(25):
            created_date = date.today() - timedelta(days=random.randint(0, 30))
            updated_date = created_date + timedelta(days=random.randint(0, 7))
            
            tickets.append({
                'Ticket ID': f"TKT{1000 + i}",
                'Customer': f"Customer {random.randint(1, 150)}",
                'Category': random.choice(categories),
                'Subject': random.choice([
                    'Product not working properly',
                    'Invoice discrepancy',
                    'Delivery delay',
                    'Technical assistance needed',
                    'Warranty claim'
                ]),
                'Status': random.choice(statuses),
                'Priority': random.choice(priorities),
                'Created Date': created_date.strftime('%Y-%m-%d'),
                'Last Updated': updated_date.strftime('%Y-%m-%d'),
                'Assigned To': random.choice(['Support Team A', 'Support Team B', 'Rajesh', 'Priya']),
                'SLA': random.choice(['Within 24h', 'Within 48h', 'Within 7 days'])
            })
        
        tickets_df = pd.DataFrame(tickets)
        
        # Ticket metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            open_tickets = len(tickets_df[tickets_df['Status'] == 'Open'])
            st.metric("Open Tickets", open_tickets)
        
        with col2:
            high_priority = len(tickets_df[tickets_df['Priority'] == 'High'])
            st.metric("High Priority", high_priority)
        
        with col3:
            avg_response = "12.5 hours"
            st.metric("Avg Response Time", avg_response)
        
        with col4:
            resolution_rate = "94.2%"
            st.metric("Resolution Rate", resolution_rate)
        
        # Filter tickets
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=statuses,
                default=['Open', 'In Progress']
            )
        
        with col2:
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=priorities,
                default=['High', 'Medium']
            )
        
        # Apply filters
        filtered_tickets = tickets_df.copy()
        
        if status_filter:
            filtered_tickets = filtered_tickets[filtered_tickets['Status'].isin(status_filter)]
        
        if priority_filter:
            filtered_tickets = filtered_tickets[filtered_tickets['Priority'].isin(priority_filter)]
        
        # Display tickets
        st.dataframe(filtered_tickets, use_container_width=True)
        
        # Create new ticket
        with st.expander("➕ Create New Support Ticket", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                customer = st.selectbox("Customer", portal.customers['name'].tolist()[:20])
                category = st.selectbox("Category", categories)
                priority = st.selectbox("Priority", priorities)
            
            with col2:
                assigned_to = st.selectbox("Assign To", ['Support Team A', 'Support Team B', 'Rajesh', 'Priya', 'Amit'])
                sla = st.selectbox("SLA", ['Within 24h', 'Within 48h', 'Within 7 days'])
            
            subject = st.text_input("Subject")
            description = st.text_area("Description", height=150)
            
            if st.button("Create Ticket", type="primary"):
                ticket_id = f"TKT{random.randint(2000, 9999)}"
                st.success(f"Ticket {ticket_id} created successfully!")
                st.info(f"Assigned to: {assigned_to} | SLA: {sla}")
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Customer Feedback & Reviews</h2>', unsafe_allow_html=True)
        
        # Feedback metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Rating", "4.5/5.0", "0.2 ↑")
        
        with col2:
            st.metric("Total Reviews", "342", "12 this month")
        
        with col3:
            st.metric("Response Rate", "89%", "5% ↑")
        
        # Recent reviews
        st.markdown('<h3 class="subsection-header">Recent Customer Reviews</h3>', unsafe_allow_html=True)
        
        reviews = []
        sentiments = ['Positive', 'Neutral', 'Negative']
        
        for i in range(10):
            review_date = date.today() - timedelta(days=random.randint(0, 90))
            rating = random.randint(1, 5)
            
            reviews.append({
                'Date': review_date.strftime('%Y-%m-%d'),
                'Customer': f"Customer {random.randint(1, 150)}",
                'Rating': '⭐' * rating,
                'Numeric Rating': rating,
                'Product': random.choice(['Mild Steel Worker Locker', 'SS Industrial Duct', 'Generator Control Panel']),
                'Comment': random.choice([
                    'Excellent product quality and timely delivery.',
                    'Good service but delivery was delayed by 2 days.',
                    'Product met our expectations perfectly.',
                    'Facing some issues with installation, need support.',
                    'Very satisfied with the purchase, will buy again.'
                ]),
                'Sentiment': random.choice(sentiments),
                'Response': random.choice(['Replied', 'Pending', 'Not Required'])
            })
        
        reviews_df = pd.DataFrame(reviews)
        
        # Display reviews
        for _, review in reviews_df.iterrows():
            sentiment_color = {
                'Positive': '#28a745',
                'Neutral': '#6c757d',
                'Negative': '#dc3545'
            }.get(review['Sentiment'], '#6c757d')
            
            st.markdown(f'''
            <div style="padding: 15px; margin: 10px 0; border-radius: 10px; background: #f8f9fa; border-left: 4px solid {sentiment_color};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <strong>{review['Customer']}</strong> - {review['Product']}<br>
                        <span style="color: #ffc107; font-size: 1.2rem;">{review['Rating']}</span><br>
                        <span style="color: #666; font-size: 0.9rem;">{review['Comment']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: {sentiment_color}; font-weight: 600;">{review['Sentiment']}</span><br>
                        <span style="color: #666; font-size: 0.9rem;">{review['Date']}</span><br>
                        <span style="color: #666; font-size: 0.9rem;">Response: {review['Response']}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Sentiment analysis
        st.markdown('<h3 class="subsection-header">Customer Sentiment Analysis</h3>', unsafe_allow_html=True)
        
        sentiment_counts = reviews_df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        fig = px.pie(
            sentiment_counts,
            values='Count',
            names='Sentiment',
            title='Customer Sentiment Distribution',
            color='Sentiment',
            color_discrete_map={
                'Positive': '#28a745',
                'Neutral': '#6c757d',
                'Negative': '#dc3545'
            }
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def finance_page():
    """Financial management page"""
    st.markdown('<h1 class="main-header">💰 Financial Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Financial Dashboard", "Revenue Analysis", "Expense Tracking", "Cash Flow"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Financial Dashboard</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        finance = portal.financial_data
        
        # Key financial metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = finance['revenue']['revenue'].sum()
            st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
        
        with col2:
            total_profit = finance['revenue']['net_profit'].sum()
            st.metric("Total Profit", f"₹{total_profit:,.0f}")
        
        with col3:
            profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
        
        with col4:
            current_cash = finance['cashflow']['balance'].iloc[-1]
            st.metric("Cash Balance", f"₹{current_cash:,.0f}")
        
        # Financial charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue vs Profit trend
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=finance['revenue']['month'],
                y=finance['revenue']['revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#006400', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=finance['revenue']['month'],
                y=finance['revenue']['net_profit'],
                mode='lines+markers',
                name='Net Profit',
                line=dict(color='#FF8C00', width=3)
            ))
            
            fig.update_layout(
                title='Revenue vs Net Profit Trend',
                height=400,
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Expense breakdown
            fig = px.pie(
                finance['expenses'],
                values='amount',
                names='category',
                title='Expense Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Financial ratios
        st.markdown('<h3 class="subsection-header">Financial Ratios</h3>', unsafe_allow_html=True)
        
        # Calculate ratios
        current_ratio = random.uniform(1.5, 3.0)  # Simulated
        quick_ratio = random.uniform(1.0, 2.5)    # Simulated
        debt_to_equity = random.uniform(0.3, 1.5) # Simulated
        roe = (total_profit / 10000000) * 100     # Simulated equity base
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{current_ratio:.2f}</div>
                <div class="metric-label">Current Ratio</div>
                <div class="metric-change {'positive' if current_ratio > 2 else 'negative'}">
                    {'Good' if current_ratio > 2 else 'Needs Attention'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{quick_ratio:.2f}</div>
                <div class="metric-label">Quick Ratio</div>
                <div class="metric-change {'positive' if quick_ratio > 1.5 else 'negative'}">
                    {'Strong' if quick_ratio > 1.5 else 'Adequate'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{debt_to_equity:.2f}</div>
                <div class="metric-label">Debt to Equity</div>
                <div class="metric-change {'positive' if debt_to_equity < 1 else 'negative'}">
                    {'Conservative' if debt_to_equity < 1 else 'Aggressive'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div class="metric-value">{roe:.1f}%</div>
                <div class="metric-label">Return on Equity</div>
                <div class="metric-change {'positive' if roe > 15 else 'negative'}">
                    {'Excellent' if roe > 15 else 'Good'}
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Revenue Analysis</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        finance = portal.financial_data
        
        # Revenue breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly revenue growth
            revenue_growth = finance['revenue'].copy()
            revenue_growth['growth'] = revenue_growth['revenue'].pct_change() * 100
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=revenue_growth['month'],
                y=revenue_growth['revenue'],
                name='Revenue',
                marker_color='#006400'
            ))
            
            fig.add_trace(go.Scatter(
                x=revenue_growth['month'],
                y=revenue_growth['growth'],
                name='Growth %',
                yaxis='y2',
                line=dict(color='#FF8C00', width=3)
            ))
            
            fig.update_layout(
                title='Monthly Revenue & Growth Rate',
                height=400,
                xaxis_title="Month",
                yaxis_title="Revenue (₹)",
                yaxis2=dict(
                    title="Growth %",
                    overlaying='y',
                    side='right'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue by product category (simulated)
            product_revenue = []
            for category, products in portal.products.items():
                category_revenue = sum(p['price'] * random.randint(10, 100) for p in products)
                product_revenue.append({
                    'Category': category,
                    'Revenue': category_revenue,
                    'Percentage': (category_revenue / total_revenue * 100) if total_revenue > 0 else 0
                })
            
            product_revenue_df = pd.DataFrame(product_revenue)
            
            fig = px.bar(
                product_revenue_df.sort_values('Revenue', ascending=False),
                x='Category',
                y='Revenue',
                title='Revenue by Product Category',
                color='Revenue',
                color_continuous_scale='Greens'
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="Product Category",
                yaxis_title="Revenue (₹)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Revenue forecasting
        st.markdown('<h3 class="subsection-header">Revenue Forecasting</h3>', unsafe_allow_html=True)
        
        forecast_data = create_ai_forecast()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=finance['revenue']['month'].tail(6),
            y=finance['revenue']['revenue'].tail(6),
            mode='lines+markers',
            name='Historical',
            line=dict(color='#006400', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_data['sales_forecast']['Month'],
            y=forecast_data['sales_forecast']['Forecast'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#FF8C00', width=3, dash='dash')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_data['sales_forecast']['Month'].tolist() + forecast_data['sales_forecast']['Month'].tolist()[::-1],
            y=forecast_data['sales_forecast']['Upper_Bound'].tolist() + forecast_data['sales_forecast']['Lower_Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 140, 0, 0.2)',
            line=dict(color='rgba(255, 140, 0, 0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))
        
        fig.update_layout(
            title='Revenue Forecast (Next 6 Months)',
            height=400,
            xaxis_title="Month",
            yaxis_title="Revenue (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "6-Month Forecast",
                f"₹{forecast_data['metrics']['total_forecast']:,.0f}",
                f"₹{forecast_data['metrics']['avg_monthly_forecast']/1000:,.0f}K/month"
            )
        
        with col2:
            st.metric(
                "Expected Growth",
                f"{forecast_data['metrics']['growth_rate']:.1f}%",
                "per 6 months"
            )
        
        with col3:
            st.metric(
                "Confidence Level",
                f"{forecast_data['metrics']['confidence_level']*100:.0f}%",
                "Statistical confidence"
            )
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Expense Tracking</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        finance = portal.financial_data
        
        # Expense tracking metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_expenses = finance['expenses']['amount'].sum()
            st.metric("Total Expenses", f"₹{total_expenses:,.0f}")
        
        with col2:
            budget_variance = ((finance['expenses']['amount'].sum() - finance['expenses']['budget'].sum()) / 
                             finance['expenses']['budget'].sum() * 100) if finance['expenses']['budget'].sum() > 0 else 0
            st.metric("Budget Variance", f"{budget_variance:.1f}%", 
                     "Under" if budget_variance < 0 else "Over")
        
        with col3:
            avg_expense = finance['expenses']['amount'].mean()
            st.metric("Avg Expense per Category", f"₹{avg_expense:,.0f}")
        
        # Expense vs Budget
        st.markdown('<h3 class="subsection-header">Expense vs Budget Analysis</h3>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=finance['expenses']['category'],
            y=finance['expenses']['budget'],
            name='Budget',
            marker_color='#6c757d'
        ))
        
        fig.add_trace(go.Bar(
            x=finance['expenses']['category'],
            y=finance['expenses']['amount'],
            name='Actual',
            marker_color='#006400'
        ))
        
        fig.update_layout(
            title='Expense vs Budget by Category',
            height=500,
            xaxis_title="Expense Category",
            yaxis_title="Amount (₹)",
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Expense trends
        st.markdown('<h3 class="subsection-header">Expense Trends</h3>', unsafe_allow_html=True)
        
        # Simulated monthly expense data
        months = finance['revenue']['month'].tolist()
        expense_categories = finance['expenses']['category'].tolist()
        
        monthly_expenses = []
        for month in months:
            for category in expense_categories:
                monthly_expenses.append({
                    'Month': month,
                    'Category': category,
                    'Amount': random.randint(50000, 300000)
                })
        
        monthly_expenses_df = pd.DataFrame(monthly_expenses)
        
        # Select top 3 expense categories for trend
        top_categories = finance['expenses'].nlargest(3, 'amount')['category'].tolist()
        top_expenses = monthly_expenses_df[monthly_expenses_df['Category'].isin(top_categories)]
        
        fig = px.line(
            top_expenses,
            x='Month',
            y='Amount',
            color='Category',
            title='Top 3 Expense Categories Trend',
            markers=True
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Month",
            yaxis_title="Amount (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add new expense
        with st.expander("➕ Add New Expense", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                expense_date = st.date_input("Expense Date", value=date.today())
                category = st.selectbox("Category", expense_categories)
            
            with col2:
                amount = st.number_input("Amount (₹)", min_value=0, value=1000)
                payment_method = st.selectbox("Payment Method", 
                                            ['Bank Transfer', 'Cheque', 'Cash', 'Online Payment', 'Credit Card'])
            
            with col3:
                vendor = st.text_input("Vendor/Supplier")
                reference = st.text_input("Reference Number")
            
            description = st.text_area("Description")
            
            if st.button("Record Expense", type="primary"):
                st.success("Expense recorded successfully!")
                st.info(f"₹{amount:,.0f} recorded under {category}")
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Cash Flow Management</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        finance = portal.financial_data
        
        # Cash flow metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_balance = finance['cashflow']['balance'].iloc[-1]
            st.metric("Current Balance", f"₹{current_balance:,.0f}")
        
        with col2:
            avg_daily_inflow = finance['cashflow']['inflow'].mean()
            st.metric("Avg Daily Inflow", f"₹{avg_daily_inflow:,.0f}")
        
        with col3:
            avg_daily_outflow = finance['cashflow']['outflow'].mean()
            st.metric("Avg Daily Outflow", f"₹{avg_daily_outflow:,.0f}")
        
        # Cash flow chart
        st.markdown('<h3 class="subsection-header">Cash Flow Analysis</h3>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=finance['cashflow']['date'],
            y=finance['cashflow']['inflow'],
            name='Inflow',
            marker_color='#28a745'
        ))
        
        fig.add_trace(go.Bar(
            x=finance['cashflow']['date'],
            y=finance['cashflow']['outflow'],
            name='Outflow',
            marker_color='#dc3545'
        ))
        
        fig.add_trace(go.Scatter(
            x=finance['cashflow']['date'],
            y=finance['cashflow']['balance'],
            name='Balance',
            yaxis='y2',
            line=dict(color='#006400', width=3)
        ))
        
        fig.update_layout(
            title='Daily Cash Flow',
            height=500,
            xaxis_title="Date",
            yaxis_title="Daily Flow (₹)",
            yaxis2=dict(
                title="Balance (₹)",
                overlaying='y',
                side='right'
            ),
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Accounts receivable/payable
        st.markdown('<h3 class="subsection-header">Accounts Receivable & Payable</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Accounts Receivable
            ar_data = finance['invoices'][finance['invoices']['status'] != 'Paid']
            ar_total = ar_data['amount'].sum()
            ar_count = len(ar_data)
            
            st.markdown(f'''
            <div class="widget-card">
                <h4>📥 Accounts Receivable</h4>
                <div style="font-size: 2.5rem; font-weight: 800; color: #006400; margin: 15px 0;">
                    ₹{ar_total:,.0f}
                </div>
                <div style="color: #666;">
                    {ar_count} unpaid invoices<br>
                    Avg days outstanding: 32 days<br>
                    Overdue: ₹{ar_data[ar_data['status'] == 'Overdue']['amount'].sum():,.0f}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            # Accounts Payable (simulated)
            ap_total = random.randint(500000, 2000000)
            ap_count = random.randint(15, 40)
            overdue_ap = random.randint(100000, 500000)
            
            st.markdown(f'''
            <div class="widget-card">
                <h4>📤 Accounts Payable</h4>
                <div style="font-size: 2.5rem; font-weight: 800; color: #dc3545; margin: 15px 0;">
                    ₹{ap_total:,.0f}
                </div>
                <div style="color: #666;">
                    {ap_count} unpaid bills<br>
                    Avg days pending: 25 days<br>
                    Due this week: ₹{overdue_ap:,.0f}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Cash flow forecast
        st.markdown('<h3 class="subsection-header">Cash Flow Forecast</h3>', unsafe_allow_html=True)
        
        # Simulated forecast
        forecast_days = 30
        forecast_dates = [(date.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, forecast_days + 1)]
        
        forecast_inflow = []
        forecast_outflow = []
        forecast_balance = [current_balance]
        
        for i in range(forecast_days):
            inflow = random.randint(50000, 500000)
            outflow = random.randint(30000, 400000)
            balance = forecast_balance[-1] + inflow - outflow
            
            forecast_inflow.append(inflow)
            forecast_outflow.append(outflow)
            forecast_balance.append(balance)
        
        forecast_balance = forecast_balance[1:]  # Remove initial balance
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_inflow,
            mode='lines',
            name='Forecast Inflow',
            line=dict(color='#28a745', width=2, dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_outflow,
            mode='lines',
            name='Forecast Outflow',
            line=dict(color='#dc3545', width=2, dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_balance,
            mode='lines',
            name='Forecast Balance',
            line=dict(color='#006400', width=3)
        ))
        
        fig.update_layout(
            title='30-Day Cash Flow Forecast',
            height=400,
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cash position alerts
        min_cash_threshold = 1000000  # ₹10L minimum cash
        
        if current_balance < min_cash_threshold:
            st.error(f"⚠️ Cash balance below minimum threshold! Current: ₹{current_balance:,.0f} | Minimum: ₹{min_cash_threshold:,.0f}")
            
            # Recommendations
            st.markdown("**Recommendations:**")
            st.markdown("""
            1. Accelerate collection of overdue invoices
            2. Defer non-essential expenses
            3. Consider short-term financing options
            4. Review credit terms with suppliers
            """)
        else:
            st.success(f"✅ Healthy cash position: ₹{current_balance:,.0f} (above minimum threshold of ₹{min_cash_threshold:,.0f})")

def marketing_page():
    """Marketing management page"""
    st.markdown('<h1 class="main-header">🎯 Marketing & Lead Management</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Campaign Dashboard", "Lead Management", "Marketing Analytics", "Content Calendar"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">Marketing Campaign Dashboard</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Campaign metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_campaigns = len(portal.marketing_campaigns[portal.marketing_campaigns['status'] == 'Active'])
            st.metric("Active Campaigns", active_campaigns)
        
        with col2:
            total_leads = portal.leads['lead_id'].nunique()
            st.metric("Total Leads", total_leads)
        
        with col3:
            conversion_rate = (len(portal.leads[portal.leads['status'] == 'Closed Won']) / len(portal.leads) * 100) if len(portal.leads) > 0 else 0
            st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
        
        with col4:
            avg_cost_per_lead = portal.marketing_campaigns['cost_per_lead'].mean()
            st.metric("Avg Cost per Lead", f"₹{avg_cost_per_lead:,.0f}")
        
        # Campaign performance
        st.markdown('<h3 class="subsection-header">Campaign Performance</h3>', unsafe_allow_html=True)
        
        # Top performing campaigns
        top_campaigns = portal.marketing_campaigns.sort_values('roi', ascending=False).head(5)
        
        fig = px.bar(
            top_campaigns,
            x='name',
            y='roi',
            title='Top 5 Campaigns by ROI',
            color='roi',
            color_continuous_scale='Greens',
            text='roi'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Campaign",
            yaxis_title="ROI (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Campaign status overview
        st.markdown('<h3 class="subsection-header">Campaign Status Overview</h3>', unsafe_allow_html=True)
        
        campaign_status = portal.marketing_campaigns['status'].value_counts().reset_index()
        campaign_status.columns = ['Status', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                campaign_status,
                values='Count',
                names='Status',
                title='Campaign Status Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Campaign timeline
            active_campaigns = portal.marketing_campaigns[portal.marketing_campaigns['status'] == 'Active']
            
            if len(active_campaigns) > 0:
                st.markdown("**Active Campaigns Timeline:**")
                
                for _, campaign in active_campaigns.iterrows():
                    days_left = (pd.to_datetime(campaign['end_date']) - pd.Timestamp.now()).days
                    
                    st.markdown(f'''
                    <div style="padding: 12px; margin: 8px 0; border-radius: 8px; background: #f8f9fa; border-left: 4px solid #1E90FF;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{campaign['name']}</strong><br>
                                <span style="color: #666; font-size: 0.9rem;">
                                    {campaign['platform']} | Budget: ₹{campaign['budget']:,.0f}
                                </span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: {'#28a745' if days_left > 7 else '#ffc107'}; font-weight: 600;">
                                    {days_left} days left
                                </span><br>
                                <span style="color: #666; font-size: 0.9rem;">
                                    ROI: {campaign['roi']}%
                                </span>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.info("No active campaigns at the moment")
        
        # Create new campaign
        with st.expander("➕ Launch New Campaign", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_name = st.text_input("Campaign Name")
                platform = st.selectbox("Platform", 
                                      ['Email', 'LinkedIn', 'Google Ads', 'Trade Show', 'Social Media'])
                target_audience = st.selectbox("Target Audience",
                                             ['Manufacturing Companies', 'Construction Firms', 
                                              'Hospitality Sector', 'Government Projects', 'All Industries'])
            
            with col2:
                budget = st.number_input("Budget (₹)", min_value=1000, value=50000)
                start_date = st.date_input("Start Date", value=date.today())
                end_date = st.date_input("End Date", value=date.today() + timedelta(days=30))
            
            campaign_manager = st.selectbox("Campaign Manager",
                                          ['Marketing Team', 'Sales Team', 'External Agency', 'Rajesh Kumar', 'Priya Sharma'])
            
            objectives = st.text_area("Campaign Objectives")
            
            if st.button("Launch Campaign", type="primary"):
                campaign_id = f"CAMP{random.randint(70000, 79999)}"
                st.success(f"Campaign '{campaign_name}' launched successfully!")
                st.info(f"Campaign ID: {campaign_id} | Budget: ₹{budget:,.0f}")
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Lead Management System</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # Lead metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            new_leads = len(portal.leads[portal.leads['status'] == 'New'])
            st.metric("New Leads", new_leads)
        
        with col2:
            qualified_leads = len(portal.leads[portal.leads['status'] == 'Qualified'])
            st.metric("Qualified Leads", qualified_leads)
        
        with col3:
            pipeline_value = portal.leads[portal.leads['status'].isin(['New', 'Contacted', 'Qualified', 'Proposal Sent'])]['value'].sum()
            st.metric("Pipeline Value", f"₹{pipeline_value:,.0f}")
        
        with col4:
            win_rate = (len(portal.leads[portal.leads['status'] == 'Closed Won']) / 
                       len(portal.leads[portal.leads['status'].isin(['Closed Won', 'Closed Lost'])]) * 100) if len(portal.leads[portal.leads['status'].isin(['Closed Won', 'Closed Lost'])]) > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        # Lead pipeline
        st.markdown('<h3 class="subsection-header">Lead Pipeline</h3>', unsafe_allow_html=True)
        
        lead_stages = ['New', 'Contacted', 'Qualified', 'Proposal Sent', 'Negotiation', 'Closed Won', 'Closed Lost']
        lead_counts = []
        lead_values = []
        
        for stage in lead_stages:
            stage_leads = portal.leads[portal.leads['status'] == stage]
            lead_counts.append(len(stage_leads))
            lead_values.append(stage_leads['value'].sum())
        
        fig = go.Figure(go.Funnel(
            y=lead_stages,
            x=lead_counts,
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.8,
            marker={"color": ["#1E90FF", "#87CEEB", "#90EE90", "#FF8C00", "#FFD700", "#28a745", "#dc3545"]}
        ))
        
        fig.update_layout(
            height=500,
            title="Lead Conversion Funnel",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Lead list with filters
        st.markdown('<h3 class="subsection-header">Lead Management</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lead_status_filter = st.multiselect(
                "Filter by Status",
                options=portal.leads['status'].unique(),
                default=['New', 'Contacted', 'Qualified']
            )
        
        with col2:
            source_filter = st.multiselect(
                "Filter by Source",
                options=portal.leads['source'].unique(),
                default=[]
            )
        
        with col3:
            assigned_filter = st.multiselect(
                "Filter by Assigned To",
                options=portal.leads['assigned_to'].unique(),
                default=[]
            )
        
        # Apply filters
        filtered_leads = portal.leads.copy()
        
        if lead_status_filter:
            filtered_leads = filtered_leads[filtered_leads['status'].isin(lead_status_filter)]
        
        if source_filter:
            filtered_leads = filtered_leads[filtered_leads['source'].isin(source_filter)]
        
        if assigned_filter:
            filtered_leads = filtered_leads[filtered_leads['assigned_to'].isin(assigned_filter)]
        
        # Display leads
        st.dataframe(
            filtered_leads[
                ['lead_id', 'name', 'company', 'source', 'status', 'value', 
                 'conversion_probability', 'assigned_to', 'next_followup']
            ].sort_values('conversion_probability', ascending=False),
            use_container_width=True
        )
        
        # Add new lead
        with st.expander("➕ Add New Lead", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                lead_name = st.text_input("Lead Name")
                company = st.text_input("Company")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
            
            with col2:
                source = st.selectbox("Source", portal.leads['source'].unique())
                product_interest = st.selectbox("Product Interest", 
                                              ['Lockers', 'HVAC Ducts', 'Electrical Panels', 'Fabrication', 'Laser Cutting'])
                estimated_value = st.number_input("Estimated Value (₹)", min_value=0, value=50000)
                assigned_to = st.selectbox("Assign To", portal.leads['assigned_to'].unique())
            
            notes = st.text_area("Notes")
            
            if st.button("Add Lead", type="primary"):
                lead_id = f"LEAD{random.randint(60000, 69999)}"
                st.success(f"Lead '{lead_name}' added successfully!")
                st.info(f"Lead ID: {lead_id} | Assigned to: {assigned_to}")
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Marketing Analytics</h2>', unsafe_allow_html=True)
        
        portal = st.session_state.portal
        
        # ROI Analysis
        st.markdown('<h3 class="subsection-header">Marketing ROI Analysis</h3>', unsafe_allow_html=True)
        
        roi_data = portal.marketing_campaigns.copy()
        roi_data['roi_category'] = pd.cut(roi_data['roi'], 
                                         bins=[0, 100, 200, 500, 1000],
                                         labels=['Low (<100%)', 'Medium (100-200%)', 'High (200-500%)', 'Very High (>500%)'])
        
        roi_summary = roi_data.groupby('roi_category').agg({
            'campaign_id': 'count',
            'budget': 'sum',
            'roi': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                roi_summary,
                x='roi_category',
                y='campaign_id',
                title='Campaigns by ROI Category',
                color='roi_category',
                text='campaign_id'
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="ROI Category",
                yaxis_title="Number of Campaigns",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                roi_data,
                x='budget',
                y='roi',
                size='leads_generated',
                color='platform',
                hover_name='name',
                title='Budget vs ROI by Platform',
                log_x=True
            )
            
            fig.update_layout(
                height=400,
                xaxis_title="Budget (₹)",
                yaxis_title="ROI (%)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Lead Source Analysis
        st.markdown('<h3 class="subsection-header">Lead Source Effectiveness</h3>', unsafe_allow_html=True)
        
        lead_source_analysis = portal.leads.groupby('source').agg({
            'lead_id': 'count',
            'value': 'sum',
            'conversion_probability': 'mean'
        }).reset_index()
        
        lead_source_analysis.columns = ['Source', 'Lead Count', 'Total Value', 'Avg Conversion Probability']
        
        fig = px.bar(
            lead_source_analysis.sort_values('Lead Count', ascending=False),
            x='Source',
            y=['Lead Count', 'Total Value'],
            title='Lead Generation by Source',
            barmode='group'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Lead Source",
            yaxis_title="Count / Value",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost Analysis
        st.markdown('<h3 class="subsection-header">Marketing Cost Analysis</h3>', unsafe_allow_html=True)
        
        cost_data = portal.marketing_campaigns.copy()
        cost_data['cost_per_conversion'] = cost_data['spent'] / cost_data['conversions']
        cost_data['leads_per_spent'] = cost_data['leads_generated'] / cost_data['spent']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(
                cost_data,
                y='cost_per_lead',
                title='Cost per Lead Distribution',
                points='all'
            )
            
            fig.update_layout(
                height=300,
                yaxis_title="Cost per Lead (₹)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(
                cost_data,
                y='cost_per_conversion',
                title='Cost per Conversion Distribution',
                points='all'
            )
            
            fig.update_layout(
                height=300,
                yaxis_title="Cost per Conversion (₹)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Content & Event Calendar</h2>', unsafe_allow_html=True)
        
        # Content calendar
        events = []
        event_types = ['Blog Post', 'Social Media', 'Email Newsletter', 'Webinar', 'Trade Show', 'Product Launch']
        
        for i in range(20):
            event_date = date.today() + timedelta(days=random.randint(0, 60))
            events.append({
                'Date': event_date.strftime('%Y-%m-%d'),
                'Event': random.choice(event_types),
                'Title': f"{random.choice(['Q4', 'New Product', 'Industry', 'Case Study'])} {random.choice(['Launch', 'Update', 'Report', 'Webinar'])}",
                'Platform': random.choice(['Website', 'LinkedIn', 'Email', 'All Platforms']),
                'Status': random.choice(['Scheduled', 'In Progress', 'Completed', 'Cancelled']),
                'Assigned To': random.choice(['Marketing Team', 'Content Team', 'External Agency', 'Rajesh', 'Priya'])
            })
        
        events_df = pd.DataFrame(events)
        
        # Filter events
        col1, col2 = st.columns(2)
        
        with col1:
            event_type_filter = st.multiselect(
                "Filter by Event Type",
                options=event_types,
                default=event_types
            )
        
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=events_df['Status'].unique(),
                default=['Scheduled', 'In Progress']
            )
        
        # Apply filters
        filtered_events = events_df.copy()
        
        if event_type_filter:
            filtered_events = filtered_events[filtered_events['Event'].isin(event_type_filter)]
        
        if status_filter:
            filtered_events = filtered_events[filtered_events['Status'].isin(status_filter)]
        
        # Display calendar
        st.dataframe(
            filtered_events.sort_values('Date'),
            use_container_width=True
        )
        
        # Monthly calendar view
        st.markdown('<h3 class="subsection-header">Monthly Calendar View</h3>', unsafe_allow_html=True)
        
        # Create a simple calendar view for current month
        current_month = date.today().strftime('%B %Y')
        st.subheader(f"📅 {current_month}")
        
        # Get days in current month
        today = date.today()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Create calendar grid
        days_in_month = last_day.day
        first_weekday = first_day.weekday()  # Monday=0, Sunday=6
        
        # Create calendar
        calendar_html = '''
        <div style="background: white; border-radius: 10px; padding: 20px; margin: 20px 0;">
            <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; text-align: center;">
        '''
        
        # Day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days:
            calendar_html += f'<div style="font-weight: bold; padding: 10px; background: #f8f9fa; border-radius: 5px;">{day}</div>'
        
        # Empty cells for days before first day of month
        for _ in range(first_weekday):
            calendar_html += '<div style="padding: 10px;"></div>'
        
        # Days of the month
        month_events = filtered_events[filtered_events['Date'].str.startswith(today.strftime('%Y-%m'))]
        
        for day in range(1, days_in_month + 1):
            day_str = f"{today.strftime('%Y-%m')}-{day:02d}"
            day_events = month_events[month_events['Date'] == day_str]
            
            cell_class = "today" if day == today.day else ""
            event_count = len(day_events)
            
            calendar_html += f'''
            <div style="padding: 10px; border-radius: 5px; background: {'#e3f2fd' if event_count > 0 else '#f8f9fa'}; 
                         border: {'2px solid #1E90FF' if day == today.day else '1px solid #dee2e6'};">
                <div style="font-weight: bold; margin-bottom: 5px;">{day}</div>
            '''
            
            if event_count > 0:
                event_titles = [e['Title'] for _, e in day_events.head(2).iterrows()]
                for title in event_titles[:2]:
                    calendar_html += f'<div style="font-size: 0.8rem; color: #666; margin: 2px 0;">• {title[:15]}{"..." if len(title) > 15 else ""}</div>'
                
                if event_count > 2:
                    calendar_html += f'<div style="font-size: 0.8rem; color: #666;">+{event_count - 2} more</div>'
            
            calendar_html += '</div>'
        
        calendar_html += '</div></div>'
        
        st.markdown(calendar_html, unsafe_allow_html=True)
        
        # Add new event
        with st.expander("➕ Schedule New Event", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                event_title = st.text_input("Event Title")
                event_type = st.selectbox("Event Type", event_types)
                event_date = st.date_input("Event Date", value=date.today() + timedelta(days=7))
            
            with col2:
                platform = st.selectbox("Platform", ['Website', 'LinkedIn', 'Email', 'All Platforms', 'Multiple'])
                assigned_to = st.selectbox("Assigned To", ['Marketing Team', 'Content Team', 'External Agency', 'Rajesh', 'Priya'])
                priority = st.selectbox("Priority", ['High', 'Medium', 'Low'])
            
            description = st.text_area("Description")
            
            if st.button("Schedule Event", type="primary"):
                st.success(f"Event '{event_title}' scheduled for {event_date.strftime('%Y-%m-%d')}!")
                st.info(f"Type: {event_type} | Platform: {platform} | Assigned to: {assigned_to}")

def ai_assistant_page():
    """AI Assistant page"""
    st.markdown('<h1 class="main-header">🤖 AI Manufacturing Assistant</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Chat Assistant", "Predictive Analytics", "Process Optimization", "Grok AI"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">AI Chat Assistant</h2>', unsafe_allow_html=True)
        
        # Chat interface
        st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>AI Assistant:</strong> {message['content']}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input("Type your message...", key="chat_input", 
                                     placeholder="Ask about production, inventory, sales, or analytics...")
        
        with col2:
            send_button = st.button("Send", type="primary", use_container_width=True)
        
        # Quick action buttons
        st.markdown("**Quick Questions:**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Sales Report", use_container_width=True):
                user_input = "Show me current sales report"
        
        with col2:
            if st.button("📦 Inventory Status", use_container_width=True):
                user_input = "What's our inventory status?"
        
        with col3:
            if st.button("🏭 Production Issues", use_container_width=True):
                user_input = "Any production issues today?"
        
        with col4:
            if st.button("💰 Financial Forecast", use_container_width=True):
                user_input = "Give me financial forecast for next quarter"
        
        # Process user input
        if send_button and user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Generate AI response
            response = generate_ai_response(user_input)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Rerun to update chat display
            st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">Predictive Analytics</h2>', unsafe_allow_html=True)
        
        # Generate AI forecast
        forecast_data = create_ai_forecast()
        
        # Sales forecast visualization
        st.markdown('<h3 class="subsection-header">📈 Sales Forecast</h3>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=forecast_data['sales_forecast']['Month'],
            y=forecast_data['sales_forecast']['Forecast'],
            mode='lines+markers',
            name='AI Forecast',
            line=dict(color='#FF8C00', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_data['sales_forecast']['Month'].tolist() + forecast_data['sales_forecast']['Month'].tolist()[::-1],
            y=forecast_data['sales_forecast']['Upper_Bound'].tolist() + forecast_data['sales_forecast']['Lower_Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 140, 0, 0.2)',
            line=dict(color='rgba(255, 140, 0, 0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))
        
        fig.update_layout(
            height=400,
            title='AI-Powered Sales Forecast (Next 6 Months)',
            xaxis_title="Month",
            yaxis_title="Forecasted Revenue (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast insights
        st.markdown('<h3 class="subsection-header">🔍 Forecast Insights</h3>', unsafe_allow_html=True)
        
        insights = [
            f"**Total Forecast Revenue:** ₹{forecast_data['metrics']['total_forecast']:,.0f} over next 6 months",
            f"**Average Monthly Revenue:** ₹{forecast_data['metrics']['avg_monthly_forecast']:,.0f}",
            f"**Expected Growth Rate:** {forecast_data['metrics']['growth_rate']:.1f}% over forecast period",
            f"**Confidence Level:** {forecast_data['metrics']['confidence_level']*100:.0f}% statistical confidence",
            "**Seasonal Pattern:** Higher demand expected in months 2 and 5",
            "**Recommendation:** Increase inventory by 15% to meet forecasted demand"
        ]
        
        for insight in insights:
            st.markdown(f"- {insight}")
        
        # Demand forecasting by product
        st.markdown('<h3 class="subsection-header">📊 Product Demand Forecast</h3>', unsafe_allow_html=True)
        
        product_demand_data = []
        for category, data in forecast_data['product_demand'].items():
            product_demand_data.append({
                'Product Category': category,
                'Current Demand': data['current_demand'],
                'Projected Demand': data['projected_demand'],
                'Growth %': data['growth_percentage']
            })
        
        product_demand_df = pd.DataFrame(product_demand_data)
        
        fig = px.bar(
            product_demand_df,
            x='Product Category',
            y=['Current Demand', 'Projected Demand'],
            title='Product Category Demand Forecast',
            barmode='group'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Product Category",
            yaxis_title="Demand Value (₹)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Predictive maintenance
        st.markdown('<h3 class="subsection-header">🔧 Predictive Maintenance Alerts</h3>', unsafe_allow_html=True)
        
        maintenance_alerts = [
            {"machine": "CNC Machine #1", "issue": "Motor bearing wear detected", "probability": "85%", "eta_failure": "14-21 days"},
            {"machine": "Laser Cutter #2", "issue": "Cooling system efficiency dropping", "probability": "72%", "eta_failure": "30-45 days"},
            {"machine": "Assembly Line #3", "issue": "Conveyor belt tension variation", "probability": "63%", "eta_failure": "60-90 days"}
        ]
        
        for alert in maintenance_alerts:
            st.markdown(f'''
            <div style="padding: 15px; margin: 10px 0; border-radius: 10px; background: {'#fff3cd' if float(alert['probability'][:-1]) > 70 else '#f8f9fa'}; 
                         border-left: 4px solid {'#ffc107' if float(alert['probability'][:-1]) > 70 else '#6c757d'};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{alert['machine']}</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{alert['issue']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: {'#dc3545' if float(alert['probability'][:-1]) > 70 else '#6c757d'}; font-weight: 600;">
                            {alert['probability']} probability
                        </span><br>
                        <span style="color: #666; font-size: 0.9rem;">ETA failure: {alert['eta_failure']}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Process Optimization</h2>', unsafe_allow_html=True)
        
        # AI recommendations
        recommendations = generate_ai_recommendations()
        
        st.markdown('<h3 class="subsection-header">🎯 AI Optimization Recommendations</h3>', unsafe_allow_html=True)
        
        if recommendations:
            cols = st.columns(min(3, len(recommendations)))
            
            for idx, rec in enumerate(recommendations):
                with cols[idx % 3]:
                    priority_color = {
                        'high': '#DC3545',
                        'medium': '#FF8C00',
                        'low': '#006400'
                    }
                    
                    st.markdown(f'''
                    <div class="widget-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4>{rec['title']}</h4>
                            <span style="background-color: {priority_color[rec['priority']]}; 
                                        color: white; padding: 4px 12px; border-radius: 15px; 
                                        font-size: 0.9rem; font-weight: 600;">
                                {rec['priority'].upper()}
                            </span>
                        </div>
                        <p style="color: #666; font-size: 1rem;">{rec['description']}</p>
                        <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 10px;">
                            <strong>📌 Action:</strong> {rec['action']}<br>
                            <strong>🎯 Impact:</strong> {rec['impact']}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.info("No optimization recommendations at this time")
        
        # Process efficiency analysis
        st.markdown('<h3 class="subsection-header">📊 Process Efficiency Analysis</h3>', unsafe_allow_html=True)
        
        efficiency_data = get_production_efficiency()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Equipment Effectiveness", f"{efficiency_data['metrics']['avg_oee']:.1f}%",
                     "World class: >85%")
        
        with col2:
            st.metric("Defect Rate", f"{efficiency_data['metrics']['avg_defect_rate']:.2f}%",
                     "Target: <1.5%")
        
        with col3:
            st.metric("Total Downtime", f"{efficiency_data['metrics']['total_downtime']/60:.1f} hours",
                     "Last 30 days")
        
        with col4:
            st.metric("Capacity Utilization", f"{efficiency_data['metrics']['utilization']:.1f}%",
                     "Optimal: 85-90%")
        
        # Efficiency trend
        fig = px.line(
            efficiency_data['data'],
            x='date',
            y='oee',
            title='OEE Trend (Last 30 Days)',
            markers=True
        )
        
        fig.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="World Class")
        fig.add_hline(y=65, line_dash="dash", line_color="red", annotation_text="Minimum Target")
        
        fig.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="OEE (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost optimization
        st.markdown('<h3 class="subsection-header">💰 Cost Optimization Opportunities</h3>', unsafe_allow_html=True)
        
        cost_opportunities = [
            {"area": "Energy Consumption", "savings": "₹45,000/month", "action": "Install smart meters", "payback": "8 months"},
            {"area": "Raw Material Waste", "savings": "₹28,000/month", "action": "Implement lean manufacturing", "payback": "3 months"},
            {"area": "Maintenance Costs", "savings": "₹15,000/month", "action": "Predictive maintenance", "payback": "6 months"},
            {"area": "Logistics", "savings": "₹32,000/month", "action": "Optimize delivery routes", "payback": "4 months"}
        ]
        
        for opp in cost_opportunities:
            st.markdown(f'''
            <div style="padding: 12px; margin: 8px 0; border-radius: 8px; background: #f8f9fa; border-left: 4px solid #28a745;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{opp['area']}</strong><br>
                        <span style="color: #666; font-size: 0.9rem;">{opp['action']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #28a745; font-weight: 600;">{opp['savings']}</span><br>
                        <span style="color: #666; font-size: 0.9rem;">Payback: {opp['payback']}</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">Grok AI Integration</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 25px;">
            <h2 style="color: white; margin-bottom: 15px;">🚀 Grok AI Advanced Analytics</h2>
            <p style="font-size: 1.2rem;">Advanced AI-powered insights for manufacturing optimization, 
            predictive maintenance, and strategic decision-making.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grok AI chat
        st.markdown('<h3 class="subsection-header">💬 Grok AI Chat</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="chat-container" id="grok-chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.grok_chat_history:
            if message['role'] == 'user':
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message grok-message">
                    <strong>Grok AI:</strong> {message['content']}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Grok chat input
        col1, col2 = st.columns([5, 1])
        
        with col1:
            grok_input = st.text_input("Ask Grok AI...", key="grok_input",
                                     placeholder="Ask advanced manufacturing questions...")
        
        with col2:
            grok_send = st.button("Ask Grok", type="primary", use_container_width=True)
        
        # Grok capabilities
        st.markdown("**Grok AI Capabilities:**")
        
        capabilities = [
            "🤖 **Advanced predictive analytics** for sales and demand forecasting",
            "🔧 **Predictive maintenance** with failure probability analysis",
            "📊 **Process optimization** using machine learning algorithms",
            "💰 **Cost-benefit analysis** for capital investments",
            "🌍 **Market trend analysis** and competitive intelligence",
            "⚡ **Real-time anomaly detection** in production processes"
        ]
        
        for capability in capabilities:
            st.markdown(f"- {capability}")
        
        # Process Grok input
        if grok_send and grok_input:
            # Add user message to history
            st.session_state.grok_chat_history.append({
                'role': 'user',
                'content': grok_input,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Generate Grok response
            grok_response = generate_grok_response(grok_input)
            
            # Add Grok response to history
            st.session_state.grok_chat_history.append({
                'role': 'grok',
                'content': grok_response,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Rerun to update chat display
            st.rerun()
        
        # Grok analysis tools
        st.markdown('<h3 class="subsection-header">🔬 Grok AI Analysis Tools</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Deep Market Analysis", use_container_width=True):
                st.session_state.grok_chat_history.append({
                    'role': 'user',
                    'content': "Perform deep market analysis for our products",
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
                response = """**Grok AI Market Analysis:**
                
                **Market Trends:**
                - Growing demand for sustainable manufacturing solutions (15% CAGR)
                - Increased adoption of Industry 4.0 technologies in Indian manufacturing
                - Government initiatives boosting infrastructure projects
                
                **Competitive Analysis:**
                - Top 3 competitors hold 45% market share
                - Our unique value proposition: Customized solutions with quick turnaround
                - Price competitiveness: We're 12% below market average
                
                **Opportunities:**
                - Expand into Middle East market (projected 20% growth)
                - Develop smart locker solutions with IoT integration
                - Partner with construction tech companies
                
                **Recommendations:**
                1. Launch premium product line with IoT features
                2. Expand digital marketing presence
                3. Develop strategic partnerships in infrastructure sector"""
                
                st.session_state.grok_chat_history.append({
                    'role': 'grok',
                    'content': response,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                st.rerun()
        
        with col2:
            if st.button("⚡ Predictive Maintenance", use_container_width=True):
                st.session_state.grok_chat_history.append({
                    'role': 'user',
                    'content': "Analyze predictive maintenance needs",
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
                response = """**Grok AI Predictive Maintenance Analysis:**
                
                **Machine Health Status:**
                - CNC Machine #1: 92% health score, optimal performance
                - Laser Cutter #2: 78% health score, requires attention
                - Assembly Line #3: 85% health score, minor issues detected
                
                **Failure Predictions:**
                - Laser Cutter #2: 85% probability of cooling system failure in 14-21 days
                - CNC Machine #1: 15% probability of bearing wear in 30-45 days
                - Painting Booth #4: 60% probability of nozzle clog in 7-10 days
                
                **Maintenance Recommendations:**
                1. **Immediate Action:** Schedule maintenance for Laser Cutter #2 this week
                2. **Priority:** Replace filters in Painting Booth #4
                3. **Monitoring:** Increase monitoring frequency for CNC Machine #1
                
                **Cost Impact:**
                - Preventive maintenance cost: ₹45,000
                - Potential breakdown cost: ₹325,000
                - **ROI: 622%**"""
                
                st.session_state.grok_chat_history.append({
                    'role': 'grok',
                    'content': response,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                st.rerun()
        
        with col3:
            if st.button("📈 Investment Analysis", use_container_width=True):
                st.session_state.grok_chat_history.append({
                    'role': 'user',
                    'content': "Analyze ROI for new CNC machine investment",
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
                response = """**Grok AI Investment Analysis:**
                
                **New CNC Machine Investment:**
                - Cost: ₹2,500,000
                - Installation: ₹150,000
                - Training: ₹75,000
                - **Total Investment: ₹2,725,000**
                
                **Expected Benefits:**
                - Production capacity increase: 35%
                - Labor cost reduction: ₹45,000/month
                - Quality improvement: 40% reduction in defects
                - Energy efficiency: 15% reduction in power consumption
                
                **Financial Analysis:**
                - Annual savings: ₹1,080,000
                - Additional revenue: ₹1,200,000/year
                - **Total annual benefit: ₹2,280,000**
                
                **ROI Calculation:**
                - Payback period: **14.3 months**
                - 5-year ROI: **318%**
                - NPV (5 years): ₹6,450,000
                
                **Recommendation:**
                ✅ **STRONG INVESTMENT CASE** - Proceed with purchase"""
                
                st.session_state.grok_chat_history.append({
                    'role': 'grok',
                    'content': response,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                st.rerun()

def generate_ai_response(user_input):
    """Generate AI response based on user input"""
    portal = st.session_state.portal
    
    # Simple keyword-based response system
    user_input_lower = user_input.lower()
    
    if 'sales' in user_input_lower and 'report' in user_input_lower:
        total_sales = portal.orders['amount'].sum()
        recent_sales = portal.orders[portal.orders['order_date'] >= (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')]['amount'].sum()
        
        return f"""**Sales Report Summary:**
        
        📊 **Overall Sales Performance:**
        - Total Sales Revenue: ₹{total_sales:,.0f}
        - Last 30 Days Revenue: ₹{recent_sales:,.0f}
        - Average Order Value: ₹{portal.orders['amount'].mean():,.0f}
        
        📈 **Top Performing Products:**
        1. Generator Control Panel: ₹{random.randint(500000, 1000000):,.0f}
        2. SS Industrial Duct: ₹{random.randint(300000, 600000):,.0f}
        3. Mild Steel Worker Locker: ₹{random.randint(200000, 400000):,.0f}
        
        🎯 **Recommendations:**
        - Focus on upselling electrical panels (highest margin)
        - Increase inventory for top-selling products
        - Target construction companies for ducting systems"""
    
    elif 'inventory' in user_input_lower or 'stock' in user_input_lower:
        low_stock_items = len(portal.inventory[portal.inventory['current_stock'] < portal.inventory['min_stock']])
        total_inventory_value = portal.inventory['value'].sum()
        
        return f"""**Inventory Status:**
        
        📦 **Current Inventory Overview:**
        - Total Items in Stock: {len(portal.inventory):,}
        - Total Inventory Value: ₹{total_inventory_value:,.0f}
        - Items Below Minimum Stock: {low_stock_items}
        
        ⚠️ **Critical Items (Need Reordering):**
        1. Steel Sheets: 45 units (min: 100)
        2. GI Coils: 120 units (min: 150)
        3. Electrical Components: 85 units (min: 100)
        
        🔄 **Inventory Turnover:**
        - Current Turnover Rate: 4.2x/year
        - Target: 6.0x/year
        - **Action:** Optimize stock levels to improve turnover
        
        📋 **Recommendations:**
        1. Place purchase orders for critical items immediately
        2. Review safety stock levels for fast-moving items
        3. Consider JIT inventory for high-cost items"""
    
    elif 'production' in user_input_lower and ('issue' in user_input_lower or 'problem' in user_input_lower):
        return f"""**Production Status Report:**
        
        🏭 **Current Production Status:**
        - Active Work Orders: {len(portal.orders[portal.orders['status'] == 'Production']):,}
        - On-time Delivery Rate: 92.3%
        - Quality Yield: 97.8%
        
        ⚠️ **Current Issues:**
        1. **CNC Machine #2:** Scheduled maintenance overdue by 3 days
        2. **Raw Material Delay:** Steel sheets delivery delayed by 2 days
        3. **QC Issue:** Batch #2045 has 3% defect rate (above 2% target)
        
        🔧 **Resolution Actions:**
        - **Immediate:** Reschedule CNC maintenance for tomorrow
        - **Today:** Contact supplier for material ETA
        - **Ongoing:** Quality team investigating defect root cause
        
        📊 **Performance Metrics:**
        - Overall Equipment Effectiveness (OEE): 86.5%
        - Machine Utilization: 78.2%
        - Downtime (Last 7 days): 14.5 hours
        
        ✅ **Recommendations:**
        1. Implement predictive maintenance schedule
        2. Increase buffer stock for critical materials
        3. Review quality control procedures"""
    
    elif 'financial' in user_input_lower or 'forecast' in user_input_lower:
        forecast_data = create_ai_forecast()
        
        return f"""**Financial Forecast & Analysis:**
        
        📈 **Revenue Forecast (Next 6 Months):**
        - Total Forecast: ₹{forecast_data['metrics']['total_forecast']:,.0f}
        - Monthly Average: ₹{forecast_data['metrics']['avg_monthly_forecast']:,.0f}
        - Expected Growth: {forecast_data['metrics']['growth_rate']:.1f}%
        
        💰 **Current Financial Position:**
        - Cash Balance: ₹{portal.financial_data['cashflow']['balance'].iloc[-1]:,.0f}
        - Accounts Receivable: ₹{portal.financial_data['invoices'][portal.financial_data['invoices']['status'] != 'Paid']['amount'].sum():,.0f}
        - Profit Margin: {(portal.financial_data['revenue']['net_profit'].sum() / portal.financial_data['revenue']['revenue'].sum() * 100):.1f}%
        
        📊 **Key Financial Ratios:**
        - Current Ratio: 2.3 (Healthy: >2.0)
        - Quick Ratio: 1.8 (Good: >1.5)
        - Debt to Equity: 0.45 (Conservative: <1.0)
        
        🎯 **Financial Recommendations:**
        1. **Invest:** Allocate ₹500K for new equipment (ROI: 25%)
        2. **Optimize:** Reduce inventory holding costs by 15%
        3. **Grow:** Expand credit terms for top 20% customers
        
        ⚠️ **Risk Factors:**
        - Raw material prices increasing by 8% next quarter
        - Competitive pressure on pricing (3-5% erosion expected)
        - Labor cost inflation: 6% annually"""
    
    elif 'customer' in user_input_lower:
        active_customers = len(portal.customers[portal.customers['status'] == 'Active'])
        new_customers = len(portal.customers[pd.to_datetime(portal.customers['customer_since']) >= (date.today() - timedelta(days=90))])
        
        return f"""**Customer Analysis:**
        
        👥 **Customer Overview:**
        - Total Customers: {len(portal.customers):,}
        - Active Customers: {active_customers:,}
        - New Customers (Last 90 days): {new_customers:,}
        
        💰 **Customer Value Metrics:**
        - Average Lifetime Value: ₹{portal.customers['total_spent'].mean():,.0f}
        - Customer Acquisition Cost: ₹{random.randint(5000, 15000):,.0f}
        - Customer Retention Rate: 78.5%
        
        📊 **Customer Segmentation:**
        - **Champions (Top 20%):** 30 customers, 65% of revenue
        - **Loyal Customers:** 45 customers, 25% of revenue
        - **At Risk:** 25 customers, 10% of revenue
        
        ⭐ **Top 5 Customers by Revenue:**
        1. Company A: ₹2.5M total spend
        2. Company B: ₹1.8M total spend
        3. Company C: ₹1.5M total spend
        4. Company D: ₹1.2M total spend
        5. Company E: ₹950K total spend
        
        🎯 **Customer Strategy Recommendations:**
        1. **Retention:** Create loyalty program for top 20% customers
        2. **Growth:** Upsell/cross-sell to mid-tier customers
        3. **Acquisition:** Focus on manufacturing sector (highest LTV)
        4. **Reactivate:** Contact 15 dormant customers with special offers
        
        📈 **Growth Opportunities:**
        - **Referral Program:** 25% of new customers come from referrals
        - **Industry Focus:** Construction sector shows 35% growth potential
        - **Geographic Expansion:** South India market underpenetrated"""
    
    elif 'order' in user_input_lower and 'status' in user_input_lower:
        pending_orders = portal.orders[portal.orders['status'].isin(['Quote', 'Confirmed', 'Production'])]
        urgent_orders = pending_orders[pending_orders['priority'] == 'High']
        
        return f"""**Order Status Overview:**
        
        📋 **Order Pipeline:**
        - Total Orders: {len(portal.orders):,}
        - Pending Orders: {len(pending_orders):,}
        - Urgent Orders: {len(urgent_orders):,}
        
        📊 **Order Status Distribution:**
        - Quotes: {len(portal.orders[portal.orders['status'] == 'Quote']):,}
        - Confirmed: {len(portal.orders[portal.orders['status'] == 'Confirmed']):,}
        - Production: {len(portal.orders[portal.orders['status'] == 'Production']):,}
        - Shipped: {len(portal.orders[portal.orders['status'] == 'Shipped']):,}
        - Delivered: {len(portal.orders[portal.orders['status'] == 'Delivered']):,}
        
        ⚠️ **Orders Requiring Attention:**
        1. **ORD21058:** High priority, 3 days overdue
        2. **ORD21042:** Payment pending, 7 days overdue
        3. **ORD21067:** QC hold, needs resolution today
        
        🚚 **Shipping Status:**
        - On-time Delivery Rate: 92.3%
        - Average Delivery Time: 14.5 days
        - Shipping Cost as % of Revenue: 3.2%
        
        🎯 **Order Management Recommendations:**
        1. **Prioritize:** Focus on 5 overdue orders this week
        2. **Communicate:** Update customers on delayed orders
        3. **Optimize:** Batch similar orders for production efficiency
        4. **Automate:** Implement order tracking system
        
        📈 **Performance Metrics:**
        - Order Fulfillment Cycle Time: 18.5 days (Target: 15 days)
        - Perfect Order Rate: 85.7% (Target: 90%)
        - Order Accuracy: 98.2% (Excellent)"""
    
    elif 'lead' in user_input_lower or 'marketing' in user_input_lower:
        new_leads = len(portal.leads[portal.leads['status'] == 'New'])
        conversion_rate = (len(portal.leads[portal.leads['status'] == 'Closed Won']) / len(portal.leads) * 100)
        
        return f"""**Lead & Marketing Analysis:**
        
        🎯 **Lead Pipeline:**
        - Total Leads: {len(portal.leads):,}
        - New Leads: {new_leads:,}
        - Qualified Leads: {len(portal.leads[portal.leads['status'] == 'Qualified']):,}
        - Conversion Rate: {conversion_rate:.1f}%
        
        📊 **Lead Sources (Top 5):**
        1. Website: 35% of leads
        2. Referrals: 25% of leads
        3. Trade Shows: 15% of leads
        4. LinkedIn: 12% of leads
        5. Google Ads: 8% of leads
        
        💰 **Lead Quality Metrics:**
        - Average Lead Value: ₹{portal.leads['value'].mean():,.0f}
        - Cost per Lead: ₹{portal.marketing_campaigns['cost_per_lead'].mean():,.0f}
        - Lead to Customer Rate: 12.5%
        
        🏆 **Best Performing Campaigns:**
        1. **Q4 Manufacturing Promotion:** 45% ROI, 120 leads
        2. **LinkedIn Industry Campaign:** 38% ROI, 85 leads
        3. **Email Newsletter:** 25% ROI, 210 leads
        
        🎯 **Marketing Recommendations:**
        1. **Double Down:** Increase budget for Q4 campaign by 30%
        2. **Optimize:** Improve website conversion rate (current: 2.1%)
        3. **Expand:** Test WhatsApp Business for lead generation
        4. **Retarget:** Implement email nurture sequence for abandoned quotes
        
        📈 **Growth Opportunities:**
        - **Content Marketing:** Case studies increase conversions by 40%
        - **Partnerships:** Co-marketing with complementary businesses
        - **Automation:** Lead scoring system to prioritize high-value leads"""
    
    elif 'help' in user_input_lower or 'what can you do' in user_input_lower:
        return """**I can help you with:**
        
        📊 **Sales & Revenue:**
        - Current sales performance
        - Revenue forecasts and trends
        - Order pipeline analysis
        
        📦 **Inventory & Supply Chain:**
        - Stock levels and reorder points
        - Inventory optimization
        - Supplier performance
        
        🏭 **Production & Operations:**
        - Production status and issues
        - Quality control metrics
        - Equipment efficiency
        
        👥 **Customer Management:**
        - Customer analytics and segmentation
        - Customer value analysis
        - Retention strategies
        
        💰 **Finance & Accounting:**
        - Financial performance
        - Cash flow analysis
        - Cost optimization
        
        🎯 **Marketing & Leads:**
        - Campaign performance
        - Lead pipeline analysis
        - Marketing ROI
        
        🔮 **Predictive Analytics:**
        - Sales forecasting
        - Demand planning
        - Risk analysis
        
        💡 **Just ask me anything about your manufacturing business!**"""
    
    else:
        # Default response
        return f"""I understand you're asking about: "{user_input}"
        
        As your AI Manufacturing Assistant, I can help you analyze:
        
        🔍 **Based on your query, here's what I found:**
        - Your manufacturing portal has {len(portal.products)} product categories
        - You have {len(portal.customers)} active customers
        - Current order pipeline value: ₹{portal.orders[portal.orders['status'].isin(['Quote', 'Confirmed', 'Production'])]['amount'].sum():,.0f}
        
        💡 **For more specific information, you can ask me about:**
        - "Show me sales report"
        - "What's our inventory status?"
        - "Any production issues today?"
        - "Give me financial forecast"
        - "Analyze customer data"
        
        How else can I assist you with your manufacturing operations today?"""

def generate_grok_response(user_input):
    """Generate Grok AI response"""
    # Simulated Grok AI responses based on query
    user_input_lower = user_input.lower()
    
    responses = {
        'market': """**Grok AI Deep Market Analysis:**
        
        **Industry Insights:**
        - Global manufacturing growth: 3.8% CAGR (2023-2028)
        - Indian manufacturing sector: 7.5% expected growth
        - Key growth drivers: Infrastructure spending, Make in India, export demand
        
        **Competitive Landscape:**
        - **Direct Competitors:** 12 major players in your segment
        - **Market Share:** You hold approximately 8% of regional market
        - **Competitive Advantages:** Faster delivery (15% quicker), customization capability
        
        **Emerging Trends:**
        1. **Sustainability:** 42% of buyers prefer eco-friendly manufacturers
        2. **Digitalization:** IoT adoption growing at 28% annually
        3. **Automation:** Robotics adoption increasing by 35% year-over-year
        
        **Strategic Recommendations:**
        1. **Product Development:** Launch smart, connected products with IoT features
        2. **Market Expansion:** Target Middle East (20% growth) and Southeast Asia (15% growth)
        3. **Partnerships:** Collaborate with construction tech companies
        4. **Digital Transformation:** Implement AI-powered production planning
        
        **Risk Assessment:**
        - Raw material price volatility: High risk
        - Regulatory changes: Medium risk
        - Technology disruption: High risk
        
        **Action Plan:**
        - Short-term (0-6 months): Digital marketing optimization
        - Medium-term (6-18 months): Product line expansion
        - Long-term (18-36 months): International expansion""",
        
        'investment': """**Grok AI Investment Analysis Framework:**
        
        **Analysis Methodology:**
        - Machine learning models trained on 5,000+ manufacturing investments
        - Real-time market data integration
        - Competitor benchmarking analysis
        - Risk-adjusted return calculations
        
        **Current Investment Opportunities:**
        1. **Advanced CNC Machines:** 
           - ROI: 28-35% | Payback: 18-24 months
           - Risk: Low | Strategic Fit: High
        
        2. **Solar Power Installation:**
           - ROI: 22% | Payback: 42 months
           - Risk: Medium | Strategic Fit: Medium
        
        3. **AI Quality Control System:**
           - ROI: 45% | Payback: 14 months
           - Risk: Medium | Strategic Fit: High
        
        **Capital Allocation Strategy:**
        - **Growth Investments:** 60% of capital (new equipment, technology)
        - **Efficiency Investments:** 30% of capital (process optimization)
        - **Risk Management:** 10% of capital (insurance, hedging)
        
        **Financial Modeling:**
        - **Best Case:** 32% average ROI across portfolio
        - **Base Case:** 24% average ROI
        - **Worst Case:** 8% average ROI (recession scenario)
        
        **Implementation Roadmap:**
        1. **Phase 1 (Months 1-3):** CNC machine acquisition
        2. **Phase 2 (Months 4-9):** AI system implementation
        3. **Phase 3 (Months 10-18):** Solar power installation
        
        **Monitoring Framework:**
        - Monthly ROI tracking
        - Quarterly performance reviews
        - Annual strategic reassessment""",
        
        'optimization': """**Grok AI Process Optimization Analysis:**
        
        **Current State Analysis:**
        - Overall equipment effectiveness (OEE): 78.5% (Industry benchmark: 85%)
        - Production yield: 94.2% (Target: 97%)
        - Energy efficiency: 68% (Best practice: 85%)
        
        **Bottleneck Identification:**
        1. **Primary Bottleneck:** Material handling (23% of production time)
        2. **Secondary Bottleneck:** Quality inspection (15% of production time)
        3. **Tertiary Bottleneck:** Machine setup (12% of production time)
        
        **AI-Optimized Solutions:**
        
        **1. Material Handling Optimization:**
        - **Solution:** Automated guided vehicles (AGVs)
        - **Investment:** ₹1.2M
        - **Benefits:** 40% reduction in handling time
        - **ROI:** 35% | Payback: 20 months
        
        **2. Quality Inspection Automation:**
        - **Solution:** Computer vision inspection system
        - **Investment:** ₹850K
        - **Benefits:** 60% faster inspection, 50% fewer defects
        - **ROI:** 42% | Payback: 16 months
        
        **3. Smart Machine Setup:**
        - **Solution:** Digital twins and simulation
        - **Investment:** ₹600K
        - **Benefits:** 30% reduction in setup time
        - **ROI:** 28% | Payback: 22 months
        
        **Implementation Priority:**
        1. Quality inspection automation (highest ROI)
        2. Material handling optimization
        3. Smart machine setup
        
        **Expected Overall Impact:**
        - Production capacity increase: 22%
        - Cost reduction: 18%
        - Quality improvement: 45%
        - Energy savings: 12%"""
    }
    
    # Check for keywords
    for keyword, response in responses.items():
        if keyword in user_input_lower:
            return response
    
    # Default Grok response
    return """**Grok AI Analysis:**
    
    I've analyzed your query using advanced machine learning models trained on manufacturing data. Here are my insights:
    
    **Contextual Understanding:**
    - Your query relates to manufacturing optimization and strategic decision-making
    - Based on your company's current performance metrics and industry benchmarks
    
    **Advanced Analytics Applied:**
    1. **Predictive Modeling:** Time-series analysis of your production data
    2. **Pattern Recognition:** Identifying optimization opportunities
    3. **Risk Assessment:** Evaluating potential challenges and mitigations
    
    **Key Findings:**
    - Your operations show 78% efficiency score (industry average: 72%)
    - There's a 22% improvement opportunity through process optimization
    - Market conditions favor expansion in the next 6-12 months
    
    **Strategic Recommendations:**
    1. **Immediate Action:** Implement the top 3 quick-win optimizations
    2. **Medium-term:** Invest in digital transformation initiatives
    3. **Long-term:** Develop strategic partnerships for market expansion
    
    **Next Steps:**
    - Schedule a detailed analysis session with my advanced analytics module
    - Access real-time dashboards for continuous monitoring
    - Set up automated alerts for performance deviations
    
    **Would you like me to dive deeper into any specific area?**"""

def settings_page():
    """Settings and configuration page"""
    st.markdown('<h1 class="main-header">⚙️ System Settings & Configuration</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["User Management", "System Configuration", "Data Management", "Integration"])
    
    with tabs[0]:
        st.markdown('<h2 class="section-header">User Management</h2>', unsafe_allow_html=True)
        
        # User list
        users = [
            {"name": "Rajesh Kumar", "role": "Plant Manager", "email": "rajesh@manufacturing.com", "status": "Active", "last_login": "2024-01-15"},
            {"name": "Priya Sharma", "role": "Sales Manager", "email": "priya@manufacturing.com", "status": "Active", "last_login": "2024-01-14"},
            {"name": "Amit Patel", "role": "Production Head", "email": "amit@manufacturing.com", "status": "Active", "last_login": "2024-01-15"},
            {"name": "Neha Gupta", "role": "Inventory Manager", "email": "neha@manufacturing.com", "status": "Active", "last_login": "2024-01-13"},
            {"name": "Vikram Singh", "role": "Quality Head", "email": "vikram@manufacturing.com", "status": "Inactive", "last_login": "2023-12-20"},
            {"name": "Suresh Reddy", "role": "Finance Manager", "email": "suresh@manufacturing.com", "status": "Active", "last_login": "2024-01-14"}
        ]
        
        # Display users
        for user in users:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.write(f"**{user['name']}**")
                st.caption(user['email'])
            
            with col2:
                st.write(user['role'])
            
            with col3:
                status_color = "green" if user['status'] == "Active" else "gray"
                st.write(f":{status_color}[{user['status']}]")
                st.caption(f"Last login: {user['last_login']}")
            
            with col4:
                st.button("Edit", key=f"edit_{user['name']}", use_container_width=True)
        
        # Add new user
        with st.expander("➕ Add New User", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                new_role = st.selectbox("Role", ["Plant Manager", "Sales Manager", "Production Head", 
                                               "Inventory Manager", "Quality Head", "Finance Manager", "Operator"])
            
            with col2:
                new_department = st.selectbox("Department", ["Production", "Sales", "Inventory", 
                                                           "Quality", "Finance", "Maintenance"])
                access_level = st.selectbox("Access Level", ["Admin", "Manager", "Supervisor", "Operator"])
                status = st.selectbox("Status", ["Active", "Inactive"])
            
            if st.button("Add User", type="primary"):
                st.success(f"User {new_name} added successfully!")
    
    with tabs[1]:
        st.markdown('<h2 class="section-header">System Configuration</h2>', unsafe_allow_html=True)
        
        # General settings
        st.markdown('<h3 class="subsection-header">General Settings</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", "Manufacturing Solutions Pvt Ltd")
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
            timezone = st.selectbox("Timezone", ["IST (UTC+5:30)", "GMT (UTC+0)", "EST (UTC-5)", "PST (UTC-8)"])
        
        with col2:
            date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "DD-MM-YYYY", "MM/DD/YYYY"])
            language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu"])
            theme = st.selectbox("Theme", ["Light", "Dark", "Green (Current)"])
        
        # Notification settings
        st.markdown('<h3 class="subsection-header">Notification Settings</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            email_notifications = st.checkbox("Email Notifications", True)
            low_stock_alerts = st.checkbox("Low Stock Alerts", True)
            order_updates = st.checkbox("Order Status Updates", True)
        
        with col2:
            maintenance_alerts = st.checkbox("Maintenance Alerts", True)
            quality_alerts = st.checkbox("Quality Alerts", True)
            shipment_alerts = st.checkbox("Shipment Alerts", True)
        
        with col3:
            daily_reports = st.checkbox("Daily Reports", True)
            weekly_summary = st.checkbox("Weekly Summary", True)
            monthly_review = st.checkbox("Monthly Review", True)
        
        # Save settings
        if st.button("Save Configuration", type="primary"):
            st.success("Configuration saved successfully!")
    
    with tabs[2]:
        st.markdown('<h2 class="section-header">Data Management</h2>', unsafe_allow_html=True)
        
        # Data backup
        st.markdown('<h3 class="subsection-header">Data Backup & Restore</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Database Size", "245 MB")
            st.metric("Last Backup", "Today, 02:00 AM")
            st.metric("Backup Frequency", "Daily")
        
        with col2:
            if st.button("📥 Backup Now", use_container_width=True):
                st.success("Backup initiated successfully!")
            
            if st.button("📤 Restore Backup", use_container_width=True):
                st.info("Select backup file to restore")
        
        with col3:
            backup_location = st.selectbox("Backup Location", ["Local Server", "Cloud Storage", "Both"])
            retention_days = st.slider("Retention Period (days)", 7, 365, 30)
        
        # Data export
        st.markdown('<h3 class="subsection-header">Data Export</h3>', unsafe_allow_html=True)
        
        export_options = st.multiselect(
            "Select data to export",
            ["Customers", "Orders", "Inventory", "Suppliers", "Leads", "Financial Data", "Production Data"],
            default=["Customers", "Orders"]
        )
        
        export_format = st.radio("Export Format", ["CSV", "Excel", "JSON", "PDF"])
        
        if st.button("Export Data", type="primary"):
            st.success(f"Exporting {len(export_options)} datasets as {export_format}...")
            st.info("Your download will begin shortly")
        
        # Data cleanup
        st.markdown('<h3 class="subsection-header">Data Cleanup</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            delete_old_leads = st.checkbox("Delete leads older than 365 days")
            archive_old_orders = st.checkbox("Archive completed orders older than 180 days")
        
        with col2:
            if delete_old_leads or archive_old_orders:
                st.warning("⚠️ This action cannot be undone!")
                if st.button("Execute Cleanup", type="secondary"):
                    st.success("Data cleanup completed successfully!")
    
    with tabs[3]:
        st.markdown('<h2 class="section-header">System Integration</h2>', unsafe_allow_html=True)
        
        # Available integrations
        integrations = [
            {"name": "Accounting Software", "status": "Connected", "provider": "Tally/QuickBooks"},
            {"name": "CRM System", "status": "Connected", "provider": "Salesforce"},
            {"name": "ERP System", "status": "Pending", "provider": "SAP"},
            {"name": "E-commerce Platform", "status": "Connected", "provider": "Shopify"},
            {"name": "Payment Gateway", "status": "Connected", "provider": "Razorpay"},
            {"name": "Shipping Partners", "status": "Connected", "provider": "DTDC/Blue Dart"}
        ]
        
        # Display integrations
        for integration in integrations:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.write(f"**{integration['name']}**")
                st.caption(integration['provider'])
            
            with col2:
                status_color = "green" if integration['status'] == "Connected" else "orange"
                st.write(f":{status_color}[{integration['status']}]")
            
            with col3:
                if integration['status'] == "Connected":
                    st.button("Sync Now", key=f"sync_{integration['name']}", use_container_width=True)
                else:
                    st.button("Connect", key=f"connect_{integration['name']}", use_container_width=True)
            
            with col4:
                st.button("Configure", key=f"config_{integration['name']}", use_container_width=True)
        
        # API Settings
        st.markdown('<h3 class="subsection-header">API Configuration</h3>', unsafe_allow_html=True)
        
        api_key = st.text_input("API Key", type="password", value="••••••••••••••••••••••••••••••")
        
        col1, col2 = st.columns(2)
        
        with col1:
            api_rate_limit = st.number_input("API Rate Limit (requests/minute)", min_value=10, max_value=1000, value=100)
            webhook_url = st.text_input("Webhook URL")
        
        with col2:
            if st.button("Generate New API Key", use_container_width=True):
                st.success("New API key generated!")
            
            if st.button("Test Webhook", use_container_width=True):
                st.success("Webhook test successful!")

# ============================================
# MAIN APP
# ============================================

def main():
    """Main application"""
    # Render sidebar
    sidebar()
    
    # Render current page based on selection
    if st.session_state.current_page == "dashboard":
        dashboard_page()
    elif st.session_state.current_page == "production":
        production_page()
    elif st.session_state.current_page == "inventory":
        inventory_page()
    elif st.session_state.current_page == "sales":
        sales_orders_page()
    elif st.session_state.current_page == "customers":
        customers_page()
    elif st.session_state.current_page == "finance":
        finance_page()
    elif st.session_state.current_page == "marketing":
        marketing_page()
    elif st.session_state.current_page == "ai":
        ai_assistant_page()
    elif st.session_state.current_page == "settings":
        settings_page()

if __name__ == "__main__":
    main()