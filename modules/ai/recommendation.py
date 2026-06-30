def get_recommendation(final_score):
    """
    Returns recommendation based on final AI match score.
    """
    if final_score >= 80:
        return "Highly Suitable"
    elif final_score >= 60:
        return "Suitable"
    elif final_score >= 40:
        return "Needs Review"
    else:
        return "Not Suitable"