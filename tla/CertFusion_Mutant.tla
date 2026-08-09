-------------------------- MODULE CertFusion_Mutant --------------------------
EXTENDS CertFusion

MutantAssignCertified ==
  /\ phase = "AssignStatus"
  /\ solverResult \in {"UNSAT","SAT"}
  /\ predSet # {}
  /\ phase' = "Released"
  /\ certificate' = TRUE
  /\ outputStatus' = "CERT"
  /\ UNCHANGED <<inputId,propertyId,boundsReady,solverResult,counterexample,predSet>>

MutantNext ==
  \/ \E i \in InputIds, p \in PropertyIds: Prepare(i,p)
  \/ MakeBounds
  \/ \E r \in {"UNSAT","SAT","TIMEOUT"}: Solve(r)
  \/ \E S \in SUBSET Labels: SetPrediction(S)
  \/ MutantAssignCertified
  \/ AssignUnverified

MutantSpec == Init /\ [][MutantNext]_vars
=============================================================================
