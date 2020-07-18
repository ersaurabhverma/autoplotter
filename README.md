# AutoPlotter

autoplotter is a python package for GUI based exploratory data analysis. It is built on the top of dash.

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install autoplotter.

```bash
pip install autoplotter
```

## Usage

```python
from autoplotter import run_app # Importing the autoplotter for GUI Based EDA

import plotly.express as px # Importing plotly express to load dataset
df = px.data.tips() # Getting the   Restaurant data

run_app(df) # Calling the autoplotter.run_app
```
[![LWR-Recording-2.gif](https://s7.gifyu.com/images/LWR-Recording-2.gif)](https://gifyu.com/image/QGyH)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Support 

- Support me by following on <a href="https://github.com/ersaurabhverma" target="_blank">Github</a> and <a href="https://www.linkedin.com/in/vermasaurabh8010/" target="_blank">LinkedIn</a>.


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
