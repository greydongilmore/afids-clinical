
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">AFIDs Clinical</h3>
  <p align="center">
    AFIDs framework applied to clinical imaging data.
    <br />
    <a href="https://github.com/greydongilmore/afids-clinical"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/greydongilmore/afids-clinical/issues">Report Bug</a>
    ·
    <a href="https://github.com/greydongilmore/afids-clinical/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#Repository Structure">Repository Structure</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This companion repository is for the article **Application of the anatomical fiducials framework to a clinical dataset of patients with Parkinson’s disease
Brain Structure and Function** submitted to the journal *Brain Structure & Function*.

### Built With

* Python version: 3.8
* Matlab version: vR2018b

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* No Prerequisites required

### Installation

1. In a terminal, clone the repo by running:
    ```sh
    git clone https://github.com/greydongilmore/afids-clinical.git
    ```

2. Change into the project directory (update path to reflect where you stored this project directory):
    ```sh
    cd /home/user/Documents/Github/afids-clinical
    ```

3. Install the required Python packages:
    ```sh
    python -m pip install -r src/python/requirements.txt
    ```


<!-- USAGE EXAMPLES -->
## Usage

* Linear transforms of fcsv to MNI are at: [/input/input_linear_transform](/input/input_linear_transform)
* Non-linear transforms of fcsv to MNI are at: [/input/input_mniTransform_fmriprep](/input/input_mniTransform_fmriprep)

### Repository Structure

The repository has the following scheme:
```
├── README.md
├── LICENSE.txt
├── data
|   ├── fid_standards
|   ├── input_fid_MNI_linear
|   ├── input_fid_MNI_nonlinear
|   ├── input_fid_native
|   ├── OASIS-1
|   └── demographics.tsv
├── manuscript
|   └── final_figures
├── results
|   ├── avg_fcsv
|   └── plots
└── src
    ├── matlab
    └── python
        └── requirements.txt
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

* Mohamad Abbass - mohamad.abbass26@gmail.com
* Greydon Gilmore - [@GilmoreGreydon](https://twitter.com/GilmoreGreydon) - greydon.gilmore@gmail.com

Project Link: [https://github.com/greydongilmore/afids-clinical](https://github.com/greydongilmore/afids-clinical)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* README format was adapted from [Best-README-Template](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/greydongilmore/afids-clinical.svg?style=for-the-badge
[contributors-url]: https://github.com/greydongilmore/afids-clinical/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/greydongilmore/afids-clinical.svg?style=for-the-badge
[forks-url]: https://github.com/greydongilmore/afids-clinical/network/members
[stars-shield]: https://img.shields.io/github/stars/greydongilmore/afids-clinical.svg?style=for-the-badge
[stars-url]: https://github.com/greydongilmore/afids-clinical/stargazers
[issues-shield]: https://img.shields.io/github/issues/greydongilmore/afids-clinical.svg?style=for-the-badge
[issues-url]: https://github.com/greydongilmore/afids-clinical/issues
[license-shield]: https://img.shields.io/github/license/greydongilmore/afids-clinical.svg?style=for-the-badge
[license-url]: https://github.com/greydongilmore/afids-clinical/blob/master/LICENSE.txt
