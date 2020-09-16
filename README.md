# AutoPlotter

autoplotter is a python package for GUI based exploratory data analysis. It is built on the top of dash.

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install autoplotter.

```bash
$pip install autoplotter
```

## Usage

```python
from autoplotter import run_app # Importing the autoplotter for GUI Based EDA
import pandas as pd # Importing Pandas to read csv

df = pd.read_csv("https://raw.githubusercontent.com/ersaurabhverma/autoplotter/master/Data/data.csv") # Reading data

run_app(df,mode = "inline", host="127.0.0.1", port=5000) # Calling the autoplotter.run_app in inline mode

run_app(df,mode = "external", host="127.0.0.1", port=5000) # Calling the autoplotter.run_app in external mode
```
[![Autoplotter.gif](https://s8.gifyu.com/images/Autoplotter.gif)](https://gifyu.com/image/gyrf)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Support 

- Support me by following on <a href="https://github.com/ersaurabhverma" target="_blank">Github</a> and <a href="https://www.linkedin.com/in/vermasaurabh8010/" target="_blank">LinkedIn</a>

<a href="https://www.buymeacoffee.com/ersaurabhverma" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
