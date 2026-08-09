import torch

def implication(a, b):
    # Product-logic-style differentiable implication surrogate.
    return torch.clamp(1.0 - a + a*b, 0.0, 1.0)

def prior_satisfaction(predicates, class_probs):
    """
    Soft computational priors corresponding to manuscript phi_1 ... phi_7.
    Predicate tensors must be supplied by the caller and should be in [0,1].
    Class indices:
      0 background, 1 NCR/NET, 2 oedema, 3 enhancing tumour, 4 enhancement-dominant.
    """
    bg = class_probs[:,0]
    oedema = class_probs[:,2]
    et = class_probs[:,3]
    edom = class_probs[:,4]

    enh = predicates["enhancement"]
    flair = predicates["flair_abnormality"]
    strong = predicates["strong_enhancement"]
    core = predicates["core_abnormality"]
    peripheral = predicates["peripheral_flair"]
    diffuse = predicates["diffuse_flair"]
    ring = predicates["ring_enhancement"]
    low_t1 = predicates["low_t1_core"]

    vals = [
        implication(enh*flair, 1-bg),
        implication((1-flair)*(1-enh), bg),
        implication(ring*low_t1, edom),
        implication(peripheral*(1-strong), oedema),
        implication(core, 1-bg),
        implication(strong, et),
        implication(diffuse, 1-bg),
    ]
    return torch.stack(vals, dim=0).mean()
