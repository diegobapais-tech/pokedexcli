from pokedexcli.pokecache import PokeCache

import time

def test_add_and_get():
    cache = PokeCache()
    testing_url = "url_test"
    testing_response = "test_response"
    cache.add(testing_url, testing_response)
    
    assert cache.get(testing_url) == testing_response 

def test_get_nonexistent():
    cache = PokeCache()
    url = "non_existent_url"

    assert cache.get(url) is None

def test_expiration():
    cache_persistance_time = 1
    testing_url = "url_test"
    testing_response = "test_response"

    cache = PokeCache(save_time=cache_persistance_time)
    
    cache.add(testing_url, testing_response)
    time.sleep(cache_persistance_time)
    
    assert cache.get(testing_url) is None


def test_refresh_on_get():
    cache_persistance_time = 1
    testing_url = "url_test"
    testing_response = "test_response"

    cache = PokeCache(save_time=cache_persistance_time)
    
    cache.add(testing_url, testing_response)
    time.sleep(0.5)
    _ = cache.get(testing_url)
    time.sleep(0.5)
    
    assert cache.get(testing_url) == testing_response



