"""
Configuration for India Quick-Commerce Operational Risk Monitor

Defines city tiers, SLA thresholds, and risk weights for operational risk scoring.
"""

# Indian city tiers based on population and quick-commerce market size
# Expanded to ~150 cities for comprehensive coverage and diverse risk distribution
CITY_TIERS = {
    'Tier 1': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune'],
    'Tier 2': ['Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Coimbatore', 'Chandigarh', 'Madurai', 'Jamshedpur', 'Raipur', 'Allahabad', 'Amritsar', 'Varanasi', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Srinagar', 'Ludhiana', 'Ghaziabad', 'Navi Mumbai', 'Vijayawada'],
    'Tier 3': ['Gwalior', 'Jabalpur', 'Bhubaneswar', 'Mysore', 'Tiruchirappalli', 'Salem', 'Warangal', 'Kochi', 'Thiruvananthapuram', 'Dehradun', 'Guwahati', 'Jalandhar', 'Bareilly', 'Aligarh', 'Gorakhpur', 'Bokaro Steel City', 'Asansol', 'Dhanbad', 'Hubli', 'Mangalore', 'Belgaum', 'Tirunelveli', 'Udaipur', 'Tiruppur', 'Kozhikode', 'Akola', 'Kurnool', 'Bellary', 'Patiala', 'Bhagalpur', 'Muzaffarnagar', 'Latur', 'Dhule', 'Rohtak', 'Korba', 'Bhilwara', 'Muzaffarpur', 'Ahmednagar', 'Mathura', 'Kollam', 'Avadi', 'Kadapa', 'Sambalpur', 'Bilaspur', 'Shahjahanpur', 'Satara', 'Bijapur', 'Rampur', 'Shivamogga', 'Chandrapur', 'Junagadh', 'Thrissur', 'Alwar', 'Bardhaman', 'Nizamabad', 'Parbhani', 'Tumkur', 'Khammam', 'Panipat', 'Darbhanga', 'Dewas', 'Ichalkaranji', 'Karnal', 'Bathinda', 'Jalna', 'Eluru', 'Barasat', 'Purnia', 'Satna', 'Mau', 'Sonipat', 'Farrukhabad', 'Sagar', 'Rourkela', 'Durg', 'Imphal', 'Ratlam', 'Hapur', 'Anantapur', 'Arrah', 'Karimnagar', 'Etawah', 'Bharatpur', 'Begusarai', 'Noida', 'Gurgaon', 'Greater Noida', 'Gandhinagar', 'Kalyan', 'Vasai', 'Aurangabad', 'Solapur', 'Kolhapur', 'Sangli', 'Malegaon', 'Jalgaon', 'Bhusawal', 'Amravati', 'Nanded', 'Osmanabad', 'Bidar', 'Gulbarga', 'Raichur', 'Hospet', 'Davangere', 'Hassan', 'Mandya', 'Chitradurga', 'Tumakuru', 'Kolar', 'Chikkaballapur', 'Ramanagara', 'Hosur', 'Krishnagiri', 'Dharmapuri', 'Erode', 'Namakkal', 'Karur', 'Dindigul', 'Theni', 'Virudhunagar', 'Sivakasi', 'Thoothukudi', 'Nagercoil', 'Kanyakumari']
}

# SLA thresholds (in minutes) for delivery time by city tier
# Lower tier = higher expectations for faster delivery
SLA_THRESHOLDS = {
    'Tier 1': {
        'target': 15,      # Target delivery time in minutes
        'warning': 25,     # Warning threshold
        'critical': 35     # Critical threshold
    },
    'Tier 2': {
        'target': 20,
        'warning': 30,
        'critical': 40
    },
    'Tier 3': {
        'target': 25,
        'warning': 35,
        'critical': 45
    }
}

# Risk weights for different factors (sum should be ~1.0)
RISK_WEIGHTS = {
    'traffic': 0.40,      # Traffic congestion has highest impact on delivery times
    'weather': 0.35,      # Weather (rain) significantly affects operations
    'demand': 0.25        # Demand surge can strain capacity
}

# Traffic congestion level thresholds
# congestion_level: 0-1 scale where 1 = maximum congestion
TRAFFIC_THRESHOLDS = {
    'low': 0.3,      # < 0.3 = Low risk
    'medium': 0.6,   # 0.3-0.6 = Medium risk
    'high': 0.8      # > 0.6 = High risk, > 0.8 = Critical
}

# Weather (rainfall) impact thresholds (mm per day)
WEATHER_THRESHOLDS = {
    'low': 5.0,      # < 5mm = Light rain, minimal impact
    'medium': 15.0,  # 5-15mm = Moderate rain, delays expected
    'high': 30.0     # > 15mm = Heavy rain, significant delays, > 30mm = Critical
}

# Demand index thresholds
# demand_index: normalized 0-1 scale where 1 = peak demand
DEMAND_THRESHOLDS = {
    'low': 0.5,      # < 0.5 = Normal demand
    'medium': 0.7,   # 0.5-0.7 = Elevated demand
    'high': 0.85     # > 0.7 = High demand, > 0.85 = Surge demand
}

# Temperature thresholds (Celsius) - extreme temperatures affect operations
TEMPERATURE_THRESHOLDS = {
    'cold_risk': 10,   # Below 10°C = cold weather risk
    'hot_risk': 40     # Above 40°C = extreme heat risk
}

# Risk score classification thresholds
RISK_SCORE_THRESHOLDS = {
    'low': 30,      # 0-30 = Low risk
    'medium': 60,   # 31-60 = Medium risk
    'high': 100     # 61-100 = High risk
}

def get_city_tier(city_name: str) -> str:
    """
    Get the tier for a given city name.
    
    Args:
        city_name: Name of the city
        
    Returns:
        Tier level ('Tier 1', 'Tier 2', 'Tier 3') or 'Unknown'
    """
    city_name_normalized = city_name.strip().title()
    
    for tier, cities in CITY_TIERS.items():
        if city_name_normalized in cities:
            return tier
    
    return 'Unknown'

def get_sla_thresholds(tier: str) -> dict:
    """
    Get SLA thresholds for a city tier.
    
    Args:
        tier: City tier ('Tier 1', 'Tier 2', 'Tier 3')
        
    Returns:
        Dictionary with target, warning, and critical thresholds
    """
    return SLA_THRESHOLDS.get(tier, SLA_THRESHOLDS['Tier 3'])

