class ClimateIncident:

    def __init__(self, incident_type, severity, snapshot):
        self.incident_type = incident_type
        self.severity = severity
        self.snapshot = snapshot
        self.causal_chain = []
        self.confidence = 0.0
