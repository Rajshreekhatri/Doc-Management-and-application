from app.models import Ingestion

def test_model_instantiation():
    model = Ingestion(name='Test Name')
    assert model.name == 'Test Name'
