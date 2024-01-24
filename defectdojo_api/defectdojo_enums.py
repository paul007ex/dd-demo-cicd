from enum import Enum

class DefectDojoEngagementStatus(Enum):
    NotStarted = "Not Started"
    Cancelled = "Cancelled"
    Completed = "Completed"
    InProgress = "In Progress"
    OnHold = "On Hold"
    WaitingForResource = "Waiting for Resource"

class DefectDojoEngagementOrder(Enum):
    NameAscending = "name"
    NameDescending = "-name"
    VersionAscending = "version"
    VersionDescending = "-version"
    TargetStartAscending = "target_start"
    TargetStartDescending = "-target_start"
    TargetEndAscending = "target_end"
    TargetEndDescending = "-target_end"
    StatusAscending = "status"
    StatusDescending = "-status"
    LeadAscending = "lead"
    LeadDescending = "-lead"
    CreatedAscending = "created"
    CreatedDescending = "-created"
    UpdatedAscending = "updated"
    UpdatedDescending = "-updated"

class DefectDojoEngagementType(Enum):
    Interactive = "Interactive"
    CICD = "CI/CD"