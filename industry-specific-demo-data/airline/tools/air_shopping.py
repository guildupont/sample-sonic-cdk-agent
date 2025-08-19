PRICES = {
    "VCE": {"min": 250, "max": 450},
    "BCN": {"min": 200, "max": 400},
    "NCE": {"min": 180, "max": 350},
    "PMI": {"min": 150, "max": 300},
    "ATH": {"min": 300, "max": 500},
    "SKG": {"min": 300, "max": 600},
    "CFU": {"min": 300, "max": 700},
    "HER": {"min": 300, "max": 800},
    "CUN": {"min": 700, "max": 1200},
    "MIA": {"min": 500, "max": 1000}
}

def get_air_destinations_and_respective_cheapest_prices(iOriginAirportCode: str) -> str:
    """
    Provides an array of available destinations and respective cheapest price per roundtrip passenger from an origin airport
    
    Parameters:
    - iOriginAirportCode: Origin airport code
    
    Returns:
    - List of destinations and their respective lowest prices. Prices are provided in USD.
    """
    available_destinations = []
    for destination, prices in PRICES.items():
        if destination != iOriginAirportCode:
            available_destinations.append(
                {"destination_airport_code": destination, "lowest_price": prices["min"]}
            )
    print(f"get_available_destinations_and_respective_cheapest_prices({iOriginAirportCode})={available_destinations}")
    oAvailableDestinationsAsString = str(available_destinations)
    return oAvailableDestinationsAsString
    #"\n---\n".join(available_destinations)

