import pytest
from faker import Faker
import copy
import json

from ..models import Owner, Farm

fake = Faker()

OWNER_DATA = {
    "name": fake.name(),
    "document": "84575187046",
    "document_type": "CPF",
    "creation_date": "2020-06-01 20:33:32.872527",
    "last_modification_date": "2021-06-01 18:21:02.872527",
    "is_active": True

}

FARM_DATA = {
    "name": fake.company(),
    "area": 0.0002587,
    "creation_date": "2020-06-01 20:33:32.872527",
    "last_modification_date": "2021-06-01 18:21:02.872527",
    "is_active": True,
    "municipality": "Rio de Janeiro",
    "owner_id": 1,
    "state_short_form": "RJ",
    "geometry": "SRID=4326;POLYGON ((-37.5238037109375 -10.93984346235492, -37.48260498046874 -11.02073244690711, -37.43728637695312 -10.94658505651706, -37.5238037109375 -10.93984346235492))",
    "centroid": "SRID=4326;POINT (-37.48123168945312 -10.9690536552597)"
}



@pytest.mark.django_db
@pytest.fixture(autouse=True)
def setup_owner_and_farm():
    owner = Owner()
    owner.name = OWNER_DATA["name"]
    owner.document = OWNER_DATA["document"]
    owner.document_type = OWNER_DATA["document_type"]
    owner.creation_date = OWNER_DATA["creation_date"]
    owner.last_modification_date = OWNER_DATA["last_modification_date"]
    owner.is_active = OWNER_DATA["is_active"]
    owner.save()

    farm = Farm()
    farm.name = FARM_DATA["name"]
    farm.area = FARM_DATA["area"]
    farm.creation_date = FARM_DATA["creation_date"]
    farm.last_modification_date = FARM_DATA["last_modification_date"]
    farm.is_active = FARM_DATA["is_active"]
    farm.municipality = FARM_DATA["municipality"]
    farm.owner = Owner.objects.get(id=owner.id)
    farm.state_short_form = FARM_DATA["state_short_form"]
    farm.geometry = FARM_DATA["geometry"]
    farm.centroid = FARM_DATA["centroid"]
    farm.save()

    return {"farm": farm, "owner": owner}


@pytest.mark.django_db
def test_get_farms(api_client):
    response = api_client.get('/api/v1/farms')
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_farms_with_valid_data_should_return_201(api_client):
    farm_data = copy.copy(FARM_DATA)
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_post_farms_with_not_registered_owner_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["owner_id"] = 1123
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["owner_id"][0]  == "Owner does not exist!"
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_without_owner_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    del farm_data["owner_id"]
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["owner_id"][0]  == "This field is required."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_invalid_owner_id_datatype_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["owner_id"] = "string"
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["owner_id"][0]  == "A valid integer is required."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_invalid_municipality_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["municipality"] = "F"
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["municipality"][0]  == "Invalid municipality."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_without_municipality_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    del farm_data["municipality"]
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["municipality"][0]  == "This field is required."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_municipality_wrong_datatype_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["municipality"] = 123
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["municipality"][0]  == "Invalid municipality."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_invalid_state_datatype_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["state_short_form"] = 12
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["state_short_form"][0]  == f"Invalid state. State must be a string of 2 letters. E.g. SP. And not {farm_data['state_short_form']}"
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_more_than_2_char_state_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["state_short_form"] = "ARE"
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["state_short_form"][0]  == "Ensure this field has no more than 2 characters."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_without_state_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    del farm_data["state_short_form"]
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["state_short_form"][0]  == "This field is required."
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_invalid_name_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["name"] = "p"
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["name"][0]  == f"Invalid Farm name. Farm name must be a string of 2 or more letters. E.g. My Farm. And not {farm_data['name']}"
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_with_invalid_name_datatype_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    farm_data["name"] = "123"
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["name"][0]  == f"Invalid Farm name. Farm name must be a string of 2 or more letters. E.g. My Farm. And not {farm_data['name']}"
    assert response.status_text == "Bad Request"

@pytest.mark.django_db
def test_post_farms_without_name_should_return_400(api_client):
    farm_data = copy.copy(FARM_DATA)
    del farm_data["name"]
    response = api_client.post('/api/v1/farms', data=farm_data)
    assert response.status_code == 400
    assert json.loads(response.content)["name"][0]  == "This field is required."
    assert response.status_text == "Bad Request"