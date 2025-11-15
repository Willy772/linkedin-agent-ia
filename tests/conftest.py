import json
import pytest


@pytest.fixture
def sample_candidates(tmp_path):
    data = [
        {"full_name": "Alice Dupont", "school": "ESIGELEC", "title": "Ingénieure", "company": "InnovTech", "location": "Ile-de-France"},
        {"full_name": "Benoît Leroy", "school": "INSA", "title": "Data Scientist", "company": "DataCorp", "location": "Lyon"},
    ]
    dataset_path = tmp_path / 'candidates.json'
    dataset_path.write_text(json.dumps(data), encoding='utf-8')
    return data, dataset_path
