from sarpaminfohub.infohub.backend import Backend

class TestBackend(Backend):
    def search(self, search_term):
        return [{\
            "formulation":"ciprofloxacin 500mg tablet",\
            "fob_price":"0.05",\
            "landed_price":"0.06",\
            "country":"South Africa"}]
