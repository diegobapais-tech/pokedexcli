from datetime import datetime, timedelta
from pokedexcli.cli_color_print import warning_command_output

default_save_time = 15

class PokeCache():
    def __init__(self, save_time=default_save_time):
        self.cache = {}
        self.save_time = save_time
    
    def add(self, url, response):
        expiration_time = datetime.now() + timedelta(seconds=self.save_time)
        self.cache[url] = (response, expiration_time)
        self._reap_loop()

    def get(self, url):
        self._reap_loop()
        cached_object = self.cache.get(url)
        if cached_object is not None:
            warning_command_output("*")
            cached_response = cached_object[0]
            self.add(url, cached_response)
            return cached_response

        return None
    
    def _reap_loop(self):
        keys_to_delete = []

        actual_time = datetime.now()
        for cache_key, (_, expiration_time) in self.cache.items():
            if actual_time > expiration_time:
                keys_to_delete.append(cache_key)


        for key in keys_to_delete:
            self.cache.pop(key)




