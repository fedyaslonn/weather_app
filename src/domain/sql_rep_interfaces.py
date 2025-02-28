from typing import Protocol, List, TypeVar

T = TypeVar("T")

class AbstractRepository(Protocol[T]):
    async def add_one(self, data: dict) -> T:
        ...

    async def find_all(self) -> List[T]:
        ...
