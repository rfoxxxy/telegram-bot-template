from abc import ABC, abstractmethod

try:
    from apscheduler.triggers.base import BaseTrigger
except ImportError:
    pass


class BaseSchedulerTask(ABC):
    name: str
    trigger: "BaseTrigger"
    misfire_grace_time: int
    force_reschedule: bool

    def __repr__(self) -> str:
        return f"<SchedulerTask name={self.name} at {hex(id(self))}>"  # yapf: disable

    @abstractmethod
    async def run_task(self):
        ...
