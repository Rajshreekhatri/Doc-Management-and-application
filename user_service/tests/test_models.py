from app.models import User

def test_model_instantiation():
    model = User(name='Test Name')
    assert model.name == 'Test Name'
