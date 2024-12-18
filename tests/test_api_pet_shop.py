import pytest
import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# Load test data from JSON file
with open("test_data.json", "r") as file:
    test_data = json.load(file)

@pytest.mark.serial
def test_verify_user_creation():
    """
    Verify that the API allows creating a user and fetching user details.
    """
    # Extract user data from JSON
    user_creation_data = test_data["petStore"]["userCreationData"]
    username = user_creation_data["username"]

    # Step 1: Create a user using POST request
    create_response = requests.post(f"{BASE_URL}/user", json=user_creation_data)

    # Validate the response status
    assert create_response.ok, f"Expected status 200, but got {create_response.status_code}"
    assert create_response.status_code == 200, f"Failed to create user. Response: {create_response.text}"

    # Step 2: Fetch the created user details using GET request
    get_user_response = requests.get(f"{BASE_URL}/user/{username}")
    assert get_user_response.ok, f"Failed to fetch user. Status: {get_user_response.status_code}"
    assert get_user_response.status_code == 200, f"Expected 200, but got {get_user_response.status_code}"

    # Parse the user details response
    user_details = get_user_response.json()

    # Step 3: Validate the user details
    assert user_details["username"] == user_creation_data["username"], \
        f"Expected username '{user_creation_data['username']}', but got '{user_details['username']}'"
    assert user_details["firstName"] == user_creation_data["firstName"], \
        f"Expected firstName '{user_creation_data['firstName']}', but got '{user_details['firstName']}'"
    assert user_details["lastName"] == user_creation_data["lastName"], \
        f"Expected lastName '{user_creation_data['lastName']}', but got '{user_details['lastName']}'"

    print("User created and validated successfully.")

def test_verify_user_login():
    """
    Verify that the API allows login as a User.
    """
    # Extract user data from JSON
    user_creation_data = test_data["petStore"]["userCreationData"]
    username = user_creation_data["username"]
    password = user_creation_data["password"]

    # Step 1: Perform login request using GET with query parameters
    login_response = requests.get(f"{BASE_URL}/user/login", params={
        "username": username,
        "password": password
    })

    # Step 2: Validate the response status
    assert login_response.ok, f"Expected response status 200, but got {login_response.status_code}"
    assert login_response.status_code == 200, f"Failed to log in. Response: {login_response.text}"

    # Step 3: Parse and log the response body
    login_response_body = login_response.json()
    print("Login Response Body:", login_response_body)

    # Step 4: Validate the response contains the expected values
    assert "logged in" in login_response_body["message"], \
        f"Expected 'logged in' in the message, but got '{login_response_body['message']}'"

    print("Login successful: User is logged in.")

def test_verify_user_logout():
    """
    Verify that the API allows logging out the User.
    """
    # Step 1: Perform logout request
    logout_response = requests.get(f"{BASE_URL}/user/logout", headers={
        "accept": "application/json"
    })

    # Step 2: Validate the response status
    assert logout_response.ok, f"Expected response status 200, but got {logout_response.status_code}"
    assert logout_response.status_code == 200, f"Failed to log out. Response: {logout_response.text}"

    # Step 3: Parse and log the response body
    logout_response_body = logout_response.json()
    print("Logout Response Body:", logout_response_body)

    # Step 4: Validate the response body contains the expected data
    assert logout_response_body["code"] == 200, \
        f"Expected response code 200, but got {logout_response_body['code']}"
    assert logout_response_body["message"] == "ok", \
        f"Expected message 'ok', but got '{logout_response_body['message']}'"

    print("Logout successful.")

def test_verify_create_user_list():
    """
    Verify that the API allows creating a list of users.
    """
    # Extract user list data from JSON
    user_list = test_data["petStore"]["userList"]

    # Step 1: Send a POST request to create users with the list
    response = requests.post(f"{BASE_URL}/user/createWithList", json=user_list)

    # Step 2: Validate the response status
    assert response.ok, f"Expected response status 200, but got {response.status_code}"
    assert response.status_code == 200, f"Failed to create user list. Response: {response.text}"

    # Step 3: Parse and log the response body
    response_body = response.json()
    print("Response Body:", response_body)

    # Step 4: Validate the response body contains the expected data
    assert response_body["code"] == 200, \
        f"Expected response code 200, but got {response_body['code']}"
    assert response_body["message"] == "ok", \
        f"Expected message 'ok', but got '{response_body['message']}'"

    print("User list created successfully.")

def test_verify_add_new_pet():
    """
    Verify that the API allows adding a new pet.
    """
    # Extract pet data from JSON
    pet_data = test_data["petStore"]["petData"]

    # Step 1: Send a POST request to add a new pet
    response = requests.post(f"{BASE_URL}/pet", json=pet_data)

    # Step 2: Assert the response is OK
    assert response.ok, f"Expected response status 200, but got {response.status_code}"
    assert response.status_code == 200, f"Failed to add new pet. Response: {response.text}"

    # Step 3: Parse the response body
    response_body = response.json()
    print("Response Body:", response_body)

    # Step 4: Validate the response body matches the input data
    assert response_body["id"] == pet_data["id"], \
        f"Expected pet ID {pet_data['id']}, but got {response_body['id']}"
    assert response_body["name"] == pet_data["name"], \
        f"Expected pet name '{pet_data['name']}', but got '{response_body['name']}'"
    assert response_body["status"] == pet_data["status"], \
        f"Expected pet status '{pet_data['status']}', but got '{response_body['status']}'"

    print("Pet added successfully.")

def test_verify_update_pet():
    """
    Verify that the API allows updating a pet's name and status.
    """
    # Extract pet data and update data from JSON
    pet_id = test_data["petStore"]["petData"]["id"]
    update_data = {
        **test_data["petStore"]["petData"],  # Start with the existing pet data
        "name": test_data["petStore"]["updatePetData"]["name"],  # Update name
        "status": test_data["petStore"]["updatePetData"]["status"]  # Update status
    }

    # Step 1: Send a PUT request to update the pet
    response = requests.put(f"{BASE_URL}/pet", json=update_data)

    # Step 2: Assert the response is OK
    assert response.ok, f"Expected response status 200, but got {response.status_code}"
    assert response.status_code == 200, f"Failed to update pet. Response: {response.text}"

    # Step 3: Parse the response body
    response_body = response.json()
    print("Response Body:", response_body)

    # Step 4: Validate the updated data in the response body
    assert response_body["id"] == pet_id, \
        f"Expected pet ID {pet_id}, but got {response_body['id']}"
    assert response_body["name"] == update_data["name"], \
        f"Expected pet name '{update_data['name']}', but got '{response_body['name']}'"
    assert response_body["status"] == update_data["status"], \
        f"Expected pet status '{update_data['status']}', but got '{response_body['status']}'"

    print("Pet updated successfully.")

def test_verify_update_pet_image():
    """
    Verify that the API allows updating a pet's image while preserving other fields.
    """
    # Extract the pet ID from test data
    pet_id = test_data["petStore"]["petData"]["id"]

    # Step 1: Fetch the existing pet data
    get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    assert get_response.ok, f"Failed to fetch pet. Status: {get_response.status_code}"
    assert get_response.status_code == 200, f"Expected 200, but got {get_response.status_code}"

    existing_pet_data = get_response.json()
    print("Existing Pet Data:", existing_pet_data)

    # Step 2: Update only the photoUrls while preserving other fields
    updated_data = {
        **existing_pet_data,  # Preserve all existing fields
        "photoUrls": ["https://example.com/updated-pet-image.jpg"]  # Update image URL
    }

    # Step 3: Send a PUT request to update the pet
    put_response = requests.put(f"{BASE_URL}/pet", json=updated_data)
    assert put_response.ok, f"Failed to update pet. Status: {put_response.status_code}"
    assert put_response.status_code == 200, f"Expected 200, but got {put_response.status_code}"

    # Step 4: Parse the response body
    response_body = put_response.json()
    print("Updated Pet Response Body:", response_body)

    # Step 5: Verify the pet data is updated correctly
    assert response_body["id"] == pet_id, \
        f"Expected pet ID {pet_id}, but got {response_body['id']}"
    assert "https://example.com/updated-pet-image.jpg" in response_body["photoUrls"], \
        f"Expected photo URL to contain 'https://example.com/updated-pet-image.jpg', but got {response_body['photoUrls']}"
    assert response_body["name"] == existing_pet_data["name"], \
        f"Expected pet name '{existing_pet_data['name']}', but got '{response_body['name']}'"
    assert response_body["status"] == existing_pet_data["status"], \
        f"Expected pet status '{existing_pet_data['status']}', but got '{response_body['status']}'"

    print("Pet image updated successfully.")

def test_verify_delete_pet():
    """
    Verify that the API allows deleting a pet.
    """
    # Extract the pet ID from test data
    pet_id = test_data["petStore"]["petData"]["id"]

    # Step 1: Send a DELETE request to delete the pet
    delete_response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

    # Step 2: Assert the response is OK
    assert delete_response.ok, f"Expected response status 200, but got {delete_response.status_code}"
    assert delete_response.status_code == 200, f"Failed to delete pet. Response: {delete_response.text}"

    # Step 3: Parse the response body
    delete_response_body = delete_response.json()
    print("Delete Response Body:", delete_response_body)

    # Step 4: Verify the response confirms deletion
    assert delete_response_body["code"] == 200, \
        f"Expected response code 200, but got {delete_response_body['code']}"
    assert delete_response_body["message"] == str(pet_id), \
        f"Expected message '{pet_id}', but got '{delete_response_body['message']}'"

    print("Pet deleted successfully.")

def test_verify_pet_not_found():
    """
    Verify that the deleted pet is no longer retrievable.
    """
    # Extract the pet ID from test data
    pet_id = test_data["petStore"]["petData"]["id"]

    # Step 1: Send a GET request to retrieve the deleted pet
    get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    # Step 2: Assert the response returns a 404 status
    assert get_response.status_code == 404, \
        f"Expected response status 404, but got {get_response.status_code}"

    # Step 3: Parse the response body
    get_response_body = get_response.json()
    print("Get Response Body:", get_response_body)

    # Step 4: Verify the response indicates the pet is not found
    assert get_response_body["code"] == 1, \
        f"Expected response code 1, but got {get_response_body['code']}"
    assert get_response_body["type"] == "error", \
        f"Expected type 'error', but got {get_response_body['type']}"
    assert get_response_body["message"] == "Pet not found", \
        f"Expected message 'Pet not found', but got '{get_response_body['message']}'"

    print("Pet not found as expected.")
