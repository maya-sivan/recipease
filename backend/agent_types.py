from typing import List, TypedDict, get_type_hints, Dict, Any


class HouseFeatures(TypedDict):
   is_for_sale: bool 
   price: float | None # If for sale, price is the price of the house, otherwise rent per month
   square_feet: int | None
   num_bedrooms: int | None
   num_bathrooms: int | None
   year_built: int | None
   washer_in_unit: bool | None
   dryer_in_unit: bool | None
   pet_friendly: bool | None
   location_score: int | None # 0-100, 100 is the best
   crime_rate: float | None
   walk_score: int | None
   transit_score: int | None
   bike_score: int | None
   has_elevator: bool | None
   has_gym: bool | None
   has_pool: bool | None
   has_parking: bool | None
   has_air_conditioning: bool | None
   has_heating: bool | None
   has_dishwasher: bool | None
   has_refrigerator: bool | None
   has_stove: bool | None
   has_oven: bool | None
   has_storage: bool | None


FEATURES = list(get_type_hints(HouseFeatures).keys())

class HouseListing:
   deal_url: str
   image_urls: List[str] | None
   address: str | None
   features: HouseFeatures



class LLMResponse(TypedDict):
   extra_features: dict[str, Any]
   feature_weights: dict[str, float]

class State(LLMResponse):
   query: str
   urls: List[str]
   raw_contents: List[str]
   top_deals: List[HouseListing]
   previous_top_deal: HouseListing | None
