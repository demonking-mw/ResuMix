from typing import Dict, Any


def _analyze_resume(obj: Any) -> tuple[int, int, int]:
    """
    Recursively analyze resume to count items and track tweak status.
    Returns (item_count, total_cate_scores, tweaked_cate_scores)
    """
    item_count = 0
    total_cate_scores = 0
    tweaked_cate_scores = 0

    if isinstance(obj, dict):
        # Check if this dict has aux_info with type:'items'
        if "aux_info" in obj and isinstance(obj["aux_info"], dict):
            if obj["aux_info"].get("type") == "items":
                item_count += 1

        # Check if this dict has cate_scores
        if "cate_scores" in obj and isinstance(obj["cate_scores"], dict):
            total_cate_scores += 1
            cate_scores = obj["cate_scores"]
            weight = cate_scores.get("weight", 1.0)
            bias = cate_scores.get("bias", 0.0)
            if weight != 1.0 or bias != 0.0:
                tweaked_cate_scores += 1

        # Recursively check all values in the dictionary
        for value in obj.values():
            sub_items, sub_total, sub_tweaked = _analyze_resume(value)
            item_count += sub_items
            total_cate_scores += sub_total
            tweaked_cate_scores += sub_tweaked

    elif isinstance(obj, list):
        # Recursively check all items in the list
        for item in obj:
            sub_items, sub_total, sub_tweaked = _analyze_resume(item)
            item_count += sub_items
            total_cate_scores += sub_total
            tweaked_cate_scores += sub_tweaked

    return item_count, total_cate_scores, tweaked_cate_scores


def parse_user_info(user_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse user information from a dictionary and extract relevant fields.
    Status: r for red, bad; o for orange, warning, g for green, good.
    Args:
        user_info: Dictionary containing user information after vec_rip

    Returns:
        A new dictionary with extracted and interpolated fields
    "item_count": int;
    "resume_state": r(bad), o(ok but sketchy), g(good);
    "tweak_status": r(bad), o(ok but sketchy), g(good);
    "generate_status": r(bad), o(ok but sketchy), y(good but imperfect) g(good);
    """
    item_count, total_cate_scores, tweaked_cate_scores = _analyze_resume(user_info)

    if item_count < 4:
        resume_state = "r"  # way too little
    elif item_count < 8:
        resume_state = "o"  # not enough
    else:
        resume_state = "g"  # good

    # Only check tweak status when state is orange or green
    tweak_status = "r"  # default to not tweaked
    if resume_state in ["o", "g"]:
        if total_cate_scores == 0 or tweaked_cate_scores == 0:
            tweak_status = "r"  # not tweaked
        elif tweaked_cate_scores > total_cate_scores / 2:
            tweak_status = "g"  # thoroughly tweaked (more than half)
        else:
            tweak_status = "o"  # tweaked (some but less than half)
    generate_resume = "r"
    if resume_state == "g" and tweak_status == "g":
        generate_resume = "g"
    elif resume_state == "g" and tweak_status == "o":
        generate_resume = "y"  # yellow for mostly good
    elif resume_state == "o" and tweak_status == "g":
        generate_resume = "y"
    elif resume_state == "o" and tweak_status == "o":
        generate_resume = "o"
    elif resume_state == "g":
        generate_resume = "y"
    
    parsed_info = {
        "item_count": item_count,
        "resume_state": resume_state,
        "tweak_status": tweak_status,
        "generate_status": generate_resume
    }
    return parsed_info
