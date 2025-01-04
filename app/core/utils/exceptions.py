class NoMatchingConditionsError(Exception):
    def __init__(self, symptoms: str, suggestions: list = None):
        self.symptoms = symptoms
        self.suggestions = suggestions or [
            "Try describing your symptoms in more detail",
            "Include how long you've been experiencing these symptoms",
            "Mention how these symptoms affect your daily life",
            "Include any triggers or patterns you've noticed",
            "Describe any changes in sleep, appetite, or energy levels"
        ]
        message = "Unable to identify matching conditions. Here are some suggestions to help us better understand your symptoms:"
        super().__init__(message) 