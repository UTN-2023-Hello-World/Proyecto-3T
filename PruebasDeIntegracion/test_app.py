import pytest
from app import app as flask_app
from product import Product
import database as dbase

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'APP DE PRODUCTOS' in response.data

def test_add_product(client):
    response = client.post('/products', data=dict(
        name='Test Product',
        price='10',
        quantity='5'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Product' in response.data

def test_edit_product(client):
    # First, add a product to edit
    client.post('/products', data=dict(
        name='Product to Edit',
        price='20',
        quantity='10'
    ), follow_redirects=True)
    
    # Edit the product
    response = client.post('/edit/Product to Edit', data=dict(
        name='Edited Product',
        price='25',
        quantity='15'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Edited Product' in response.data
    assert b'25' in response.data
    assert b'15' in response.data

def test_delete_product(client):
    # First, add a product to delete
    client.post('/products', data=dict(
        name='Product to Delete',
        price='30',
        quantity='20'
    ), follow_redirects=True)
    
    # Delete the product
    response = client.get('/delete/Product to Delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Product to Delete' not in response.data

def test_add_product_missing_fields(client):
    response = client.post('/products', data=dict(
        name='Incomplete Product'
    ), follow_redirects=True)
    assert response.status_code == 400
    assert b'Bad Request' in response.data

def test_edit_product_missing_fields(client):
    # First, add a product to edit
    client.post('/products', data=dict(
        name='Product to Edit Missing Fields',
        price='50',
        quantity='25'
    ), follow_redirects=True)
    
    # Attempt to edit the product with missing fields
    response = client.post('/edit/Product to Edit Missing Fields', data=dict(
        name='Edited Product Missing Fields'
    ), follow_redirects=True)
    assert response.status_code == 400
    assert b'Bad Request' in response.data
  
