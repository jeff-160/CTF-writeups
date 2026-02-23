from flask import Flask, request, render_template, jsonify
import base64
import sys
import os

app = Flask(__name__)
_EXEC_CMD = base64.b64decode(b'Q09MT1JTLmdldENvbG9ycygp').decode()
flag = os.environ.get('FLAG', 'lol u wish')

def _0x1a2b(_s, _d): 
    print(_s, _d)

    _get = getattr
    _set = setattr
    _has = hasattr
    _type = type
    _dict = dict
    for _k, _v in _s.items(): 
        if _has(_d, '__getitem__'): 
            _tmp = _d.get(_k) if hasattr(_d, 'get') else None
            if _tmp and _type(_v) == _dict: 
                _0x1a2b(_v, _tmp) 
            else: 
                _d[_k] = _v 
        elif _has(_d, _k) and _type(_v) == _dict: 
                _0x1a2b(_v, _get(_d, _k)) 
        else: 
            _set(_d, _k, _v)

class _ColorProcessor:
    def __init__(self, _c1="blue", _c2="green", _c3="orange"):
        self.color1 = _c1
        self.color2 = _c2
        self.color3 = _c3
        self._cache = {}
        self._debug = False
    
    def _get_palette(self):
        _spectrum = {
            base64.b64decode(b'cmVk').decode(): (255, 0, 0),
            base64.b64decode(b'b3Jhbmdl').decode(): (255, 165, 0),
            base64.b64decode(b'eWVsbG93').decode(): (255, 255, 0),
            base64.b64decode(b'Z3JlZW4=').decode(): (0, 255, 0),
            base64.b64decode(b'Ymx1ZQ==').decode(): (0, 0, 255),
            base64.b64decode(b'aW5kaWdv').decode(): (75, 0, 130),
            base64.b64decode(b'dmlvbGV0').decode(): (148, 0, 211)
        }
        return _spectrum

    def getColors(self):
        _palette = self._get_palette()
        
        _attr1 = str(self.color1).lower() if hasattr(self.color1, 'lower') else str(self.color1).lower()
        _attr2 = str(self.color2).lower() if hasattr(self.color2, 'lower') else str(self.color2).lower()
        _attr3 = str(self.color3).lower() if hasattr(self.color3, 'lower') else str(self.color3).lower()

        for _color_val in [_attr1, _attr2, _attr3]:
            if _color_val not in _palette:
                _error_msg = f"Error: '{_color_val}' is not one of the seven rainbow colors"
                return jsonify({
                    'message': _error_msg + " (red, orange, yellow, green, blue, indigo, violet)",
                    'rgb': [128, 128, 128]
                })

        _rgb_data = [_palette[_attr1], _palette[_attr2], _palette[_attr3]]
        _mixed = [sum(_rgb[i] for _rgb in _rgb_data) // len(_rgb_data) for i in range(3)]
        
        _closest = None
        _min_dist = sys.maxsize
        
        for _name, _rgb in _palette.items():
            _dist = sum((_mixed[i] - _rgb[i])**2 for i in range(3))**0.5
            if _dist < _min_dist:
                _min_dist = _dist
                _closest = _name

        return jsonify({
            'message': f"Mixing {_attr1}, {_attr2}, and {_attr3} results in: {_closest}",
            'rgb': _mixed
        })
        
COLORS = _ColorProcessor("blue", "green", "orange")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/colors', methods=['POST'])
def colors():
    try:
        _req_data = request.json
        if not _req_data:
            return jsonify({
                'error': 'Invalid input: JSON body is required.'
            }), 400

        _required_fields = {'color1', 'color2', 'color3'}
        if not _required_fields.issubset(_req_data.keys()):
            return jsonify({
                'error': f"Invalid input: Keys {_required_fields} are required."
            }), 400

        _0x1a2b(_req_data, COLORS)
        _result = eval(_EXEC_CMD)
        return _result

    except Exception as _ex:
        return jsonify({
            'error': f"An unexpected error occurred: {str(_ex)}"
        }), 500

if __name__ == '__main__':
    _host_config = '0.0.0.0'
    _port_config = 6789
    
    app.run(host=_host_config, port=_port_config)
