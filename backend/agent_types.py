from typing import List, TypedDict


class CarData(TypedDict):
   price: float | None
   mileage: int | None
   year: int | None
   vin: str | None
   link: str




class State(TypedDict):
   query: str
   urls: List[str]
   raw_contents: List[str]
   car_data: List[CarData]
   previous_top_deal: CarData