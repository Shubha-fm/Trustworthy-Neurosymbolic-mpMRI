from dataclasses import dataclass

CLASSES = [
    "background_dominant",
    "ncr_net",
    "oedema",
    "enhancing_tumour",
    "enhancement_dominant",
]

@dataclass(frozen=True)
class LabelThresholds:
    V_min_ml: float = 1.0
    r_ET: float = 0.35
    rho_ET: float = 1.25
    eps: float = 1e-6

def derive_label(v_et: float, v_ncr: float, v_ed: float,
                 t: LabelThresholds = LabelThresholds()) -> str:
    """Construct the manuscript's experimental five-class label."""
    if min(v_et, v_ncr, v_ed) < 0:
        raise ValueError("Compartment volumes must be non-negative.")

    lesion = v_et + v_ncr + v_ed
    if lesion < t.V_min_ml:
        return "background_dominant"

    r_et = v_et / (lesion + t.eps)
    rho_et = v_et / (v_ncr + t.eps)

    if r_et >= t.r_ET or rho_et >= t.rho_ET:
        return "enhancement_dominant"

    # Largest remaining compartment; ties ET > NCR/NET > oedema.
    candidates = [
        ("enhancing_tumour", v_et, 2),
        ("ncr_net", v_ncr, 1),
        ("oedema", v_ed, 0),
    ]
    return max(candidates, key=lambda x: (x[1], x[2]))[0]
