from app.models import Document

def test_model_instantiation():
    model = Document(name='Test Name')
    assert model.name == 'Test Name'
