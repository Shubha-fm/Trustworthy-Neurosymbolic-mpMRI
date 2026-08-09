------------------------------ MODULE CertFusion ------------------------------
EXTENDS Naturals, FiniteSets

CONSTANTS InputIds, PropertyIds, Labels

VARIABLES phase, inputId, propertyId, boundsReady, solverResult,
          certificate, counterexample, predSet, outputStatus

vars == <<phase, inputId, propertyId, boundsReady, solverResult,
          certificate, counterexample, predSet, outputStatus>>

Phases == {"Init","Bounds","Solve","AssignStatus","Released"}
SolverResults == {"NONE","UNSAT","SAT","TIMEOUT"}
Statuses == {"UNREL","CERT","UNCERT","CEX"}

Init ==
  /\ phase = "Init"
  /\ inputId = "NULL"
  /\ propertyId = "NULL"
  /\ boundsReady = FALSE
  /\ solverResult = "NONE"
  /\ certificate = FALSE
  /\ counterexample = FALSE
  /\ predSet = {}
  /\ outputStatus = "UNREL"

Prepare(i,p) ==
  /\ phase = "Init"
  /\ i \in InputIds
  /\ p \in PropertyIds
  /\ phase' = "Bounds"
  /\ inputId' = i
  /\ propertyId' = p
  /\ UNCHANGED <<boundsReady,solverResult,certificate,counterexample,predSet,outputStatus>>

MakeBounds ==
  /\ phase = "Bounds"
  /\ phase' = "Solve"
  /\ boundsReady' = TRUE
  /\ UNCHANGED <<inputId,propertyId,solverResult,certificate,counterexample,predSet,outputStatus>>

Solve(r) ==
  /\ phase = "Solve"
  /\ boundsReady
  /\ r \in {"UNSAT","SAT","TIMEOUT"}
  /\ phase' = "AssignStatus"
  /\ solverResult' = r
  /\ counterexample' = (r = "SAT")
  /\ UNCHANGED <<inputId,propertyId,boundsReady,certificate,predSet,outputStatus>>

AssignCertified ==
  /\ phase = "AssignStatus"
  /\ solverResult = "UNSAT"
  /\ predSet # {}
  /\ phase' = "Released"
  /\ certificate' = TRUE
  /\ outputStatus' = "CERT"
  /\ UNCHANGED <<inputId,propertyId,boundsReady,solverResult,counterexample,predSet>>

AssignUnverified ==
  /\ phase = "AssignStatus"
  /\ solverResult \in {"SAT","TIMEOUT"}
  /\ predSet # {}
  /\ phase' = "Released"
  /\ certificate' = FALSE
  /\ outputStatus' = IF solverResult = "SAT" THEN "CEX" ELSE "UNCERT"
  /\ UNCHANGED <<inputId,propertyId,boundsReady,solverResult,counterexample,predSet>>

SetPrediction(S) ==
  /\ phase \in {"Solve","AssignStatus"}
  /\ S \subseteq Labels
  /\ S # {}
  /\ predSet' = S
  /\ UNCHANGED <<phase,inputId,propertyId,boundsReady,solverResult,certificate,counterexample,outputStatus>>

Next ==
  \/ \E i \in InputIds, p \in PropertyIds: Prepare(i,p)
  \/ MakeBounds
  \/ \E r \in {"UNSAT","SAT","TIMEOUT"}: Solve(r)
  \/ \E S \in SUBSET Labels: SetPrediction(S)
  \/ AssignCertified
  \/ AssignUnverified

TypeOK ==
  /\ phase \in Phases
  /\ solverResult \in SolverResults
  /\ outputStatus \in Statuses
  /\ certificate \in BOOLEAN
  /\ counterexample \in BOOLEAN
  /\ predSet \subseteq Labels

NoUnsafeRelease ==
  outputStatus = "CERT" => (solverResult = "UNSAT" /\ certificate)

TimeoutNotCertified ==
  solverResult = "TIMEOUT" => ~certificate

CounterexampleNotCertified ==
  solverResult = "SAT" => (~certificate /\ outputStatus # "CERT")

ConformalBeforeRelease ==
  outputStatus # "UNREL" => predSet # {}

TraceableRelease ==
  outputStatus # "UNREL" =>
    (inputId # "NULL" /\ propertyId # "NULL" /\ solverResult # "NONE")

Spec == Init /\ [][Next]_vars
=============================================================================
