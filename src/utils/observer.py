from typing import List, Any, Callable
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: Any):
        """Update the observer with new data"""
        pass

class Observable:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        """Add an observer to the list"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Remove an observer from the list"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type: str, data: Any):
        """Notify all observers of a change"""
        for observer in self._observers:
            observer.update(event_type, data)

class EventEmitter:
    def __init__(self):
        self._handlers: dict[str, List[Callable]] = {}

    def on(self, event_type: str, handler: Callable):
        """Register an event handler"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def off(self, event_type: str, handler: Callable):
        """Remove an event handler"""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]

    def emit(self, event_type: str, *args, **kwargs):
        """Emit an event to all registered handlers"""
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(*args, **kwargs) 