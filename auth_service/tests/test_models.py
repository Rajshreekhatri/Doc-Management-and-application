from app.models import Auth

def test_model_instantiation():
    model = Auth(name='Test Name')
    assert model.name == 'Test Name'
