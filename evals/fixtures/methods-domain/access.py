def has_access(member, now):
    return now < member["paid_through"]
