def determine_price_winner(hostel1, hostel2):
    """
    Determine which hostel offers better value for money
    Considers both price and billing cycle
    """

    # Normalize prices to monthly rates for fair comparison
    def get_monthly_rate(hostel):
        price = float(hostel.pricing)
        if hostel.billing_cycle == "month":
            return price
        elif hostel.billing_cycle == "two_months":
            return price / 2
        elif hostel.billing_cycle == "semester":
            return price / 4
        return price

    monthly1 = get_monthly_rate(hostel1)
    monthly2 = get_monthly_rate(hostel2)

    if monthly1 < monthly2:
        return 1
    elif monthly2 < monthly1:
        return 2
    else:
        return 0


def generate_recommendation(
    hostel1, hostel2, price_winner, rating_winner, amenity_winner
):
    """
    Generate an intelligent recommendation based on comparison factors
    """
    hostel1_name = hostel1.name
    hostel2_name = hostel2.name

    # Score calculation
    hostel1_score = 0
    hostel2_score = 0

    # Price factor (weight: 3)
    if price_winner == 1:
        hostel1_score += 3
    elif price_winner == 2:
        hostel2_score += 3

    # Rating factor (weight: 2)
    if rating_winner == 1:
        hostel1_score += 2
    elif rating_winner == 2:
        hostel2_score += 2

    # Amenities factor (weight: 1)
    if amenity_winner == 1:
        hostel1_score += 1
    elif amenity_winner == 2:
        hostel2_score += 1

    # Availability factor (weight: 1)
    if hostel1.available_vacants > hostel2.available_vacants:
        hostel1_score += 1
    elif hostel2.available_vacants > hostel1.available_vacants:
        hostel2_score += 1

    # Generate recommendation text
    if hostel1_score > hostel2_score:
        winner = hostel1_name
        reasons = []
        if price_winner == 1:
            reasons.append("better value for money")
        if rating_winner == 1:
            reasons.append("higher rating from residents")
        if amenity_winner == 1:
            reasons.append("more amenities")
        if hostel1.available_vacants > hostel2.available_vacants:
            reasons.append("more availability")

        recommendation = (
            f"I recommend {winner}. This hostel offers {', '.join(reasons[:-1])}"
        )
        if len(reasons) > 1:
            recommendation += f" and {reasons[-1]}"
        else:
            recommendation += reasons[0] if reasons else ""
        recommendation += ", making it the better choice overall."

    elif hostel2_score > hostel1_score:
        winner = hostel2_name
        reasons = []
        if price_winner == 2:
            reasons.append("better value for money")
        if rating_winner == 2:
            reasons.append("higher rating from residents")
        if amenity_winner == 2:
            reasons.append("more amenities")
        if hostel2.available_vacants > hostel1.available_vacants:
            reasons.append("more availability")

        recommendation = (
            f"I recommend {winner}. This hostel offers {', '.join(reasons[:-1])}"
        )
        if len(reasons) > 1:
            recommendation += f" and {reasons[-1]}"
        else:
            recommendation += reasons[0] if reasons else ""
        recommendation += ", making it the better choice overall."

    else:
        recommendation = f"Both {hostel1_name} and {hostel2_name} are quite comparable. Your choice might depend on personal preferences like location convenience or specific amenities that matter most to you."

    return recommendation
