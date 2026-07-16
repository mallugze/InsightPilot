class DatasetValidationError(Exception):
    """
    Custom exception raised when a dataset fails structural, encoding, 
    delimiter, or validation rules during ingestion.
    """
    def __init__(self, reason: str, details: list):
        super().__init__(reason)
        self.reason = reason
        self.details = details
