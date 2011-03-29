def get_median(values):
    num_set = len(values)

    if num_set > 0:
        sorted_values = sorted(values)
        
        (mid_point, remainder) = divmod(num_set, 2)
        
        if remainder == 1:
            median = sorted_values[mid_point]
        else:
            median = (sorted_values[mid_point] + sorted_values[mid_point - 1]) / 2
    else:
        median = None
        
    return median

def get_median_prices(formulations):
    fob_prices = []
    landed_prices = []
    
    for formulation in formulations:
        fob_price = formulation['fob_price']
        landed_price = formulation['landed_price']
        
        if fob_price != None:
            fob_prices.append(fob_price)

        if landed_price != None:
            landed_prices.append(landed_price)

    median_fob_price = get_median(fob_prices)
    median_landed_price = get_median(landed_prices)

    return (median_fob_price, median_landed_price)
