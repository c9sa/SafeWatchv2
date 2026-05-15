from typing import Literal


# Stores each valid incident category and its meaning.
# Used to generate the classifier prompt category guide.
CATEGORY_DESCRIPTIONS = {
    "theft": "stolen items, snatching, shop theft",
    "burglary": "break-ins into homes, shops, or private premises",
    "robbery": "theft involving force, threat, or confrontation",
    "assault": "physical attack or fight involving harm",
    "violent_crime": "serious violence, weapons, major physical harm",
    "vandalism": "property damage, graffiti, destruction",
    "scam_fraud": "scams, cheating, online fraud, impersonation",
    "identity_document_fraud": "NRIC, passport, ID misuse or forgery",
    "harassment_threat": "stalking, harassment, threats, intimidation",
    "sexual_offense": "sexual harassment, molestation, indecent exposure",
    "suspicious_activity": "suspicious behavior without confirmed offence",
    "public_disorder": "fights, shouting, disorderly conduct in public",
    "regulatory_offence": "illegal works, licensing, fines, rule breaches",
    "drug_offence": "drug use, trafficking, possession",
    "traffic_transport_offence": "road incidents, reckless driving, transport offences",
    "other": "unclear, non-incident, or not covered above",
}


# Restricts classifier output to only these category names.
# If the LLM returns a category outside this list, Pydantic validation fails.
CategoryType = Literal[
    "theft",
    "burglary",
    "robbery",
    "assault",
    "violent_crime",
    "vandalism",
    "scam_fraud",
    "identity_document_fraud",
    "harassment_threat",
    "sexual_offense",
    "suspicious_activity",
    "public_disorder",
    "regulatory_offence",
    "drug_offence",
    "traffic_transport_offence",
    "other",
]


# Converts CATEGORY_DESCRIPTIONS into readable prompt text.
# Prevents repeating category guide
CATEGORY_GUIDE = "\n".join(
    f"- {category}: {description}"
    for category, description in CATEGORY_DESCRIPTIONS.items()
)