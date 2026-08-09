from dataclasses import dataclass, field

@dataclass
class RepairItem:
    subject_id: str
    property_id: str
    description: str

@dataclass
class RepairBuffer:
    items: list[RepairItem] = field(default_factory=list)

    def add(self, subject_id, property_id, description):
        self.items.append(RepairItem(subject_id, property_id, description))
