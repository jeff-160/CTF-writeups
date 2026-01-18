
class Theme():
    default: dict[str, str] = {
        'color': '#ffa500',
        'background-color': 'white',
    }
    customs = {}
    
    def __init__(self, custom : dict[str, str] | None) -> None:
        self.style = custom | Theme.default
        
    @staticmethod
    def add(username, theme):
        Theme.customs[str(username)] = theme

    @staticmethod
    def get(username):
        return Theme.customs[str(username)]
    