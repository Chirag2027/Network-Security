# After Data Ingestion Component, Output will be there. 
# Code related to Output is here
# Output of Data Ingestion Component => Data Ingestion Artifact

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
