# Hospitality reports

The [structured report details](hospitality.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Hotel Room Occupancy

Script Report. The reference record is Hotel Room Reservation. Declared inputs include `from_date`, `to_date`.

Both file locations declare the Hotels module and the same lookup name. The Hotels module chooses the row procedure; the second declaration has the same stored fields. The direct return positions are columns / data. [Row procedure](https://github.com/frappe/hospitality/blob/2003ff8db7d7fbc453a9d14da0f971b9186a0b4b/hospitality/hotels/report/hotel_room_occupancy/hotel_room_occupancy.py#L12) [Declaration](https://github.com/frappe/hospitality/blob/2003ff8db7d7fbc453a9d14da0f971b9186a0b4b/hospitality/hotels/report/hotel_room_occupancy/hotel_room_occupancy.json) [Module bindings](procedures/hospitality--hotel-room-occupancy-bindings.json) · [Ordered report procedures](procedures/hospitality--hotel-room-occupancy-1.json)
