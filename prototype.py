
    def create_tag(self, name, comments="", location="vsys"):
        if location == "vsys":
            uri = f'Objects/tags?location={location}&{location}={self.vsys}&name={name}'
        else:
            uri = f'Objects/Addresses?location={location}&name={name}'

        payload = {
            "entry": {
                "@name": name,
                "description": comments
            }
        } 

        resp = self._post_req(self.rest_uri+uri,payload)

        return resp.json()
    

   def get_vsys_data(self, device_list=None):
        """
        returns the number (int) of vsys unused

        if no sn specified, method will pull all devices. 


        Firewall must be in multi vsys mode to have return data
        """
        
        devices_vsys = []
        if not device_list:
            devices = self.get_devices()
        else:
            devices = device_list