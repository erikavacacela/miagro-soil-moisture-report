class SoilMoisture:

    def __init__(self, sample_time, device_id, sensor_type, 
        humidity, potassium, nitrogen, ph, temperature, 
        phosphorous) -> None:
        self.sample_time = sample_time
        self.device_id = device_id
        self.sensor_type = sensor_type
        self.humidity = humidity
        self.potassium = potassium
        self.nitrogen = nitrogen
        self.ph = ph
        self.temperature = temperature
        self.phosphorous = phosphorous
    
    def __str__(self) -> str:
        return f"{self.sample_time} - {self.device_id} - {self.sensor_type}"

    @staticmethod
    def json_to_class(data: any):
        return SoilMoisture(
            sample_time = data.get("sample_time"),
            device_id = data.get("device_id"),
            sensor_type = data.get("device_data").get("sensor_type"),
            humidity = data.get("device_data").get("humidity"),
            potassium = data.get("device_data").get("potassium"),
            nitrogen = data.get("device_data").get("nitrogen"),
            ph = data.get("device_data").get("ph"),
            temperature = data.get("device_data").get("temperature"),
            phosphorous = data.get("device_data").get("phosphorous"),
        )
