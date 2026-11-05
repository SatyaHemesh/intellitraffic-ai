# ml/analytics/density_calculator.py
from datetime import datetime

class DensityCalculator:
    def __init__(self, low_threshold=10, medium_threshold=25):
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold

    def calculate_density(self, vehicle_count: int) -> str:
        """
        Calculates traffic density state based on the current vehicle count.
        """
        if vehicle_count < self.low_threshold:
            return "Low"
        elif vehicle_count < self.medium_threshold:
            return "Medium"
        else:
            return "High"

    def get_stats(self, tracked_objects: list) -> dict:
        """
        Generates congestion statistics for a given frame.
        """
        vehicle_count = len(tracked_objects)
        density_level = self.calculate_density(vehicle_count)
        
        return {
            "total_vehicles": vehicle_count,
            "density_level": density_level,
            "timestamp": datetime.utcnow().isoformat()
        }