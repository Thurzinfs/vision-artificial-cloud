from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DetectionEntity:
    device: str = field(default='')
    timestamp: datetime | None = field(default=None)
    frame_id: int = field(default=0)
    image_bytes: str = field(default='')
