import requests
import json

def test_sort_list():
    response = requests.post("http://data-structures:8000/api/list/sort", 
                           json={"items": [3, 1, 4, 1, 5]})
    assert response.json() == [1, 1, 3, 4, 5]

def test_remove_duplicates():
    response = requests.post("http://data-structures:8000/api/list/remove-duplicates",
                           json={"items": [1, 2, 2, 3, 3, 4]})
    assert response.json() == [1, 2, 3, 4]

def test_merge_dicts():
    response = requests.post("http://data-structures:8000/api/dict/merge",
                           json={"dict1": {"a": 1}, "dict2": {"b": 2}})
    assert response.json() == {"a": 1, "b": 2}

if __name__ == "__main__":
    print("Running data structures tests...")
    test_sort_list()
    test_remove_duplicates()
    test_merge_dicts()
    print("Data structures tests passed!")
